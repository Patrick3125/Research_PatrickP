import matplotlib.pyplot as plt
import numpy as np
import os

# Path where the files are stored
path = "../"

# Automatically detect the number of correlation data files
correlation_files = [f for f in os.listdir(path) if f.startswith('sir_')]
num_files = len(correlation_files)

data = np.loadtxt(os.path.join(path, "sir_averages.txt"))
x_val = data[:, 0]
s_av = data[:, 1]
i_av = data[:, 2]
r_av = data[:, 3]

fig, ax = plt.subplots()

plt.plot(0, 0, 'k-', label='Averaged raw data from ABM')
plt.plot(x_val, s_av, 'b-')
plt.plot(x_val, i_av, 'r-')
plt.plot(x_val, r_av, 'g-')

# Plot each individual sir. -3 because average, method1 and method2 
for i in range(0, num_files-3):
        individual_data = np.loadtxt(os.path.join(path, "sir_indiv" + str(i) + ".txt"))
        s_indiv = individual_data[:, 1]
        i_indiv = individual_data[:, 2]
        r_indiv = individual_data[:, 3]
        ax.plot(x_val, s_indiv, 'o', color = '#8080FF', alpha=0.05, markersize=1)
        ax.plot(x_val, i_indiv, 'o', color = '#FF8080', alpha=0.05, markersize=1)
        ax.plot(x_val, r_indiv, 'o', color = '#80FF80', alpha=0.05, markersize=1)

shapestep = 60
x_valstep = x_val[::shapestep]

# Plot the graph from method 1
data = np.loadtxt(os.path.join(path, "sir_ode.txt"))
s_ode = data[::shapestep, 0]
i_ode = data[::shapestep, 1]
r_ode = data[::shapestep, 2]

ax.plot(x_valstep, s_ode, 'm^', markersize=7, label='Method 1 (Least Squares)')
ax.plot(x_valstep, i_ode, 'm^', markersize=7)
ax.plot(x_valstep, r_ode, 'm^', markersize=7)

# Plot the grpah from method 2
data = np.loadtxt(os.path.join(path, "sir_contact.txt"))
s_con = data[::shapestep, 0]
i_con = data[::shapestep, 1]
r_con = data[::shapestep, 2]

ax.plot(x_valstep, s_con, 'co', markersize=7, label='Method 2 (Contact Number)')
ax.plot(x_valstep, i_con, 'co', markersize=7)
ax.plot(x_valstep, r_con, 'co', markersize=7)

ax.grid(True)
plt.legend(fontsize = 15, loc='upper right')
plt.xlabel("Days", fontsize=21)
plt.ylabel("Proportion of Population", fontsize=21)
plt.title(r"Comparison of the two methods on finding optimal $\bf{b}$ and $\bf{k}$ values", fontsize=25)

plt.show()



