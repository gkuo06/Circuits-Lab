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
        theoretical_voltages[time] = (v0 * np.exp(-(time - (seconds//2))/time_constant))

    return theoretical_voltages


def grab_v0(midpoint):
    df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

    row = df[df['Time'] == midpoint]

    return row['Voltage'].tolist()[0]


def remove_outliers(voltages, df):
    rows = []
    for time, voltage in voltages.items():
        time_row = df[abs(df['Voltage'] - voltage) <= 0.001]

        dropped_indices = []

        for i in range(len(time_row['Time'].tolist())):
            if (abs(time_row['Time'].tolist()[i] - time) > 10):
                dropped_indices.append(int(time_row.index[i]))

        time_row = time_row.drop(dropped_indices, errors='ignore')

        rows.append(time_row)

    return rows

def average_time(matches):
    average_times = []

    for row in matches:
        total = sum(row['Time'].tolist())
        average_times.append(total / len(row['Time'].tolist()))
    
    return average_times
     
def main():
    df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

    seconds = 70

    voltages = equation(seconds)

    matches = remove_outliers(voltages, df)

    for match in matches:
        print(f"{match}\n")

    means = average_time(matches)

    print("Expected --> Observed")
    for i in range(len(means)):
        print(f"{list(voltages.keys())[i]} --> {means[i]}")

main()
