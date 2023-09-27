import numpy as np
import os

corrdir = "../correlation"
output_file = os.path.join(corrdir, "average_correlation.txt")

# Find correlation files
correlation_files = [f for f in os.listdir(corrdir) if f.startswith('correlation') and f.endswith('.txt')]

# Initialize sum and count for averaging
correlation_sums = None
file_count = 0

# Loop through each correlation file
for file in correlation_files:
    filepath = os.path.join(corrdir, file)
    data = np.loadtxt(filepath)

    # If sums array is not initialized, create one with the same shape as data
    if correlation_sums is None:
        correlation_sums = np.zeros(data.shape)

    # Add the correlations to the sums array (assuming correlations are in the second column)
    correlation_sums[:, 1] += data[:, 1]
    file_count += 1

# Calculate the average
if file_count > 0:
    correlation_sums[:, 1] /= file_count

# Save the average correlations to a file
header_str = "i average_correlation"
np.savetxt(output_file, correlation_sums, fmt="%d %f", header=header_str)

print("Finished writing average correlations to {}".format(output_file))

