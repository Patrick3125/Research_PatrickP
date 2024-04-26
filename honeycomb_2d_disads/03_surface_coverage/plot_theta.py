from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
import json
import os
# Define symbols
m, j, k = symbols('m j k', integer=True)
k_value = 5

theta_analytical = []
theta_simulation = []
num_sites = []
theta_means = []
theta_errors = []
theta = -1
is_bipartite=[]

#reading how many log files there are
log_folders = [item for item in os.listdir('../') if os.path.isdir(os.path.join('../', item)) and item.startswith('log_') and item.count('_') == 2]
x_vals = []
y_vals = []
for folder in log_folders:
    parts = folder.split('_')
    if len(parts) == 3:
        try:
            x = int(parts[1])
            y = int(parts[2])
            x_vals.append(x)
            y_vals.append(y)
        except ValueError:
            continue
for i in range(len(x_vals)):
    x = x_vals[i]
    y = y_vals[i]
    N = x * y * 2
    num_sites.append(N)
    # Always non-bipartite
    is_bipartite.append(False)

    m_value = N / 2
    numerator_sum = Sum(binomial(m, j) *binomial(m - 1, j) * k**j, (j, 0, m-1))
    denominator_sum = Sum(binomial(m, j)**2 * k**j, (j, 0, m))
    theta_analytical_expr =  (numerator_sum / denominator_sum)

    # Get k value from json file
    with open('../log_{}_{}'.format(x, y) + '/variables.txt') as f:
        data = json.load(f)
        ra2 = data['ra2']
        rd2 = data['rd2']
        k_value = rd2/ra2
        theta = 1/(1+math.sqrt(k_value))


    theta_analytical_simplified = theta_analytical_expr.subs({m: m_value, k: k_value})
    theta_analytical_temp = theta_analytical_simplified.doit().evalf()
    theta_analytical.append(theta_analytical_temp)
 
    with open('../res_{}_{}'.format(x, y) + '/average_surface_coverage.txt') as f:
       f.readline()  # Skip the first row
       theta_values = [float(line) for line in f]  # Assuming the second column is theta
       theta_mean = sum(theta_values) / len(theta_values)

       sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
       standard_error = ((sample_variance / len(theta_values)) ** 0.5)
       theta_means.append(theta_mean)
       theta_errors.append(standard_error)
 

theta_errors_3sigma = [error * 3 for error in theta_errors]

plt.figure(figsize=(4.5, 3))

# Initializing lists for storing sorted data
bp_sites = []
bp_means = []
bp_errors = []
nbp_sites = []
nbp_means = []
nbp_errors = []

# Sort num_sites in numerical order for plotting
for i in range(len(num_sites)):
    if is_bipartite[i]:
        bp_sites.append(num_sites[i])
        bp_means.append(theta_means[i])
        bp_errors.append(theta_errors_3sigma[i])
    else:
        nbp_sites.append(num_sites[i])
        nbp_means.append(theta_means[i])
        nbp_errors.append(theta_errors_3sigma[i])

# Sort the bipartite lists
if bp_sites:
    zipped_bp = zip(bp_sites, bp_means, bp_errors)
    sorted_bp = sorted(zipped_bp)
    bp_sites, bp_means, bp_errors = zip(*sorted_bp)
else:
    bp_sites, bp_means, bp_errors = ([],[],[])

# Sort the non-bipartite lists
if nbp_sites:
    zipped_nbp = zip(nbp_sites, nbp_means, nbp_errors)
    sorted_nbp = sorted(zipped_nbp)
    nbp_sites, nbp_means, nbp_errors = zip(*sorted_nbp)
else:
    nbp_sites, nbp_means, nbp_errors = ([], [], [])

# Convert zipped lists back to lists
bp_sites = list(bp_sites)
bp_means = list(bp_means)
bp_errors = list(bp_errors)

nbp_sites = list(nbp_sites)
nbp_means = list(nbp_means)
nbp_errors = list(nbp_errors)

# lines for non-bipartite
plt.plot(nbp_sites, nbp_means, '-', color='green', linewidth=1, zorder=10)

print(nbp_sites)
print(nbp_means)
# Error bars for non-bipartite
plt.errorbar(nbp_sites,
             nbp_means,
             yerr=nbp_errors,
             fmt='none', ecolor='red', zorder=20)

# Plot lines for bipartite
plt.plot(bp_sites, bp_means, '-', color='blue', linewidth=1, zorder=10)

# Error bars for bipartite
plt.errorbar(bp_sites,
             bp_means,
             yerr=bp_errors,
             fmt='none', ecolor='red', zorder=20)

#empty graph for labeling
plt.errorbar(0,0, yerr = 0, color = 'green', ecolor='red', label = r'Non-bipartite lattice with $N$ values')
plt.errorbar(0,0, yerr = 0, color = 'blue', ecolor='red', label = r'Bipartite lattice with $N$ values')


#plt.scatter(product_values, theta_from_res_results, label='Theta from Simulation', marker='x')
plt.scatter(num_sites, theta_analytical, label=r'Theoretical $\overline{\theta}_N$', marker='o',facecolors='none',  edgecolors = 'blue')

plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

plt.axhline(y=theta, color='black', linestyle=':')
plt.text(x=103,
         y=theta+0.003,
         s=r'$\overline{\theta}_\infty$',
         fontsize=12)

plt.xlim(0, 110)
plt.ylim(0.23, 0.33)

x_ticks = plt.gca().get_xticks()
y_ticks = plt.gca().get_yticks()

plt.gca().set_xticklabels(['{:.0f}'.format(x_ticks[0]), '', '{:.0f}'.format(x_ticks[2]), '', '{:.0f}'.format(x_ticks[4])])
plt.gca().set_yticklabels(['{:.2f}'.format(y_ticks[0]), '{:.2f}'.format(y_ticks[1]), '', '{:.2f}'.format(y_ticks[3]), '', '{:.2f}'.format(y_ticks[5])])

plt.rcParams['font.size'] = 12

plt.xlabel(r'Number of sites $N$', fontsize = 12)
plt.ylabel(r'$\overline{\theta}_N$  ', rotation='horizontal', fontsize = 12, labelpad=7)
plt.legend(loc='lower right')

plt.tight_layout()
plt.grid(True)
plt.savefig('periodic_1d_even_odd.png', format='png', dpi=300)
plt.show()
