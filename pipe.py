import gmsh
import math
import sys

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
length = 10.0
numberOfTest = 100

center = gmsh.model.geo.addPoint(x=0,y=0,z=0,tag=0)
gmsh.model.geo.addPoint(x=math.cos(math.pi*0)*radius, y=math.sin(math.pi*0)*radius, z=0, tag=1)
gmsh.model.geo.addPoint(x=math.cos(math.pi/2)*radius, y=math.sin(math.pi/2)*radius, z=0, tag=2)
gmsh.model.geo.addPoint(x=math.cos(math.pi*1)*radius, y=math.sin(math.pi*1)*radius, z=0, tag=3)
gmsh.model.geo.addPoint(x=math.cos(math.pi*3/2)*radius, y=math.sin(math.pi*3/2) * radius, z=0, tag=4)

gmsh.model.geo.addLine(startTag=center, endTag=1, tag=1)
gmsh.model.geo.addLine(startTag=center, endTag=2, tag=2)
gmsh.model.geo.addLine(startTag=center, endTag=3, tag=3)
gmsh.model.geo.addLine(startTag=center, endTag=4, tag=4)
gmsh.model.geo.addCircleArc(startTag=1, centerTag=center, endTag=2, tag=5)
gmsh.model.geo.addCircleArc(startTag=2, centerTag=center, endTag=3, tag=6)
gmsh.model.geo.addCircleArc(startTag=3, centerTag=center, endTag=4, tag=7)
gmsh.model.geo.addCircleArc(startTag=4, centerTag=center, endTag=1, tag=8)

gmsh.model.geo.addCurveLoop([1, 5, -2], 1)
gmsh.model.geo.addCurveLoop([2, 6, -3], 2)
gmsh.model.geo.addCurveLoop([3, 7, -4], 3)
gmsh.model.geo.addCurveLoop([4, 8, -1], 4)
gmsh.model.geo.addPlaneSurface([1], 1)
gmsh.model.geo.addPlaneSurface([2], 2)
gmsh.model.geo.addPlaneSurface([3], 3)
gmsh.model.geo.addPlaneSurface([4], 4)

ov = gmsh.model.geo.extrude(dimTags=[(2, 1)], dx=0, dy=0, dz=length, numElements=[numberOfTest], heights=[1])
ov = gmsh.model.geo.extrude(dimTags=[(2, 2)], dx=0, dy=0, dz=length, numElements=[numberOfTest], heights=[1])
ov = gmsh.model.geo.extrude(dimTags=[(2, 3)], dx=0, dy=0, dz=length, numElements=[numberOfTest], heights=[1])
ov = gmsh.model.geo.extrude(dimTags=[(2, 4)], dx=0, dy=0, dz=length, numElements=[numberOfTest], heights=[1])

# 25 42 5 76

gmsh.model.geo.synchronize()

gmsh.model.mesh.setTransfiniteCurve(tag=1, numNodes=21, meshType="Progression", coef=0.95)
gmsh.model.mesh.setTransfiniteCurve(tag=2, numNodes=21, meshType="Progression", coef=0.95)
gmsh.model.mesh.setTransfiniteCurve(tag=3, numNodes=21, meshType="Progression", coef=0.95)
gmsh.model.mesh.setTransfiniteCurve(tag=4, numNodes=21, meshType="Progression", coef=0.95)
gmsh.model.mesh.setTransfiniteCurve(tag=5, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=6, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=7, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=8, numNodes=11, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteSurface(tag=1)
gmsh.model.mesh.setTransfiniteSurface(tag=2)
gmsh.model.mesh.setTransfiniteSurface(tag=3)
gmsh.model.mesh.setTransfiniteSurface(tag=4)

inlet = [1, 2, 3, 4]
gmsh.model.addPhysicalGroup(2, inlet, 11)
gmsh.model.setPhysicalName(2, 11, "INLET")
outlet = [25, 42, 59, 76]
gmsh.model.addPhysicalGroup(2, outlet, 12)
gmsh.model.setPhysicalName(2, 12, "OUTLET")
outlet = [20, 37, 54, 71]
gmsh.model.addPhysicalGroup(2, outlet, 13)
gmsh.model.setPhysicalName(2, 13, "WALL")
v = gmsh.model.getEntities(3)
three_dimension_list = []
for i in range(len(v)):
    three_dimension_list.append(v[i][1])
gmsh.model.addPhysicalGroup(3, three_dimension_list, 100)
gmsh.model.setPhysicalName(3, 100, "INTERNAL")

# gmsh.model.mesh.setTransfiniteVolume(tag=1)
# gmsh.model.mesh.setRecombine(dim=2, tag=1)
# gmsh.model.mesh.setRecombine(dim=2, tag=2)
# gmsh.model.mesh.setRecombine(dim=2, tag=3)
# gmsh.model.mesh.setRecombine(dim=2, tag=4)

gmsh.model.mesh.generate(3)
print("finish meshing")

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("circle.msh")
gmsh.write("circle.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
