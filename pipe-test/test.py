import gmsh
import math
import sys
import numpy as np

gmsh.initialize(sys.argv)

gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
gmsh.option.setNumber("Mesh.VolumeFaces", 1)
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
numberOfLayerOfLongitudinal = 10
N = 10
r = 1.1
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

gmsh.model.geo.synchronize()
l = gmsh.model.getEntities(1)
print(l)
extbl = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(1), [1] * N, d, True)
print(extbl)

gmsh.model.geo.synchronize()

test = [9, 13, 17, 21]
gmsh.model.geo.addCurveLoop(curveTags=test, tag=100)

gmsh.model.geo.addPlaneSurface(wireTags=[100], tag=100)
gmsh.model.geo.synchronize()

# test = [(2, 12), (2, 16), (2, 20), (2, 24), (2, 100)]
test = [(2, 100)]
# test = [(1, 9), (1, 13), (1, 17), (1, 21)]
gmsh.model.geo.extrude(dimTags=test, dx=0, dy=0, dz=length, numElements=[numberOfLayerOfLongitudinal])
gmsh.model.geo.synchronize()

# gmsh.model.mesh.setRecombine(dim=2, tag=100)

gmsh.model.mesh.generate(2)
print("finish meshing")

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("circle-boundary-3d.msh")
gmsh.write("circle-boundary-3d.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
