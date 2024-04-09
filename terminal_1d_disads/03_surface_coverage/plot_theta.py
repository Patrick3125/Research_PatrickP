from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
import json
import os
# define symbols
m, j, k = symbols('m j k', integer=True)
k_value = 5

theta_analytical = []
theta_simulation = []
num_sites = []  
theta_means = []  
theta_errors = []
theta = -1

# search for folders with name ../log_*
# N_values is an array containing number of sites used in simulation
log_folders = [item for item in os.listdir('../') if os.path.isdir(os.path.join('../', item)) and item.startswith('log_')]
N_values = sorted([int(folder.split('_')[1]) for folder in log_folders])

for N in N_values:
    num_sites.append(N)

    # Depending on the oddity of the number of sites, use a different equation
    # Equation for calculating analytical value

    if N % 2 == 1:
        m_value = (N - 1) / 2  # Use integer division for m_value
        numerator_sum = Sum((m-j)*binomial(m+1, j+1)*binomial(m, j) * k**j, (j, 0, m-1))
        denominator_sum = Sum(binomial(m+1, j+1) * binomial(m,j) * k**j, (j, 0, m))
        theta_analytical_expr = 2 / (m*2+1) * (numerator_sum / denominator_sum)

    else:
        m_value = N / 2  # Use integer division for m_value
        numerator_sum = Sum( binomial(m-1, j) *binomial(m,j)* k**j, (j, 0, m-1))
        denominator_sum = Sum(binomial(m, j)**2 * k**j, (j, 0, m))
        theta_analytical_expr =  (numerator_sum / denominator_sum)


    # Get k value from json file
    with open('../log_{}'.format(N) + '/variables.txt') as f:
        data = json.load(f)
        ra2 = data['ra2']
        rd2 = data['rd2']
        k_value = rd2/ra2
        theta = 1/(1+math.sqrt(k_value))
    
    theta_analytical_simplified = theta_analytical_expr.subs({m: m_value, k: k_value})
    theta_analytical_temp = theta_analytical_simplified.doit().evalf()
    theta_analytical.append(theta_analytical_temp)
   

    # Compute the error bar and average from simulation data
    with open('../res_{}'.format(N) + '/average_surface_coverage.txt') as f:
        f.readline() 
        theta_values = [float(line) for line in f]  
        theta_mean = sum(theta_values) / len(theta_values)

        sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
        standard_error = ((sample_variance / len(theta_values)) ** 0.5)
        theta_means.append(theta_mean)
        theta_errors.append(standard_error)
 
theta_errors_3sigma = [error * 3 for error in theta_errors]


plt.figure(figsize=(4.5, 3))

even_indices = range(0, len(num_sites), 2)  
odd_indices = range(1, len(num_sites), 2)  


# Plot lines for odd points with lower zorder
plt.plot([num_sites[i] for i in odd_indices], [theta_means[i] for i in odd_indices], '-', color='green', linewidth=1, zorder=10)

# Error bars for odd points with higher zorder
plt.errorbar([num_sites[i] for i in odd_indices],
             [theta_means[i] for i in odd_indices],
             yerr=[theta_errors_3sigma[i] for i in odd_indices],
             fmt='none', ecolor='red', zorder=20)

# Plot lines for even points with lower zorder
plt.plot([num_sites[i] for i in even_indices], [theta_means[i] for i in even_indices], '-', color='blue', linewidth=1, zorder=10)

# Error bars for even points with higher zorder
plt.errorbar([num_sites[i] for i in even_indices],
             [theta_means[i] for i in even_indices],
             yerr=[theta_errors_3sigma[i] for i in even_indices],
             fmt='none', ecolor='red', zorder=20)

#empty graph for labeling
plt.errorbar(0,0, yerr = 0, color = 'green', ecolor='red', label = r'Even $N$ values')
plt.errorbar(0,0, yerr = 0, color = 'blue', ecolor='red', label = r'Odd $N$ values')

plt.scatter(num_sites, theta_analytical, label=r'Theoretical $\overline{\theta}_N$', marker='o',facecolors='none',  edgecolors = 'blue')

plt.axhline(y=theta, color='black', linestyle=':')
plt.text(x=20,  
         y=theta+0.003,  
         s=r'$\overline{\theta}_\infty$', 
         fontsize=12)

plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

plt.xlim(0, 22)
plt.ylim(0.23, 0.33)

x_ticks = plt.gca().get_xticks()
y_ticks = plt.gca().get_yticks()
print(y_ticks)

plt.gca().set_xticklabels(['{:.0f}'.format(x_ticks[0]), '', '{:.0f}'.format(x_ticks[2]), '', '{:.0f}'.format(x_ticks[4])])
plt.gca().set_yticklabels(['{:.2f}'.format(y_ticks[0]), '{:.2f}'.format(y_ticks[1]), '', '{:.2f}'.format(y_ticks[3]), '', '{:.2f}'.format(y_ticks[5])])

plt.rcParams['font.size'] = 12  

plt.xlabel(r'Number of sites $N$', fontsize = 12)
plt.ylabel(r'$\overline{\theta}_N$  ', rotation='horizontal', fontsize = 12, labelpad=7)
plt.legend(loc='lower right')

plt.tight_layout()
plt.grid(True)
plt.savefig('terminal_1d_even_odd.png', format='png', dpi=300)
plt.show()

