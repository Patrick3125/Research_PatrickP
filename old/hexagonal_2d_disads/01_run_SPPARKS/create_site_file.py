import numpy as np
import sys

if len(sys.argv) != 4:
    print("Usage: python %s xhi yhi site_file" % sys.argv[0])
    sys.exit()

xhi = int(sys.argv[1])      # Number of cells in x-dir
yhi = int(sys.argv[2])      # Number of cells in y-dir
filename = sys.argv[3]      # Output filename

# Define variables

a1 = 0.5                     # Spacing in x-dir
a2 = a1 / np.sqrt(3)         # Spacing in y-dir (height of a triangle)
nsites = xhi * yhi * 2      # Total number of sites (2 per rectangle)

# Open output file and write first part

outfile = open(filename, "w")

outfile.write("Site file written by {}\n\n".format(sys.argv[0]))
outfile.write("{} sites\n".format(nsites))
outfile.write("{} max neighbors\n".format(3))
outfile.write("id site values\n\n")

# Write second part (Sites)

outfile.write("Sites\n\n")

for j in range(0, yhi):
    for i in range(1, xhi + 1):
        # Adjust the site positions for a triangular grid
        outfile.write("{} {} {} 0.0\n".format((i + j * xhi) * 2 - 1, a1 * (i - 1) * 2 + j * a1, a2 * j * 3))
        outfile.write("{} {} {} 0.0\n".format((i + j * xhi) * 2, a1 * (i - 0.5) * 2 + j * a1, a2 * j * 3 + a2))

outfile.write("\n")
# Write third part (Neighbors)
outfile.write("Neighbors\n\n")

# Adjusting the neighbor assignment logic
for j in range(yhi):
    for i in range(1, xhi + 1):
        site1_id = (i + j * xhi) * 2 - 1  # lower left side of rhombus
        site2_id = site1_id + 1            # upper right side of rhombus

        # Neighbors for site1
        neighbors1 = [
            site1_id + 1,
            site1_id - 1 if i > 1 else site1_id + xhi * 2 - 1,
            site1_id - xhi * 2 + 1 if j != 0 else site1_id + xhi * (yhi - 1) * 2 + 1,
        ]

        # Neighbors for site2
        neighbors2 = [
            site2_id - 1,
            site2_id + 1 if i < xhi else site2_id - xhi * 2 + 1,
            site2_id + xhi * 2 - 1 if j != yhi - 1 else site2_id - xhi * (yhi - 1) * 2 - 1,
        ]

        neighbors1 = list(set([n for n in neighbors1 if n is not None]))
        neighbors2 = list(set([n for n in neighbors2 if n is not None]))

        # Write neighbors to file
        outfile.write("{} {}\n".format(site1_id, ' '.join(map(str, neighbors1))))
        outfile.write("{} {}\n".format(site2_id, ' '.join(map(str, neighbors2))))
# Close file and print final message
outfile.close()

print("%s generated" % filename)

