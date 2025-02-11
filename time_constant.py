import pandas as pd
import numpy as np
import math

#Function equation takes in seconds as input and returns the theoretical voltages for each multiple of the time constant that exists within the interval (time_constant, seconds)
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

#Function grab_v0 takes the midpoint in as input and returns the value of the voltage at the time of the midpoint, at the beginning of discharge
def grab_v0(midpoint):
    df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

    row = df[df['Time'] == midpoint]

    return row['Voltage'].tolist()[0]

#Function remove_outliers takes in a dictionary voltages and the Pandas datafram df as input and returns a list of all of the dataframes with outliers removed
#Outliers are rows with times that deviate from the target time by more than 10 seconds
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

#Function average_time takes in a list of dataframes matches as input and returns a list of the average times in each dataframe
def average_time(matches):
    average_times = []

    for row in matches:
        total = sum(row['Time'].tolist())
        average_times.append(total / len(row['Time'].tolist()))
    
    return average_times
     
#Function main takes nothing in as input and strings everything together
def main():
    df = pd.read_csv('RC Lab Data - Sheet1.csv', header=0)

    seconds = 70

    voltages = equation(seconds)

    matches = remove_outliers(voltages, df)

    for match in matches:
        print(f"{match}\n")

    means = average_time(matches)

    print("Voltage --> Expected Time --> Observed Time")
    for i in range(len(means)):
        print(f"{list(voltages.values())[i]} --> {list(voltages.keys())[i]} --> {round(means[i], 3)}")

main()
