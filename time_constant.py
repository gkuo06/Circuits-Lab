import pandas as pd
import numpy as np
import math

#Function equation takes in seconds as input and return the theoretical voltages for each multiple of the time constant that exists within the interval (time_constant, seconds)
def equation(seconds):
    emf = 4.5
    resistance = 15000
    capacitance = 0.001
    time_constant = resistance * capacitance
    time_constants = math.floor(seconds / time_constant)

    theoretical_times = np.linspace(time_constant, time_constants * time_constant, time_constants)

    charge_times = theoretical_times[:((len(theoretical_times) + 1) // 2)]
    discharge_times = theoretical_times[((len(theoretical_times) + 1) // 2):]

    theoretical_voltages = {}

    v0 = grab_v0(seconds // 2)

    for time in charge_times:
        theoretical_voltages[time] = (emf * (1 - np.exp(-time/time_constant)))
    
    for time in discharge_times:
        theoretical_voltages[time] = (v0 * np.exp(-time/time_constant))

    return theoretical_voltages


def grab_v0(midpoint):
    df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

    row = df[df['Time'] == midpoint]

    return row['Time'].tolist()[0]

df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

voltages = equation(70)

df["Voltage"] = pd.to_numeric(df["Voltage"], errors='coerce')

print(voltages)

for target_voltage in voltages.values():
    time_row = df[abs(df['Voltage'] - target_voltage) <= 0.001]

    print(time_row)



        


