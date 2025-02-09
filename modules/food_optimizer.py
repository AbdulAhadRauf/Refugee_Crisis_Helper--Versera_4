# modules/food_optimizer.py
import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

def optimize_food_distribution(supply, demand, cost_matrix):
    """
    Optimize food distribution using the transportation problem formulation.
    
    Parameters:
        supply (list): Food supply amounts for each supply center.
        demand (list): Food demand amounts for each demand location.
        cost_matrix (list of lists): Delivery cost from each supply center to each demand location.
        
    Returns:
        plan (list of lists): Matrix indicating the optimal amount of food to deliver from each center to each location.
        total_cost (float): The minimized total transportation cost.
        status (str): The status of the LP solution (e.g., "Optimal", "Infeasible").
    """
    num_supply = len(supply)
    num_demand = len(demand)
    
    # Create the Linear Programming problem with the goal of minimizing transportation cost.
    prob = LpProblem("Food_Distribution_Optimization", LpMinimize)
    
    # Create decision variables: x[i][j] represents the amount shipped from supply i to demand j.
    x = [[LpVariable(f"x_{i}_{j}", lowBound=0, cat="Continuous") 
          for j in range(num_demand)] for i in range(num_supply)]
    
    # Objective: minimize total cost = sum(cost[i][j] * x[i][j] for all i, j)
    prob += lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_supply) for j in range(num_demand)), "Total_Transportation_Cost"
    
    # Supply constraints: each supply center should ship out exactly its available supply.
    for i in range(num_supply):
        prob += lpSum(x[i][j] for j in range(num_demand)) == supply[i], f"Supply_Constraint_{i}"
    
    # Demand constraints: each demand location must receive exactly its required demand.
    for j in range(num_demand):
        prob += lpSum(x[i][j] for i in range(num_supply)) == demand[j], f"Demand_Constraint_{j}"
    
    # Solve the problem using PuLP's default solver.
    prob.solve()
    
    # Check if the solution is optimal.
    status = LpStatus[prob.status]
    if status != "Optimal":
        return None, None, status
    
    # Extract the optimal plan from the decision variables.
    plan = [[x[i][j].varValue for j in range(num_demand)] for i in range(num_supply)]
    total_cost = value(prob.objective)
    
    return plan, total_cost, status

def app():
    st.title("AI-Driven Food Distribution Optimizer")
    st.write("Optimize food distribution to minimize costs and reduce waste.")
    
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
    
    if st.button("Optimize Distribution"):
        plan, total_cost, status = optimize_food_distribution(supply, demand, cost_matrix)
        if status == "Optimal":
            st.success("Optimization Successful!")
            st.write("### Optimized Distribution Plan:")
            df_plan = pd.DataFrame(
                plan,
                index=[f"Center {i+1}" for i in range(num_sources)],
                columns=[f"Location {j+1}" for j in range(num_destinations)]
            )
            st.dataframe(df_plan)
            st.write(f"**Total Transportation Cost:** {total_cost:.2f}")
        else:
            st.error(f"Optimization Failed. Status: {status}")

# Uncomment the following lines to run this module directly for testing.
# if __name__ == "__main__":
#     app()
