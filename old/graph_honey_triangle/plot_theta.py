from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
# Redefine symbols
m, j, k = symbols('m j k', integer=True)
k_value = 5

# Create lists to store the results
tri_theta_2m_plus_1_results = []
hex_theta_2m_plus_1_results = []
theta_from_res_results = []
product_values = []  # This will store the product of x and y
hex_theta_means = []  # Store the mean of theta values
hex_theta_errors = []
tri_theta_means = []
tri_theta_errors = []
is_bipartite=[]

N_values = list(range(3, 50, 1))
for x in range(2, 6):
    for y in range(2, 6):
        product = x * y * 2
        product_values.append(product)
        N = product  # Assuming N is the product of x and y
        m_value = N / 2
        #if x %2 ==1 or y %2 ==1:
        tri_numerator_sum = Sum((m - j) * binomial(2*m, 2*j) / k**(m-j), (j, 0, m))
        tri_denominator_sum = Sum(binomial(2*m, 2*j) / k**(m-j), (j, 0, m))
        tri_theta_2m_plus_1_expr = 1 / m * (tri_numerator_sum / tri_denominator_sum)
        
        tri_theta_2m_plus_1_simplified = tri_theta_2m_plus_1_expr.subs({m: m_value, k: k_value})
        tri_theta_2m_plus_1 = tri_theta_2m_plus_1_simplified.doit().evalf()
        tri_theta_2m_plus_1_results.append(tri_theta_2m_plus_1)
       

        hex_numerator_sum = Sum((m - j) * binomial(m, j)**2 / k**(m-j), (j, 0, m))
        hex_denominator_sum = Sum(binomial(m, j)**2 / k**(m-j), (j, 0, m))
        hex_theta_2m_plus_1_expr = 2 / (m*2) * (hex_numerator_sum / hex_denominator_sum)

        hex_theta_2m_plus_1_simplified = hex_theta_2m_plus_1_expr.subs({m: m_value, k: k_value})
        hex_theta_2m_plus_1 = hex_theta_2m_plus_1_simplified.doit().evalf()
        hex_theta_2m_plus_1_results.append(hex_theta_2m_plus_1)

 
        with open('./hon_{}_{}_av_sur_coverage.txt'.format(x, y)) as f:
            f.readline()  # Skip the first row
            theta_values = [float(line) for line in f]  # Assuming the second column is theta

            theta_mean = sum(theta_values) / len(theta_values)

            sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
            standard_error = ((sample_variance / len(theta_values)) ** 0.5)
            hex_theta_means.append(theta_mean)
            hex_theta_errors.append(standard_error)

        with open('./tri_{}_{}_av_sur_coverage.txt'.format(x, y)) as f:
            f.readline()  # Skip the first row
            theta_values = [float(line) for line in f]  # Assuming the second column is theta

            theta_mean = sum(theta_values) / len(theta_values)

            sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
            standard_error = ((sample_variance / len(theta_values)) ** 0.5)
            tri_theta_means.append(theta_mean)
            tri_theta_errors.append(standard_error)
 

hex_theta_errors_2sigma = [error * 2 for error in hex_theta_errors]
tri_theta_errors_2sigma = [error * 2 for error in tri_theta_errors]

theta = 1/(1+math.sqrt(5))
# Plot the graph
plt.figure(figsize=(4.5, 3))

bipartite_product_values = []
bipartite_theta_means = []
bipartite_theta_errors= []
nonbipartite_product_values = []
nonbipartite_theta_means = []
nonbipartite_theta_errors= []

for i in range(len(product_values)):
    bipartite_product_values.append(product_values[i])
    bipartite_theta_means.append(hex_theta_means[i])
    bipartite_theta_errors.append(hex_theta_errors_2sigma[i])
    nonbipartite_product_values.append(product_values[i])
    nonbipartite_theta_means.append(tri_theta_means[i])
    nonbipartite_theta_errors.append(tri_theta_errors_2sigma[i])
               
zipped_bipartite = zip(bipartite_product_values, bipartite_theta_means, bipartite_theta_errors)
sorted_bipartite = sorted(zipped_bipartite)
bipartite_product_values, bipartite_theta_means, bipartite_theta_errors = zip(*sorted_bipartite)

# Sort the non-bipartite lists
zipped_nonbipartite = zip(nonbipartite_product_values, nonbipartite_theta_means, nonbipartite_theta_errors)
sorted_nonbipartite = sorted(zipped_nonbipartite)
nonbipartite_product_values, nonbipartite_theta_means, nonbipartite_theta_errors = zip(*sorted_nonbipartite)

# Convert zipped lists back to lists
bipartite_product_values = list(bipartite_product_values)
bipartite_theta_means = list(bipartite_theta_means)
bipartite_theta_errors = list(bipartite_theta_errors)

nonbipartite_product_values = list(nonbipartite_product_values)
nonbipartite_theta_means = list(nonbipartite_theta_means)
nonbipartite_theta_errors = list(nonbipartite_theta_errors)
 
#plt.errorbar(nonbipartite_product_values, nonbipartite_theta_means, yerr=nonbipartite_theta_errors, fmt='-', label='Triangular case', ecolor='red', color='orange')

# Plot for bipartite values
#plt.errorbar(bipartite_product_values, bipartite_theta_means, yerr=bipartite_theta_errors, fmt='-', label='Hexagonal case', ecolor='blue', color='green')
# Assuming 'odd_indices' and 'even_indices' are defined somewhere above this code
plt.plot(nonbipartite_product_values, nonbipartite_theta_means, '-',  color='green', linewidth=1, zorder=10)

# Error bars for the "Triangular case" with higher zorder
plt.errorbar(nonbipartite_product_values, nonbipartite_theta_means, yerr=nonbipartite_theta_errors, fmt='none', ecolor='red', zorder=20)

# Plot lines and error bars for the "Hexagonal case"

# Plot lines for the "Hexagonal case" with lower zorder
plt.plot(bipartite_product_values, bipartite_theta_means, '-', color='blue', linewidth=1, zorder=10)

# Error bars for the "Hexagonal case" with higher zorder
plt.errorbar(bipartite_product_values, bipartite_theta_means, yerr=bipartite_theta_errors, fmt='none', ecolor='red', zorder=20)

plt.errorbar(0,0, yerr = 0, color = 'green', ecolor='red', label = r'triangular lattice')
plt.errorbar(0,0, yerr = 0, color = 'blue', ecolor='red', label = r'honeycomb lattice')


#plt.scatter(product_values, theta_from_res_results, label='Theta from Simulation', marker='x')
#plt.scatter(product_values, hex_theta_2m_plus_1_results, label=r'Theoretical $\overline{\theta}_N$', marker='o', facecolors='none', edgecolors='blue')

#plt.scatter(product_values, tri_theta_2m_plus_1_results, marker='o',facecolors='none',  edgecolors = 'blue')

#plt.axhline(y=theta, color='purple', linestyle='--', label=r'$\overline{\theta}_\infty$')
plt.axhline(y=theta, color='black', linestyle=':')
#plt.axhline(y=theta, color='purple', linestyle='--', label=r'$\overline{\theta}_\infty$')
plt.text(x=51,
         y=theta+0.003,
         s=r'$\overline{\theta}_\infty$',
#         va='bottom',
#         ha='right',
#         color='black',
         fontsize=12)

plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

plt.xlim(0, int(max(product_values)*1.1))

plt.ylim(0.23, 0.33)

# Set labels for both axes. Assuming you want to manually set labels at specific positions
# For demonstration, setting labels at the first, middle, and last ticks
x_ticks = plt.gca().get_xticks()
y_ticks = plt.gca().get_yticks()
print(y_ticks)

plt.gca().set_xticklabels(['{:.0f}'.format(x_ticks[0]), '', '{:.0f}'.format(x_ticks[2]), '', '{:.0f}'.format(x_ticks[4])])
plt.gca().set_yticklabels(['', '{:.2f}'.format(y_ticks[1]), '', '{:.2f}'.format(y_ticks[3]), '', '{:.2f}'.format(y_ticks[5])])

plt.rcParams['font.size'] = 12  # You can adjust this size as needed


plt.xlabel(r'Number of sites $N$', fontsize = 12)
plt.ylabel(r'$\overline{\theta}_N$  ', rotation='horizontal', fontsize = 12, labelpad=7)
#plt.title(r'$\overline{\theta}_N$ vs $N$ for honeycomb case and triangular case')
plt.legend(loc='lower right')


plt.tight_layout()
#plt.legend(fontsize='large')  # You can also use specific sizes like 14, 16 etc.
plt.grid(True)
plt.savefig('triangular_vs_honeycomb.png', format='png', dpi=300)
plt.show()
