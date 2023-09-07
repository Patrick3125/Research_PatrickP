import numpy as np
import sys

if len(sys.argv)!=3:
  print("Usage: python %s xhi yhi" % sys.argv[0])
  sys.exit()

xhi = int(sys.argv[1])
yhi = int(sys.argv[2])

a1 = 1. 
a2 = 1. 

nsites = xhi*yhi

file_name = "data.strips"
site_file = open(file_name,"w")


site_file.write("Site file written by create_site_file.py\n\n")
# site_file.write("{} dimension\n".format(2))
site_file.write("{} sites\n".format(nsites))
site_file.write("{} max neighbors\n".format(4))
site_file.write("id site values\n\n")

site_file.write("Sites\n\n")

for j in range(0,yhi):
    for i in range(1,xhi+1):
        site_file.write("{} {} {} 0.0\n".format(i + j*xhi,a1*(i-1),a2*j))

m = xhi

site_file.write("\n")
site_file.write("Neighbors\n\n")

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

        site_file.write("{} {} {} {} {}\n".format(site_id, neigh1, neigh2, neigh3, neigh4))

site_file.close()

print("%s generated" % file_name)
