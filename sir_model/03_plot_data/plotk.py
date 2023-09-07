import matplotlib.pyplot as plt

# Open the file in read mode
with open("diffrate.txt", "r") as file:
    lines = file.readlines()

# Initializing lists to store x and y values
x_values = []
y_values1 = []

i = 0
while i < len(lines):
    # This line is a x-value
    x = float(lines[i].strip())
    i += 1

    y_values = []
    # Continue reading the following lines until we reach another x-value (or the end of the file)
    while i < len(lines) and ' ' in lines[i]:
        line = lines[i].strip().split()
        y1 = float(line[1])
        y_values.append(y1)
        
        # Plot individual data points in a lighter color
        plt.plot(x, y1, marker='o', markersize=10, linestyle='', alpha=0.3, color='lightblue')
        i += 1

    # Append the averages to the respective lists
    x_values.append(x)
    y_values1.append(sum(y_values) / len(y_values))  # Average over all values

# Creating the plots
plt.plot(x_values, y_values1, color='#14867B', linewidth=2)

# Adding labels and title with increased font sizes
plt.xlabel("Recovery Rate", fontsize=16)
plt.ylabel("Optimal k value", fontsize=16)
plt.title("Recovery Rate and Optimal K value", fontsize=20)

# Increasing the size of the legend and the ticks
#plt.legend(fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Making the grid visible for better readability
#plt.grid(True)

# Optionally, you can also increase the figure size for better visibility
#plt.figure(figsize=(10, 6))
plt.subplots_adjust(bottom=0.15)

# Displaying the plot
plt.show()

