import gmsh
import math
import sys

gmsh.initialize()

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
gmsh.option.setNumber("Mesh.OptimizeThreshold", 0.9)
gmsh.option.setNumber("General.Axes", 3)
gmsh.option.setNumber("General.Trackball", 0)
gmsh.option.setNumber("General.RotationX", 0)
gmsh.option.setNumber("General.RotationY", 0)
gmsh.option.setNumber("General.RotationZ", 0)
gmsh.option.setNumber("General.Terminal", 1)

lengthX = 0
lengthY = 1
lengthZ = 10
divideX = 0
divideY = 5
divideZ = 21

gmsh.model.geo.addPoint(x=0.0, y=-lengthY, z=0.0, tag=1)
gmsh.model.geo.addPoint(x=0.0, y=-lengthY, z=lengthZ, tag=2)
gmsh.model.geo.addPoint(x=0.0, y=lengthY, z=lengthZ, tag=3)
gmsh.model.geo.addPoint(x=0.0, y=lengthY, z=0.0, tag=4)

gmsh.model.geo.addLine(startTag=1, endTag=2, tag=1)
gmsh.model.geo.addLine(startTag=2, endTag=3, tag=2)
gmsh.model.geo.addLine(startTag=3, endTag=4, tag=3)
gmsh.model.geo.addLine(startTag=4, endTag=1, tag=4)

gmsh.model.geo.addCurveLoop(curveTags=[1, 2, 3, 4], tag=1)

gmsh.model.geo.addPlaneSurface(wireTags=[1], tag=1)

gmsh.model.geo.synchronize()

gmsh.model.mesh.setTransfiniteCurve(tag=1, numNodes=divideZ, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=2, numNodes=divideY, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=3, numNodes=divideZ, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=4, numNodes=divideY, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteSurface(tag=1)
gmsh.model.mesh.setRecombine(dim=2, tag=1)

gmsh.model.addPhysicalGroup(2, [1], 10)
gmsh.model.setPhysicalName(2, 10, "SURFACE")

gmsh.model.mesh.generate(2)

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("rectangle.msh")
gmsh.write("rectangle.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
