# modules/food_optimizer.py
import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

def optimize_food_distribution(supply, demand, cost_matrix):
    """
    Optimize food distribution using the transportation problem formulation.
    
    This function automatically balances the problem by adding a dummy supply
    or dummy demand if total supply != total demand.
    
    Parameters:
        supply (list): Food supply amounts for each supply center.
        demand (list): Food demand amounts for each demand location.
        cost_matrix (list of lists): Delivery cost from each supply center to each demand location.
        
    Returns:
        plan (list of lists): Matrix indicating the optimal shipment plan for the original supply centers and demand locations.
        total_cost (float): The minimized total transportation cost.
        status (str): The status of the LP solution (e.g., "Optimal", "Infeasible").
    """
    original_num_supply = len(supply)
    original_num_demand = len(demand)
    total_supply = sum(supply)
    total_demand = sum(demand)
    dummy_added = False
    dummy_type = None  # "supply" or "demand"
    
    # Balance the problem if necessary.
    if total_supply < total_demand:
        # Add a dummy supply center to absorb the extra demand.
        dummy_supply = total_demand - total_supply
        supply.append(dummy_supply)
        # For the dummy supply, set cost=0 for all demand locations.
        dummy_row = [0.0 for _ in range(original_num_demand)]
        cost_matrix.append(dummy_row)
        dummy_added = True
        dummy_type = "supply"
    elif total_supply > total_demand:
        # Add a dummy demand location to absorb the extra supply.
        dummy_demand = total_supply - total_demand
        demand.append(dummy_demand)
        # For each supply center, add a dummy cost of 0 for shipping to the dummy demand.
        for i in range(original_num_supply):
            cost_matrix[i].append(0.0)
        dummy_added = True
        dummy_type = "demand"
    
    # Update the number of supply centers and demand locations after balancing.
    num_supply = len(supply)
    num_demand = len(demand)
    
    # Create the LP problem.
    prob = LpProblem("Food_Distribution_Optimization", LpMinimize)
    
    # Create decision variables: x[i][j] represents the shipment from supply i to demand j.
    x = [[LpVariable(f"x_{i}_{j}", lowBound=0, cat="Continuous") 
          for j in range(num_demand)] for i in range(num_supply)]
    
    # Objective: minimize total cost.
    prob += lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_supply) for j in range(num_demand)), "Total_Transportation_Cost"
    
    # Supply constraints: Each supply center ships exactly its available supply.
    for i in range(num_supply):
        prob += lpSum(x[i][j] for j in range(num_demand)) == supply[i], f"Supply_Constraint_{i}"
    
    # Demand constraints: Each demand location receives exactly its required demand.
    for j in range(num_demand):
        prob += lpSum(x[i][j] for i in range(num_supply)) == demand[j], f"Demand_Constraint_{j}"
    
    # Solve the problem.
    prob.solve()
    status = LpStatus[prob.status]
    if status != "Optimal":
        return None, None, status
    
    # Extract the optimal plan.
    full_plan = [[x[i][j].varValue for j in range(num_demand)] for i in range(num_supply)]
    total_cost = value(prob.objective)
    
    # Remove the dummy row or column from the plan if one was added.
    if dummy_added:
        if dummy_type == "supply":
            # Remove the dummy supply (last row).
            plan = full_plan[:original_num_supply]
        elif dummy_type == "demand":
            # Remove the dummy demand (last column) from each row.
            plan = [row[:original_num_demand] for row in full_plan]
    else:
        plan = full_plan
    
    return plan, total_cost, status

def app():
    st.title("AI-Driven Food Distribution Optimizer")
    st.write("Optimize food distribution to minimize costs and reduce waste.\n\n"
             "Note: Ensure that the total supply equals the total demand, or the problem will be automatically balanced.")
    
    # Sidebar inputs for number of supply centers and demand locations.
    st.sidebar.header("Input Data")
    num_sources = st.sidebar.number_input("Number of Supply Centers", min_value=1, max_value=10, value=2)
    num_destinations = st.sidebar.number_input("Number of Demand Locations", min_value=1, max_value=10, value=2)
    
    # Input fields for supply amounts.
    st.write("### Supply Amounts")
    supply = []
    for i in range(num_sources):
        amount = st.number_input(f"Supply at Center {i+1}", min_value=0, value=100, key=f"supply_{i}")
        supply.append(amount)
    
    # Input fields for demand amounts.
    st.write("### Demand Amounts")
    demand = []
    for j in range(num_destinations):
        amount = st.number_input(f"Demand at Location {j+1}", min_value=0, value=50, key=f"demand_{j}")
        demand.append(amount)
    
    # Input fields for the cost matrix.
    st.write("### Cost Matrix")
    cost_matrix = []
    for i in range(num_sources):
        row = []
        for j in range(num_destinations):
            cost = st.number_input(f"Cost from Center {i+1} to Location {j+1}", min_value=0.0, value=1.0, key=f"cost_{i}_{j}")
            row.append(cost)
        cost_matrix.append(row)
    
    if st.button("Optimize Distribution", key="optimize_distribution_button"):
        plan, total_cost, status = optimize_food_distribution(supply, demand, cost_matrix)
        if status == "Optimal":
            st.success("Optimization Successful!")
            st.write("### Optimized Distribution Plan:")
            df_plan = pd.DataFrame(
                plan,
                index=[f"Center {i+1}" for i in range(len(plan))],
                columns=[f"Location {j+1}" for j in range(len(plan[0]))]
            )
            st.dataframe(df_plan)
            st.write(f"**Total Transportation Cost:** {total_cost:.2f}")
        else:
            st.error(f"Optimization Failed. Status: {status}")
