import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def parse_logfile(filename):

    time, spec1, spec2, spec3 = [], [], [], []

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "Time" in line:
            start_index = lines.index(line) + 1
            break

    for line in lines[start_index:]:
        if not line.split()[0].replace('.','',1).isdigit():  # Stop parsing when line does not start with a number
            break

        data = line.split()
        time.append(float(data[0]))  # Convert the first entry (Time) to float
        spec1.append(float(data[6]))  # Convert the spec1 quantity to float (7th column in your log)
        spec2.append(float(data[7]))  # Convert the spec2 quantity to float (8th column in your log)
        spec3.append(float(data[8]))

    return time, spec1, spec2, spec3

def interpolate_to_common_time(time, spec, common_time):
    interpolation_function = interp1d(time, spec, fill_value="extrapolate")
    return interpolation_function(common_time)

# choose common time points as the union of all time points in all runs
common_time = np.unique(np.concatenate([parse_logfile('log{}.spparks'.format(seed))[0] for seed in range(1, 11)]))

# initialize arrays for averages
spec1_avg = np.zeros_like(common_time)
spec2_avg = np.zeros_like(common_time)
spec3_avg = np.zeros_like(common_time)

count = 0  # counter to track number of seeds included in average

for seed in range(1, 11):
    time, spec1, spec2, spec3 = parse_logfile('log{}.spparks'.format(seed))

    total_population = np.array(spec1)[0] + np.array(spec2)[0] + np.array(spec3)[0]
    
    spec1 = interpolate_to_common_time(time, np.array(spec1)/total_population, common_time)
    spec2 = interpolate_to_common_time(time, np.array(spec2)/total_population, common_time)
    spec3 = interpolate_to_common_time(time, np.array(spec3)/total_population, common_time)
    
    if spec2[-1] == 0:  # if spec3 is zero for all times
        plt.plot(common_time, spec1, 'bo', alpha=0.002, markersize=1, color='lightblue')
        plt.plot(common_time, spec2, 'ro', alpha=0.002, markersize=1, color='lightcoral')
        plt.plot(common_time, spec3, 'go', alpha=0.002, markersize=1, color='lightgreen')
        
    else:
        spec1_avg += spec1
        spec2_avg += spec2
        spec3_avg += spec3
        count += 1  # increment counter
        plt.plot(common_time, spec1, 'bo', alpha=0.002, markersize=1)
        plt.plot(common_time, spec2, 'ro', alpha=0.002, markersize=1)
        plt.plot(common_time, spec3, 'go', alpha=0.002, markersize=1)

spec1_avg /= count
spec2_avg /= count
spec3_avg /= count

# plot averages
plt.plot(common_time, spec1_avg, 'b-', label='Average Susceptible')
plt.plot(common_time, spec2_avg, 'r-', label='Average Infected')
plt.plot(common_time, spec3_avg, 'g-', label='Average Recovered')

plt.xlabel('Time')
plt.ylabel('Quantity')
plt.title('Quantity of Spec1 and Spec2 Over Time')
plt.legend()
plt.grid(True)
plt.savefig("a_graph.png")  # Save the figure as "graph.png"

plt.show()
