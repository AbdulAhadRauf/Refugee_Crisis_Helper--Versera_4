import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog

def optimize_food_distribution(supply, demand, cost_matrix):
    """
    Optimize food distribution using linear programming.
    Parameters:
        supply (list): Food supply amounts for each center.
        demand (list): Food demand amounts for each location.
        cost_matrix (list of lists): Delivery cost from each supply center to each demand location.
    Returns:
        plan (numpy.ndarray): Matrix indicating how much food to deliver from each center to each location.
    """
    num_supply = len(supply)
    num_demand = len(demand)
    
    # Flatten cost matrix for linprog
    c = np.array(cost_matrix).flatten()
    
    # Build equality constraints:
    A_eq = []
    b_eq = []
    
    # Supply constraints: Sum of shipments from each center equals its supply.
    for i in range(num_supply):
        row = [0] * (num_supply * num_demand)
        for j in range(num_demand):
            row[i * num_demand + j] = 1
        A_eq.append(row)
        b_eq.append(supply[i])
    
    # Demand constraints: Sum of shipments to each location equals its demand.
    for j in range(num_demand):
        row = [0] * (num_supply * num_demand)
        for i in range(num_supply):
            row[i * num_demand + j] = 1
        A_eq.append(row)
        b_eq.append(demand[j])
    
    bounds = [(0, None) for _ in range(num_supply * num_demand)]
    
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    if res.success:
        plan = np.array(res.x).reshape((num_supply, num_demand))
        return plan
    else:
        return None

def app():
    st.title("AI-Driven Food Distribution Optimizer")
    st.write("Optimize food distribution to minimize costs and reduce waste.")
    
    st.sidebar.header("Input Data")
    num_sources = st.sidebar.number_input("Number of Supply Centers", min_value=1, max_value=10, value=2)
    num_destinations = st.sidebar.number_input("Number of Demand Locations", min_value=1, max_value=10, value=2)
    
    st.write("### Supply Amounts")
    supply = []
    for i in range(num_sources):
        amount = st.number_input(f"Supply at Center {i+1}", min_value=0, value=100, key=f"supply_{i}")
        supply.append(amount)
    
    st.write("### Demand Amounts")
    demand = []
    for j in range(num_destinations):
        amount = st.number_input(f"Demand at Location {j+1}", min_value=0, value=50, key=f"demand_{j}")
        demand.append(amount)
    
    st.write("### Cost Matrix")
    cost_matrix = []
    for i in range(num_sources):
        row = []
        for j in range(num_destinations):
            cost = st.number_input(f"Cost from Center {i+1} to Location {j+1}", min_value=0.0, value=1.0, key=f"cost_{i}_{j}")
            row.append(cost)
        cost_matrix.append(row)
    
    if st.button("Optimize Distribution"):
        plan = optimize_food_distribution(supply, demand, cost_matrix)
        if plan is not None:
            st.success("Optimization Successful!")
            st.write("Optimized Distribution Plan:")
            df_plan = pd.DataFrame(
                plan,
                index=[f"Center {i+1}" for i in range(num_sources)],
                columns=[f"Location {j+1}" for j in range(num_destinations)]
            )
            st.dataframe(df_plan)
        else:
            st.error("Optimization Failed. Please check your input data.")
