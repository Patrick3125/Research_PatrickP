import numpy as np
import sys

# command line input

if len(sys.argv)!=4:
  print("Usage: python %s xhi yhi site_file" % sys.argv[0])
  sys.exit()

xhi = int(sys.argv[1])      # number of cells in x-dir
yhi = int(sys.argv[2])      # number of cells in y-dir
filename = sys.argv[3]      # output filename

# define variables

a1 = 1.             # spacing in x-dir
a2 = 1.             # spacing in y-dir
nsites = xhi*yhi    # total number of sites

# open output file and write first part

outfile = open(filename,"w")

outfile.write("Site file written by {}\n\n".format(sys.argv[0]))
outfile.write("{} sites\n".format(nsites))
outfile.write("{} max neighbors\n".format(4))
outfile.write("id site values\n\n")

# write second part (Sites)

outfile.write("Sites\n\n")

for j in range(0,yhi):
    for i in range(1,xhi+1):
        outfile.write("{} {} {} 0.0\n".format(i + j*xhi,a1*(i-1),a2*j))

outfile.write("\n")

# write third part (Neighbors)

outfile.write("Neighbors\n\n")

for j in range(0, yhi):
    for i in range(1, xhi+1):
        site_id = i + j*xhi
        # Up and down neighbors
        neigh1 = site_id - xhi
        if neigh1 <= 0:
            neigh1 += nsites

        neigh2 = site_id + xhi
        if neigh2 > nsites:
            neigh2 -= nsites
            
        # Left and right neighbors
        neigh3 = site_id - 1
        if i == 1:  # If on the left edge of a strip
            neigh3 += xhi

        neigh4 = site_id + 1
        if i == xhi:  # If on the right edge of a strip
            neigh4 -= xhi

        outfile.write("{} {} {} {} {}\n".format(site_id, neigh1, neigh2, neigh3, neigh4))

# close file and print final message

outfile.close()

print("%s generated" % filename)
