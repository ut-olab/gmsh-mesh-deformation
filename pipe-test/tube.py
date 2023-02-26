import gmsh
import sys
import math
import numpy as np

gmsh.initialize(sys.argv)
gmsh.model.add("Tube boundary layer")

gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)
order2 = False

c1 = gmsh.model.occ.addCylinder(x=0, y=0, z=0, dx=5, dy=0, dz=0, r=0.5)
# c2 = gmsh.model.occ.addCylinder(2,0,-2, 0,0,2, 0.3)
# s = gmsh.model.occ.fuse([(3, c1)], [(3, c2)])
gmsh.model.occ.remove(gmsh.model.occ.getEntities(3))
gmsh.model.occ.remove([(2,2), (2,3), (2,5)]) # fixme: automate this
gmsh.model.occ.synchronize()

gmsh.model.occ.synchronize()

gmsh.option.setNumber('Geometry.ExtrudeReturnLateralEntities', 0)
n = np.linspace(1, 1, 5)
d = np.logspace(-3, -1, 5)
print(d)
e = gmsh.model.geo.extrudeBoundaryLayer(dimTags=gmsh.model.getEntities(2), numElements=n, heights=-d, recombine=True)

top_ent = [s for s in e if s[0]==2]
top_surf = [s[1] for s in top_ent]
gmsh.model.geo.synchronize()
bnd_ent = gmsh.model.getBoundary(top_ent)
bnd_curv = [c[1] for c in bnd_ent]

loops = gmsh.model.geo.addCurveLoops(bnd_curv)
for l in loops:
    print(l)
    top_surf.append(gmsh.model.geo.addPlaneSurface([l]))

gmsh.model.geo.addVolume([gmsh.model.geo.addSurfaceLoop(top_surf)])
gmsh.model.geo.synchronize()

# gmsh.model.mesh.setTransfiniteCurve(tag=1, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=2, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=3, numNodes=21, meshType="Progression", coef=1.0)

# gmsh.model.mesh.setTransfiniteSurface(tag=2)
# gmsh.model.mesh.setTransfiniteSurface(tag=3)
# gmsh.model.mesh.setTransfiniteVolume(tag=1, cornerTags=[1, 2, 3, 4, 5, 6])

gmsh.model.mesh.generate(3)

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
