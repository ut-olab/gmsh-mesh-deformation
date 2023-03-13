import gmsh
import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " file")
    exit

gmsh.initialize()

gmsh.open(sys.argv[1])
gmsh.open(sys.argv[2])

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
