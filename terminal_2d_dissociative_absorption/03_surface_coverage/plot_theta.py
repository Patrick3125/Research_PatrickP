from sympy import binomial, symbols, Sum, simplify
import matplotlib.pyplot as plt

# Redefine symbols
m, j, k = symbols('m j k', integer=True)
k_value = 5

# Create lists to store the results
theta_2m_plus_1_results = []
theta_from_res_results = []
N_values = list(range(3, 21, 1))

# Loop over the desired values of N
for N in N_values:
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

    # Calculate theta_2m+1 with substitutions for m and k
    # Simplify the expression with substitutions
    theta_2m_plus_1_simplified = theta_2m_plus_1_expr.subs({m: m_value, k: k_value})

    # Evaluate the expression numerically
    theta_2m_plus_1 = theta_2m_plus_1_simplified.doit().evalf()
    
    # Append to results list
    theta_2m_plus_1_results.append(theta_2m_plus_1)    
    with open('../res_{}/theta.txt'.format(N)) as f:
        f.readline()  # Skip the first row
        theta_from_res = float(f.readline().split()[0])
        theta_from_res_results.append(theta_from_res)

print("0")
# Plot the graph
plt.figure(figsize=(10, 5))
print("1")
plt.plot(N_values, theta_2m_plus_1_results, label='theta_2m_plus_1', marker='o')
print("2")
plt.plot(N_values, theta_from_res_results, label='theta_from_res', marker='x')
plt.xlabel('m value')
plt.ylabel('Theta')
plt.title('Comparison of Theta Values')
plt.legend()
plt.grid(True)
print("3")
plt.show()
