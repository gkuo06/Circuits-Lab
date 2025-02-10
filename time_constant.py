import pandas as pd
import numpy as np


def equation(time_constants):
    emf = 4.5
    resistance = 15000
    capacitance = 0.001
    time_constant = resistance * capacitance

    theoretical_times = np.linspace(time_constant, time_constants * time_constant, time_constants)
    theoretical_voltages = {}

    for time in theoretical_times:
        theoretical_voltages[time] = (emf * (1 - np.exp(-time/time_constant)))
    
    return theoretical_voltages


df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

voltages = equation(4)

df["Voltage"] = pd.to_numeric(df["Voltage"], errors='coerce')

print(voltages)

for target_voltage in voltages.values():
    time_row = df[abs(df['Voltage'] - target_voltage) <= 0.001]

    print(time_row)




        


