import matplotlib.pyplot as plt

# Open the file in read mode
with open("../ode_params.txt", "r") as file:
    lines = file.readlines()

lines = lines[1::2]
print(lines)
# Initializing lists to store x and y values
x_values = []  # This will store Rt values
y_values1 = []  # This will store k values
y_values2 = []
infection_rate= 0
# Extracting Rt and k values from the file
for line in lines:
    values = line.strip().split()
    x_values.append(float(values[3]))  
    y_values1.append(float(values[4]))  
    y_values2.append(float(values[6]))  
    infection_rate = float(values[0]) 


# Creating the plots
plt.plot(x_values, y_values1, label="Method 1 (Least Squares)", color='blue', linewidth=2)
plt.plot(x_values, y_values2, label="Method 2 (Contact number)", color='red', linewidth=2)  # Changed label to S_inf

# Adding a dashed black line at y=0.6 and label it "Expected b value"
plt.axhline(y=infection_rate, color='black', linestyle='--', label=r"$\bf{%s}$" % u"\u03B2")

# Adding labels and title with larger font sizes
plt.xlabel(r"$\bf{%s}$" % u"\u03B3", fontsize=16)
plt.ylabel("Optimal "+r"$\bf{%s}$" % "b" +" Value", fontsize=16)
plt.title("Relationship between " + r"$\bf{%s}$" % u"\u03B3" + " and optimal "+r"$\bf{%s}$" % "b" +" value using \ntwo methods, when " + r"$\bf{%s}$" % u"\u03B2" + " = 0.6", fontsize=20)
plt.legend(fontsize=14)

# Increase tick label size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Displaying the plot
plt.tight_layout()
plt.show()


