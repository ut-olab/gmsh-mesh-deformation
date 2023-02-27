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
numberOfLayerOfLongitudinal = 50
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

test = [(1, 5), (1, 6), (1, 7), (1, 8)]
gmsh.model.geo.extrude(dimTags=test, dx=0, dy=0, dz=length, numElements=[numberOfLayerOfLongitudinal])


gmsh.model.geo.synchronize()

extbl = gmsh.model.geo.extrudeBoundaryLayer(gmsh.model.getEntities(2), [1] * N, d, True)
print(extbl)

gmsh.model.geo.synchronize()

# 46 68 90 112
# test = [48, 68, 90, 112]
# gmsh.model.geo.addSurfaceLoop(test, 10)
# s = gmsh.model.getEntities(3)
# print("s = ", s)

# ここよくわからんな
top = []
for i in range(1, len(extbl)):
    print(extbl[i], extbl[i][0])
    if extbl[i][0] == 3:
        top.append(extbl[i - 1])

# bnd = gmsh.model.getBoundary(top)
# print("top = ", top)
# print("bnd = ", bnd)
# cl2 = gmsh.model.geo.addCurveLoop([c[1] for c in bnd])
# print("cl2 = ", cl2)
# s2 = gmsh.model.geo.addPlaneSurface([cl2])
# sl = gmsh.model.geo.addSurfaceLoop([s2])
# print("s2 = ", s2)

# v = gmsh.model.geo.addVolume([sl])

# gmsh.model.geo.addLine(startTag=17, endTag=27, tag=1000)
gmsh.model.geo.addLine(startTag=center, endTag=6, tag=1000)

gmsh.model.geo.addLine(startTag=center, endTag=17, tag=1001)
gmsh.model.geo.addLine(startTag=center, endTag=18, tag=1002)
gmsh.model.geo.addLine(startTag=center, endTag=32, tag=1003)
gmsh.model.geo.addLine(startTag=center, endTag=41, tag=1004)
gmsh.model.geo.addCurveLoop([1001, 26, -1002], 2001)
gmsh.model.geo.addCurveLoop([1002, 48, -1003], 2002)
gmsh.model.geo.addCurveLoop([1003, 70, -1004], 2003)
gmsh.model.geo.addCurveLoop([1004, 92, -1001], 2004)
gmsh.model.geo.addPlaneSurface([2001], 2001)
gmsh.model.geo.addPlaneSurface([2002], 2002)
gmsh.model.geo.addPlaneSurface([2003], 2003)
gmsh.model.geo.addPlaneSurface([2004], 2004)

gmsh.model.geo.addLine(startTag=6, endTag=22, tag=1005)
gmsh.model.geo.addLine(startTag=6, endTag=27, tag=1006)
gmsh.model.geo.addLine(startTag=6, endTag=36, tag=1007)
gmsh.model.geo.addLine(startTag=6, endTag=45, tag=1008)
gmsh.model.geo.addCurveLoop([1005, 28, -1006], 2005)
gmsh.model.geo.addCurveLoop([1006, 94, -1008], 2006)
gmsh.model.geo.addCurveLoop([1008, 72, -1007], 2007)
gmsh.model.geo.addCurveLoop([1007, 50, -1005], 2008)
gmsh.model.geo.addPlaneSurface([2005], 2005)
gmsh.model.geo.addPlaneSurface([2006], 2006)
gmsh.model.geo.addPlaneSurface([2007], 2007)
gmsh.model.geo.addPlaneSurface([2008], 2008)

gmsh.model.geo.addSurfaceLoop([46, 68, 90, 112, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008], 300)
gmsh.model.geo.addVolume([300], 300)
# gmsh.model.geo.addVolume(46, 68, 90, 112, 201, 202)
gmsh.model.geo.synchronize()

# 41 63 85 107
# testtest = [(2, 41)]
# gmsh.model.geo.extrude(dimTags=testtest, dx=0, dy=0, dz=length, numElements=[numberOfLayerOfLongitudinal])

gmsh.model.geo.synchronize()

print(gmsh.model.mesh.getSizes([(0, 6)]))
gmsh.model.mesh.setSize(dimTags=[(0, 6)], size=10)
print(gmsh.model.mesh.getSizes([(0, 6)]))

# pts = gmsh.model.getEntities(0)
# for p in pts:
#     print(gmsh.model.mesh.getSizes(p[0]))
#     print(p)
# print("p = ", p)

l = gmsh.model.getEntities(1)
for i in l:
    gmsh.model.mesh.setTransfiniteCurve(tag=i[1], numNodes=11, meshType="Progression", coef=1.0)

gmsh.model.mesh.setTransfiniteCurve(tag=26, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=48, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=70, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=92, numNodes=11, meshType="Progression", coef=1.0)

# gmsh.model.mesh.setTransfiniteCurve(tag=1000, numNodes=50, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1001, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1002, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1003, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1004, numNodes=21, meshType="Progression", coef=1.0)

# gmsh.model.mesh.setTransfiniteCurve(tag=1005, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1006, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1007, numNodes=21, meshType="Progression", coef=1.0)
# gmsh.model.mesh.setTransfiniteCurve(tag=1008, numNodes=21, meshType="Progression", coef=1.0)

gmsh.model.mesh.setTransfiniteSurface(tag=12)
gmsh.model.mesh.setTransfiniteSurface(tag=16)
gmsh.model.mesh.setTransfiniteSurface(tag=20)
gmsh.model.mesh.setTransfiniteSurface(tag=24)
# gmsh.model.mesh.setTransfiniteSurface(tag=2001)
# gmsh.model.mesh.setTransfiniteSurface(tag=2002)
# gmsh.model.mesh.setTransfiniteSurface(tag=2003)
# gmsh.model.mesh.setTransfiniteSurface(tag=2004)
# gmsh.model.mesh.setTransfiniteSurface(tag=2005)
# gmsh.model.mesh.setTransfiniteSurface(tag=2006)
# gmsh.model.mesh.setTransfiniteSurface(tag=2007)
# gmsh.model.mesh.setTransfiniteSurface(tag=2008)
gmsh.model.mesh.setTransfiniteVolume(tag=1)
gmsh.model.mesh.setTransfiniteVolume(tag=2)
gmsh.model.mesh.setTransfiniteVolume(tag=3)
gmsh.model.mesh.setTransfiniteVolume(tag=4)
# gmsh.model.mesh.setTransfiniteVolume(tag=300)
gmsh.model.mesh.setRecombine(dim=2, tag=12)
gmsh.model.mesh.setRecombine(dim=2, tag=16)
gmsh.model.mesh.setRecombine(dim=2, tag=20)
gmsh.model.mesh.setRecombine(dim=2, tag=24)

# gmsh.model.mesh.setRecombine(dim=2, tag=2001)
# gmsh.model.mesh.setRecombine(dim=2, tag=2002)
# gmsh.model.mesh.setRecombine(dim=2, tag=2003)
# gmsh.model.mesh.setRecombine(dim=2, tag=2004)
# gmsh.model.mesh.setRecombine(dim=2, tag=2005)
# gmsh.model.mesh.setRecombine(dim=2, tag=2006)
# gmsh.model.mesh.setRecombine(dim=2, tag=2007)
# gmsh.model.mesh.setRecombine(dim=2, tag=2008)


gmsh.option.setNumber("Mesh.MeshSizeMin", 2.0)
gmsh.option.setNumber("Mesh.MeshSizeMax", 2.0)
gmsh.model.mesh.generate(3)
print("finish meshing")

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("circle-boundary-3d.msh")
gmsh.write("circle-boundary-3d.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
