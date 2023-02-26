import gmsh
import math
import sys
import numpy as np

gmsh.initialize(sys.argv)

gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
# gmsh.option.setNumber("Mesh.VolumeFaces", 1)
gmsh.option.setNumber("Mesh.Lines", 1)
gmsh.option.setNumber("Geometry.Points", 1)
gmsh.option.setNumber("Geometry.Curves", 1)
gmsh.option.setNumber("Geometry.Surfaces", 1)
gmsh.option.setNumber("Geometry.Volumes", 1)
gmsh.option.setNumber("Geometry.PointLabels", 1)
gmsh.option.setNumber("Geometry.CurveLabels", 1)
gmsh.option.setNumber("Geometry.SurfaceLabels", 1)
gmsh.option.setNumber("General.MouseInvertZoom", 1)
gmsh.option.setNumber("Mesh.LineWidth", 4)
gmsh.option.setNumber("Mesh.OptimizeThreshold", 0.1)
gmsh.option.setNumber("General.Axes", 3)
gmsh.option.setNumber("General.Trackball", 0)
gmsh.option.setNumber("General.RotationX", 0)
gmsh.option.setNumber("General.RotationY", 0)
gmsh.option.setNumber("General.RotationZ", 0)
gmsh.option.setNumber("General.Terminal", 1)

radius = 0.5
length = 1.0
numberOfTest = 10
N = 5
r = 1.2
d = [-0.01]
for i in range(1, N):
    d.append(d[-1] - (-d[0]) * r ** i)

center = gmsh.model.geo.addPoint(x=0,y=0,z=0,tag=0)
gmsh.model.geo.addPoint(x=math.cos(math.pi*0)*radius, y=math.sin(math.pi*0)*radius, z=0, tag=1)
gmsh.model.geo.addPoint(x=math.cos(math.pi/2)*radius, y=math.sin(math.pi/2)*radius, z=0, tag=2)
gmsh.model.geo.addPoint(x=math.cos(math.pi*1)*radius, y=math.sin(math.pi*1)*radius, z=0, tag=3)
gmsh.model.geo.addPoint(x=math.cos(math.pi*3/2)*radius, y=math.sin(math.pi*3/2) * radius, z=0, tag=4)

# gmsh.model.geo.addLine(startTag=center, endTag=1, tag=1)
# gmsh.model.geo.addLine(startTag=center, endTag=2, tag=2)
# gmsh.model.geo.addLine(startTag=center, endTag=3, tag=3)
# gmsh.model.geo.addLine(startTag=center, endTag=4, tag=4)
gmsh.model.geo.addCircleArc(startTag=1, centerTag=center, endTag=2, tag=5)
gmsh.model.geo.addCircleArc(startTag=2, centerTag=center, endTag=3, tag=6)
gmsh.model.geo.addCircleArc(startTag=3, centerTag=center, endTag=4, tag=7)
gmsh.model.geo.addCircleArc(startTag=4, centerTag=center, endTag=1, tag=8)

test = [(1, 5), (1, 6), (1, 7), (1, 8)]
gmsh.model.geo.extrude(test, dx=0, dy=0, dz=length)

gmsh.model.geo.synchronize()

s = gmsh.model.getEntities(2)
print(s)

extbl = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), [1] * N, d, True)
print(extbl)

gmsh.model.geo.synchronize()


# ここよくわからんな
top = []
for i in range(1, len(extbl)):
    print(extbl[i], extbl[i][0])
    if extbl[i][0] == 3:
        top.append(extbl[i - 1])

bnd = gmsh.model.getBoundary(top)
print("top = ", top)
print("bnd = ", bnd)
cl2 = gmsh.model.geo.addCurveLoop([c[1] for c in bnd])
print("cl2 = ", cl2)
# s2 = gmsh.model.geo.addPlaneSurface([cl2])
# sl = gmsh.model.geo.addSurfaceLoop([s2])
# print("s2 = ", s2)
# v = gmsh.model.geo.addVolume([sl])

gmsh.model.geo.synchronize()

l = gmsh.model.getEntities(1)
for i in l:
    # print(i)
    gmsh.model.mesh.setTransfiniteCurve(tag=i[1], numNodes=21, meshType="Progression", coef=1.0)

gmsh.model.mesh.setTransfiniteSurface(tag=12)
gmsh.model.mesh.setTransfiniteSurface(tag=16)
gmsh.model.mesh.setTransfiniteSurface(tag=20)
gmsh.model.mesh.setTransfiniteSurface(tag=24)
gmsh.model.mesh.setRecombine(dim=2, tag=12)
gmsh.model.mesh.setRecombine(dim=2, tag=16)
gmsh.model.mesh.setRecombine(dim=2, tag=20)
gmsh.model.mesh.setRecombine(dim=2, tag=24)



gmsh.model.mesh.generate(3)
print("finish meshing")

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("circle.msh")
gmsh.write("circle.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
