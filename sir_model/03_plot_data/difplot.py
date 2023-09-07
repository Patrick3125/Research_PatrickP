import matplotlib.pyplot as plt

# Open the file in read mode
with open("diffrate.txt", "r") as file:
    lines = file.readlines()

# Initializing lists to store x and y values
x_values = []
y_values1 = []
y_values2 = []

i = 0
while i < len(lines):
    # This line is a x-value
    x = float(lines[i].strip())
    i += 1

    y1_values = []
    y2_values = []
    # Continue reading the following lines until we reach another x-value (or the end of the file)
    while i < len(lines) and ' ' in lines[i]:
        line = lines[i].strip().split()
        y1 = float(line[0])
        y2 = float(line[2])  # Changed to second value in line
        y1_values.append(y1)
        y2_values.append(y2)

        # Plot individual data points in a lighter color
        # Commented out as per request
        plt.scatter(x, y1, color='lightblue', alpha=0.3, s=10)
        plt.scatter(x, y2, color='salmon', alpha=0.3, s=10)
        i += 1

    # Append the averages to the respective lists
    x_values.append(x)
    y_values1.append(sum(y1_values) / len(y1_values))  # Average over all values
    y_values2.append(sum(y2_values) / len(y2_values))  # Average over all values

# Creating the plots
plt.plot(x_values, y_values1, label="Mean Squared", color='blue', linewidth=2)
plt.plot(x_values, y_values2, label="Using S_inf", color='red', linewidth=2)  # Changed label to S_inf

# Adding labels and title with larger font sizes
plt.xlabel("Diffusion Rate", fontsize=16)
plt.ylabel("Optimal B Value", fontsize=16)
plt.title("Optimal B Value with Different Diffusion Rates", fontsize=20)
plt.legend(fontsize=14)

# Increase tick label size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Displaying the plot
plt.tight_layout()
plt.show()

