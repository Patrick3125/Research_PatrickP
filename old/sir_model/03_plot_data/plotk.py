import matplotlib.pyplot as plt

# Open the file in read mode
with open("../ode_params.txt", "r") as file:
    lines = file.readlines()

lines = lines[1::2]
print(lines)
# Initializing lists to store x and y values
x_values = []  # This will store Rt values
y_values = []  # This will store k values

# Extracting Rt and k values from the file
for line in lines:
    values = line.strip().split()
    x_values.append(float(values[2]))  # Rt is the second column
    y_values.append(float(values[4]))  # k is the fifth column

# Plotting the data
plt.plot(x_values, y_values, color='#14867B', linewidth=2)
# Adding labels and title with increased font sizes
plt.xlabel("Rt", fontsize=16)
plt.ylabel("k", fontsize=16)
plt.title("Rt and k values", fontsize=20)

# Display the plot
plt.show()

