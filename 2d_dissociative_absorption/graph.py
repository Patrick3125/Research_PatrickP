import matplotlib.pyplot as plt

x_values = []
y_values = []

with open("log.spparks", "r") as f:
    lines = f.readlines()[81:]
    
    start_from = True
    for line in lines:
        if "- nreaction = 0" in line:
            start_from = True
            continue
        if start_from and line.split()[0] == "Loop":
            start_from = False
            continue
        if start_from:
            x_values.append(float(line.split()[0]))
            y_values.append(float(line.split()[6]))

# Plotting
plt.plot(x_values, y_values, '-')
plt.xlabel('X-Value')
plt.ylabel('Y-Value')
plt.title('Graph from log.spparks')
plt.grid(True)
plt.show()

