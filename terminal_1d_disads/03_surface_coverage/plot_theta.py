from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
# Redefine symbols
m, j, k = symbols('m j k', integer=True)
k_value = 5

# Create lists to store the results
theta_2m_plus_1_results = []
theta_from_res_results = []
product_values = []  # This will store the product of x and y
theta_means = []  # Store the mean of theta values
theta_errors = []

N_values = list(range(4, 21, 1))

# Loop over the desired values of N
for N in N_values:
    product_values.append(N)
    if N % 2 == 1:
        m_value = (N - 1) / 2  # Use integer division for m_value
        numerator_sum = Sum((m - j) * binomial(m+1, (m-j))*binomial(m, j) / k**(m-j), (j, 0, m))
        denominator_sum = Sum(binomial(m+1, (m-j)) * binomial(m,j) / k**(m-j), (j, 0, m))
        theta_2m_plus_1_expr = 2 / (m*2+1) * (numerator_sum / denominator_sum)

#        numerator_sum = Sum((m - j) * binomial(2*m+1, 2*(m-j)) / k**(m-j), (j, 0, m))
#        denominator_sum = Sum(binomial(2*m+1, 2*(m-j)) / k**(m-j), (j, 0, m))
#        theta_2m_plus_1_expr = 2 / (m*2+1) * (numerator_sum / denominator_sum)
        #numerator_sum = Sum(binomial(2*m, 2*j+1) * k**j, (j, 0, m-1))
        #denominator_sum = Sum(binomial(2*m+1, 2*j+1) * k**j, (j, 0, m))
        #theta_2m_plus_1_expr = (numerator_sum / denominator_sum)

    else:
        m_value = N / 2  # Use integer division for m_value
        numerator_sum = Sum((m - j) * binomial(m, j)**2 / k**(m-j), (j, 0, m))
        denominator_sum = Sum(binomial(m, j)**2 / k**(m-j), (j, 0, m))
        theta_2m_plus_1_expr = 2 / (m*2) * (numerator_sum / denominator_sum)

    theta_2m_plus_1_simplified = theta_2m_plus_1_expr.subs({m: m_value, k: k_value})
    theta_2m_plus_1 = theta_2m_plus_1_simplified.doit().evalf()
    theta_2m_plus_1_results.append(theta_2m_plus_1)


#        with open('../res_{}_{}'.format(x, y) + '/average_surface_coverage.txt') as f:
#            f.readline()  # Skip the first row
#            theta_values = [float(line.split()[1]) for line in f]  # Assuming the second column is theta
#            theta_mean = np.mean(theta_values)
#            theta_std = np.std(theta_values)  # Standard deviation as the error
#            
#            theta_means.append(theta_mean)
#            theta_errors.append(theta_std)               
    with open('../res_{}'.format(N) + '/average_surface_coverage.txt') as f:
        f.readline()  # Skip the first row
        theta_values = [float(line) for line in f]  # Assuming the second column is theta

        theta_mean = sum(theta_values) / len(theta_values)

        sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
        standard_error = ((sample_variance / len(theta_values)) ** 0.5)
        theta_means.append(theta_mean)
        theta_errors.append(standard_error)
 
theta_errors_2sigma = [error * 3 for error in theta_errors]
print(theta_errors)
theta = 1/(1+math.sqrt(5))
# Plot the graph
plt.figure(figsize=(4.5, 3))

odd_indices = range(1, len(product_values), 2)  # Start from 0 for even indices because Python is 0-based
even_indices = range(0, len(product_values), 2)  # Start from 1 for odd indices

plt.plot([product_values[i] for i in odd_indices], [theta_means[i] for i in odd_indices], '-', color='green', linewidth=1, zorder=10)

# Error bars for odd points with higher zorder
plt.errorbar([product_values[i] for i in odd_indices],
             [theta_means[i] for i in odd_indices],
             yerr=[theta_errors_2sigma[i] for i in odd_indices],
             fmt='none', ecolor='red', zorder=20)

# Plot lines for even points with lower zorder
plt.plot([product_values[i] for i in even_indices], [theta_means[i] for i in even_indices], '-', color='blue', linewidth=1, zorder=10)

# Error bars for even points with higher zorder
plt.errorbar([product_values[i] for i in even_indices],
             [theta_means[i] for i in even_indices],
             yerr=[theta_errors_2sigma[i] for i in even_indices],
             fmt='none', ecolor='red', zorder=20)


plt.errorbar(0,0, yerr = 0, color = 'green', ecolor='red', label = r'Even $N$ values')
plt.errorbar(0,0, yerr = 0, color = 'blue', ecolor='red', label = r'Odd $N$ values')



#plt.scatter(product_values, theta_from_res_results, label='Theta from Simulation', marker='x')
plt.axhline(y=theta, color='black', linestyle=':')
#plt.axhline(y=theta, color='purple', linestyle='--', label=r'$\overline{\theta}_\infty$')
plt.text(x=20,
         y=theta+0.003,
         s=r'$\overline{\theta}_\infty$',
#         va='bottom',
#         ha='right',
#         color='black',
         fontsize=12)


plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

plt.xlim(0, 22)
plt.ylim(0.23, 0.33)
# Set labels for both axes. Assuming you want to manually set labels at specific positions
# For demonstration, setting labels at the first, middle, and last ticks
x_ticks = plt.gca().get_xticks()
y_ticks = plt.gca().get_yticks()
print(y_ticks)

plt.gca().set_xticklabels(['{:.0f}'.format(x_ticks[0]), '', '{:.0f}'.format(x_ticks[2]), '', '{:.0f}'.format(x_ticks[4])])
plt.gca().set_yticklabels(['{:.2f}'.format(y_ticks[0]), '{:.2f}'.format(y_ticks[1]), '', '{:.2f}'.format(y_ticks[3]), '', '{:.2f}'.format(y_ticks[5])])

plt.rcParams['font.size'] = 12  # You can adjust this size as needed


plt.xlabel(r'Number of sites $N$', fontsize = 12)
plt.ylabel(r'$\overline{\theta}_N$  ', rotation='horizontal', fontsize = 12, labelpad=7)
#plt.title(r'$\overline{\theta}_N$ vs $N$ for honeycomb case and triangular case')
plt.legend(loc='lower right')
plt.tight_layout()
plt.grid(True)
plt.savefig('terminal_1d_even_odd.png', format='png', dpi=300)

plt.show()
