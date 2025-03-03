import numpy as np
import sys

if len(sys.argv) != 4:
    print("Usage: python %s xhi yhi site_file" % sys.argv[0])
    sys.exit()

xhi = int(sys.argv[1])      # Number of cells in x-dir
yhi = int(sys.argv[2])      # Number of cells in y-dir
filename = sys.argv[3]      # Output filename

# define variables

a1 = 1.             # Spacing in x-dir for image output
a2 = 1.             # Spacing in y-dir for image output
nsites = xhi * yhi  # Total number of sites

outfile = open(filename, "w")

outfile.write("Site file written by {}\n\n".format(sys.argv[0]))
outfile.write("{} sites\n".format(nsites))
outfile.write("{} max neighbors\n".format(4))
outfile.write("id site values\n\n")

outfile.write("Sites\n\n")

for j in range(0, yhi):
    for i in range(1, xhi + 1):
        outfile.write("{} {} {} 0.0\n".format(i + j * xhi, a1 * (i - 1), a2 * j))

outfile.write("\n")

outfile.write("Neighbors\n\n")
for j in range(0, yhi):
    for i in range(1, xhi + 1):
        site_id = i + j * xhi
        neighbors = []

        # Up and down neighbors with periodic boundary
        top_neighbor = site_id - xhi if j > 0 else site_id + (yhi - 1) * xhi
        bottom_neighbor = site_id + xhi if j < yhi - 1 else site_id - (yhi - 1) * xhi
        neighbors.extend([top_neighbor, bottom_neighbor])

        # Left and right neighbors with periodic boundary
        left_neighbor = site_id - 1 if i > 1 else site_id + (xhi - 1)
        right_neighbor = site_id + 1 if i < xhi else site_id - (xhi - 1)
        neighbors.extend([left_neighbor, right_neighbor])

        # Write neighbors to file
        outfile.write("{} {}\n".format(site_id, ' '.join(map(str, neighbors))))

outfile.close()

print("%s generated" % filename)

