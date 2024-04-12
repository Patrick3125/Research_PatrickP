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
is_bipartite=[]

N_values = list(range(3, 101, 1))
for x in range(3, 10):
    for y in range(3, 11):
        product = x * y
        product_values.append(product)
        is_bipartite.append(True)
        N = product  # Assuming N is the product of x and y
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
        
        with open('../res_{}_{}'.format(x, y) + '/average_surface_coverage.txt') as f:
            f.readline()  # Skip the first row
            theta_values = [float(line) for line in f]  # Assuming the second column is theta

            theta_mean = sum(theta_values) / len(theta_values)

            sample_variance = sum((x - theta_mean) ** 2 for x in theta_values) / (len(theta_values) - 1)
            standard_error = ((sample_variance / len(theta_values)) ** 0.5)
            theta_means.append(theta_mean)
            theta_errors.append(standard_error)
 
theta_errors_2sigma = [error * 2 for error in theta_errors]

print(theta_errors)
theta = 1/(1+math.sqrt(5))
# Plot the graph
plt.figure(figsize=(8, 4))

bipartite_product_values = []
bipartite_theta_means = []
bipartite_theta_errors= []
nonbipartite_product_values = []
nonbipartite_theta_means = []
nonbipartite_theta_errors= []

for i in range(len(product_values)):
    if is_bipartite[i]:
        bipartite_product_values.append(product_values[i])
        bipartite_theta_means.append(theta_means[i])
        bipartite_theta_errors.append(theta_errors_2sigma[i])
    else:
        nonbipartite_product_values.append(product_values[i])
        nonbipartite_theta_means.append(theta_means[i])
        nonbipartite_theta_errors.append(theta_errors_2sigma[i])
               
zipped_bipartite = zip(bipartite_product_values, bipartite_theta_means, bipartite_theta_errors)
sorted_bipartite = sorted(zipped_bipartite)
bipartite_product_values, bipartite_theta_means, bipartite_theta_errors = zip(*sorted_bipartite)

# Sort the non-bipartite lists
#zipped_nonbipartite = zip(nonbipartite_product_values, nonbipartite_theta_means, nonbipartite_theta_errors)
#sorted_nonbipartite = sorted(zipped_nonbipartite)
#nonbipartite_product_values, nonbipartite_theta_means, nonbipartite_theta_errors = zip(*sorted_nonbipartite)

# Convert zipped lists back to lists
bipartite_product_values = list(bipartite_product_values)
bipartite_theta_means = list(bipartite_theta_means)
bipartite_theta_errors = list(bipartite_theta_errors)

#nonbipartite_product_values = list(nonbipartite_product_values)
#nonbipartite_theta_means = list(nonbipartite_theta_means)
#nonbipartite_theta_errors = list(nonbipartite_theta_errors)
 
plt.errorbar(nonbipartite_product_values, nonbipartite_theta_means, yerr=nonbipartite_theta_errors, fmt='x-', label='Theta for Non-bipartite', ecolor='red', color='orange')

# Plot for bipartite values
plt.errorbar(bipartite_product_values, bipartite_theta_means, yerr=bipartite_theta_errors, fmt='x-', label='Theta for Bipartite', ecolor='blue', color='green')


#plt.scatter(product_values, theta_from_res_results, label='Theta from Simulation', marker='x')
plt.scatter(product_values, theta_2m_plus_1_results, label='Theoretical Theta', marker='o',facecolors='none',  edgecolors = 'blue')

plt.axhline(y=theta, color='purple', linestyle='--', label='theta')

plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

plt.xlim(0, int(max(product_values)*1.1))

# Set labels for both axes. Assuming you want to manually set labels at specific positions
# For demonstration, setting labels at the first, middle, and last ticks
x_ticks = plt.gca().get_xticks()
y_ticks = plt.gca().get_yticks()
print(y_ticks)

plt.gca().set_xticklabels(['{:.0f}'.format(x_ticks[0]), '', '{:.0f}'.format(x_ticks[2]), '', '{:.0f}'.format(x_ticks[4])])
plt.gca().set_yticklabels(['{:.2f}'.format(y_ticks[0]), '{:.2f}'.format(y_ticks[1]), '', '{:.2f}'.format(y_ticks[3]), '', '{:.2f}'.format(y_ticks[5])])

plt.rcParams['font.size'] = 18  # You can adjust this size as needed


plt.xlabel('Number of sites')
plt.ylabel('Theta')
plt.title('Theta vs Number of sites for 2d periodic case')
plt.legend(loc='lower right')
#plt.legend(fontsize='large')  # You can also use specific sizes like 14, 16 etc.
plt.grid(True)
plt.show()
