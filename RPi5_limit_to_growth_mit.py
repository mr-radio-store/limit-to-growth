import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Limit to growth by MIT
# add more noise pandemic, financial crisis, etc.
# -----------------------------
years = np.arange(1900, 2101)
dt = 1.0
np.random.seed(42)  # reproducible

# -----------------------------
# State variables (normalized)
# -----------------------------
population = np.zeros(len(years))
industry   = np.zeros(len(years))
resources  = np.zeros(len(years))
pollution  = np.zeros(len(years))
food       = np.zeros(len(years))

# Initial conditions
population[0] = 1.0
industry[0]   = 1.0
resources[0]  = 1.0
pollution[0]  = 0.1
food[0]       = 1.0

# -----------------------------
# Model parameters
# -----------------------------
pop_growth     = 0.02
ind_growth     = 0.03
resource_use   = 0.02
pollution_rate = 0.015
cleanup_rate   = 0.005
food_growth    = 0.02

# -----------------------------
# Crisis definitions
# -----------------------------
pandemic_years = [1918, 2020]       # Spanish flu, COVID
financial_crisis_years = [1929, 2008]
energy_crisis_years = [1973, 2022]

# -----------------------------
# Simulation loop
# -----------------------------
for t in range(1, len(years)):
    y = years[t]

    # Noise (system uncertainty)
    noise_pop  = np.random.normal(0, 0.01)
    noise_ind  = np.random.normal(0, 0.015)
    noise_food = np.random.normal(0, 0.01)

    # Base factors
    resource_factor  = resources[t-1]
    pollution_factor = max(0.0, 1.0 - pollution[t-1])

    # Crisis multipliers (default = no shock)
    pop_shock = 1.0
    ind_shock = 1.0
    food_shock = 1.0
    pollution_shock = 1.0
    resource_shock = 1.0

    # Pandemic shock
    if y in pandemic_years:
        pop_shock = 0.97
        ind_shock = 0.90
        food_shock = 0.95
        pollution_shock = 0.85  # temporary emission drop

    # Financial crisis
    if y in financial_crisis_years:
        ind_shock = 0.88
        food_shock = 0.93

    # Energy / resource crisis
    if y in energy_crisis_years:
        resource_shock = 1.4
        ind_shock *= 0.92

    # -----------------------------
    # Update equations
    # -----------------------------
    population[t] = population[t-1] + dt * population[t-1] * (
        pop_growth * food[t-1] * pollution_factor - 0.01 + noise_pop
    )
    population[t] *= pop_shock

    industry[t] = industry[t-1] + dt * industry[t-1] * (
        ind_growth * resource_factor - 0.02 * pollution[t-1] + noise_ind
    )
    industry[t] *= ind_shock

    resources[t] = max(
        0.0,
        resources[t-1] - dt * resource_use * industry[t-1] * resource_shock
    )

    pollution[t] = pollution[t-1] + dt * (
        pollution_rate * industry[t-1] * pollution_shock
        - cleanup_rate * pollution[t-1]
    )

    food[t] = food[t-1] + dt * food_growth * food[t-1] * (
        resource_factor + noise_food
    )
    food[t] *= food_shock

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10, 6))
plt.plot(years, population, label="Population")
plt.plot(years, industry, label="Industry")
plt.plot(years, resources, label="Resources")
plt.plot(years, pollution, label="Pollution")
plt.plot(years, food, label="Food")

plt.xlabel("Year")
plt.ylabel("Normalized Level")
plt.title("Limits to Growth with Crises & Noise (Raspberry Pi 5)")
plt.legend()
plt.grid(True)

plt.savefig("limits_to_growth_with_crises.jpg", dpi=200)
plt.close()

print("Saved: limits_to_growth_with_crises.jpg")
