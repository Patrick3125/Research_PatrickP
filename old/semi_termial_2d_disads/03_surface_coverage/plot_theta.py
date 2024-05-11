from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt
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

N_values = list(range(3, 101, 1))
for x in range(3, 10):
    for y in range(3, 11):
        product = x * y
        product_values.append(product)

        N = product  # Assuming N is the product of x and y
        #if N % 2 == 1:
        if x %2 ==1:
            m_value = (N - 1) / 2  # Use integer division for m_value
#            numerator_sum = Sum((m - j) * binomial(m+1, (m-j))*binomial(m, j) / k**(m-j), (j, 0, m))
#            denominator_sum = Sum(binomial(m+1, (m-j)) * binomial(m,j) / k**(m-j), (j, 0, m))
#            theta_2m_plus_1_expr = 2 / (m*2+1) * (numerator_sum / denominator_sum)

            numerator_sum = Sum((m - j) * binomial(2*m+1, 2*(m-j)) / k**(m-j), (j, 0, m))
            denominator_sum = Sum(binomial(2*m+1, 2*(m-j)) / k**(m-j), (j, 0, m))
            theta_2m_plus_1_expr = 2 / (m*2+1) * (numerator_sum / denominator_sum)
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
            theta_values = [float(line.split()[1]) for line in f]  # Assuming the second column is theta
            theta_mean = np.mean(theta_values)
            theta_std = np.std(theta_values)  # Standard deviation as the error
            
            theta_means.append(theta_mean)
            theta_errors.append(theta_std)               
 

theta = 1/(1+math.sqrt(5))
# Plot the graph
plt.figure(figsize=(10, 5))
plt.errorbar(product_values, theta_means, yerr=theta_errors, fmt='x', label='Theta from Simulation', ecolor = 'orange', color = 'orange')
#plt.scatter(product_values, theta_from_res_results, label='Theta from Simulation', marker='x')
plt.scatter(product_values, theta_2m_plus_1_results, label='Theoretical Theta', marker='o',facecolors='none',  edgecolors = 'blue')

plt.axhline(y=theta, color='purple', linestyle='--', label='theta')
plt.xlabel('Product of x and y')
plt.ylabel('Theta')
plt.title('Theta values for product of x and y')
plt.legend()
plt.grid(True)
plt.show()
