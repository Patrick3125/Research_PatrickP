import numpy as np
import sys

# command line input

if len(sys.argv) != 4:
    print("Usage: python %s xhi yhi site_file" % sys.argv[0])
    sys.exit()

xhi = int(sys.argv[1])      # number of cells in x-dir
yhi = int(sys.argv[2])      # number of cells in y-dir
filename = sys.argv[3]      # output filename

# define variables

a1 = 1.             # spacing in x-dir
a2 = 2.             # spacing in y-dir
nsites = xhi * yhi  # total number of sites

# open output file and write first part

outfile = open(filename, "w")

outfile.write("Site file written by {}\n\n".format(sys.argv[0]))
outfile.write("{} sites\n".format(nsites))
outfile.write("{} max neighbors\n".format(2))
outfile.write("id site values\n\n")

# write second part (Sites)

outfile.write("Sites\n\n")

for j in range(0, yhi):
    for i in range(1, xhi + 1):
        outfile.write("{} {} {} 0.0\n".format(i + j * xhi, a1 * (i - 1), a2 * j))

outfile.write("\n")

# write third part (Neighbors)

outfile.write("Neighbors\n\n")


for j in range(0, yhi):
    for i in range(1, xhi + 1):
        site_id = i + j * xhi
        # For each site, the right neighbor is the next site in the x-direction
        #right_neighbor = site_id + 1
        # For each site, the left neighbor is the previous site in the x-direction
        #left_neighbor = site_id - 1
        
        # If it's the first site in the row, wrap around to the last site
        #if i == 1:
        #    left_neighbor += xhi
        # If it's the last site in the row, wrap around to the first site
        #if i == xhi:
        #    right_neighbor -= xhi 
        #outfile.write("{} {} {}\n".format(site_id, left_neighbor, right_neighbor))

        neighbors = []
        if i > 1:  # has left neighbor
            neighbors.append(site_id - 1)
        if i < xhi:  # has right neighbor
            neighbors.append(site_id + 1)
        # Write neighbors if they exist
        outfile.write("{} {}\n".format(site_id, ' '.join(map(str, neighbors))))


# close file and print final message

outfile.close()

print("%s generated" % filename)

