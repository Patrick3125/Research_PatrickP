import matplotlib.pyplot as plt

x_values = []
y_values = []

with open("../res/data1.txt", "r") as f:
    lines = f.readlines()[1:]
    for line in lines:    
        x_values.append(float(line.split()[0]))
        y_values.append(float(line.split()[1]))

# Plotting
plt.plot(x_values, y_values, '-')
plt.xlabel('time')
plt.ylabel('coverage')
plt.title('coverage over time')
plt.grid(True)
plt.show()

