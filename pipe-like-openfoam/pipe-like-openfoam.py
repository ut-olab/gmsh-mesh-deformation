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

# r < RB < R
R = 0.5
r = 0.35
RB = 0.49
theta = math.pi / 4
test = 0.3
LZ = 20.0

NC = 18;  # no. of nodes ( = #elem+1) in azimuthal direction
NB = 1;   # no. of elemtns adjacent to the wall
NM = 8;   # no. of nodes ( = #elem+1) between the near wall layer and central square part
# compression ratios over the radial lines of the mesh
compressRatio_B = 0.85;  #ratio of grid compression toward the wall (<1)
compressRatio_M = 0.87;  #compression ratio in the middle layer
NZ = 400;    #no of elements in z-dire (axial)

dx = r * math.cos(theta)
dy = r * math.sin(theta)
dxB = RB * math.cos(theta)
dyB = RB * math.sin(theta)
Dx = R * math.cos(theta)
Dy = R * math.sin(theta)

# define points coordinates
gmsh.model.geo.addPoint(x=0.0, y=0.0, z=0.0, tag=1)
gmsh.model.geo.addPoint(x=test * R, y=0.0, z=0.0, tag=2)
gmsh.model.geo.addPoint(x=0, y=-test*R, z=0.0, tag=3)
gmsh.model.geo.addPoint(x=-test*R, y=0.0, z=0.0, tag=4)
gmsh.model.geo.addPoint(x=0.0, y=test*R, z=0.0, tag=5)

gmsh.model.geo.addPoint(x=dx, y=dy, z=0.0, tag=6)
gmsh.model.geo.addPoint(x=dx, y=-dy, z=0.0, tag=7)
gmsh.model.geo.addPoint(x=-dx, y=-dy, z=0.0, tag=8)
gmsh.model.geo.addPoint(x=-dx, y=dy, z=0.0, tag=9)
gmsh.model.geo.addPoint(x=dxB, y=dyB, z=0.0, tag=10)
gmsh.model.geo.addPoint(x=dxB, y=-dyB, z=0.0, tag=11)
gmsh.model.geo.addPoint(x=-dxB, y=-dyB, z=0.0, tag=12)
gmsh.model.geo.addPoint(x=-dxB, y=dyB, z=0.0, tag=13)
gmsh.model.geo.addPoint(x=Dx, y=Dy, z=0.0, tag=14)
gmsh.model.geo.addPoint(x=Dx, y=-Dy, z=0.0, tag=15)
gmsh.model.geo.addPoint(x=-Dx, y=-Dy, z=0.0, tag=16)
gmsh.model.geo.addPoint(x=-Dx, y=Dy, z=0.0, tag=17)

# define lines and curves
gmsh.model.geo.addCircleArc(startTag=9, centerTag=3, endTag=6, tag=1)
gmsh.model.geo.addCircleArc(startTag=6, centerTag=4, endTag=7, tag=2)
gmsh.model.geo.addCircleArc(startTag=7, centerTag=5, endTag=8, tag=3)
gmsh.model.geo.addCircleArc(startTag=8, centerTag=2, endTag=9, tag=4)
gmsh.model.geo.addCircleArc(startTag=13, centerTag=1, endTag=10, tag=5)
gmsh.model.geo.addCircleArc(startTag=10, centerTag=1, endTag=11, tag=6)
gmsh.model.geo.addCircleArc(startTag=11, centerTag=1, endTag=12, tag=7)
gmsh.model.geo.addCircleArc(startTag=12, centerTag=1, endTag=13, tag=8)
gmsh.model.geo.addCircleArc(startTag=17, centerTag=1, endTag=14, tag=9)
gmsh.model.geo.addCircleArc(startTag=14, centerTag=1, endTag=15, tag=10)
gmsh.model.geo.addCircleArc(startTag=15, centerTag=1, endTag=16, tag=11)
gmsh.model.geo.addCircleArc(startTag=16, centerTag=1, endTag=17, tag=12)
gmsh.model.geo.addLine(startTag=6, endTag=10, tag=13)
gmsh.model.geo.addLine(startTag=7, endTag=11, tag=14)
gmsh.model.geo.addLine(startTag=8, endTag=12, tag=15)
gmsh.model.geo.addLine(startTag=9, endTag=13, tag=16)
gmsh.model.geo.addLine(startTag=10, endTag=14, tag=17)
gmsh.model.geo.addLine(startTag=11, endTag=15, tag=18)
gmsh.model.geo.addLine(startTag=12, endTag=16, tag=19)
gmsh.model.geo.addLine(startTag=13, endTag=17, tag=20)

# create surfaces
gmsh.model.geo.addCurveLoop(curveTags=[1, 2, 3, 4], tag=1)
gmsh.model.geo.addPlaneSurface(wireTags=[1], tag=1)
gmsh.model.geo.addCurveLoop(curveTags=[5, -13, -1, 16], tag=2)
gmsh.model.geo.addPlaneSurface(wireTags=[2], tag=2)
gmsh.model.geo.addCurveLoop(curveTags=[13, 6, -14 , -2], tag=3)
gmsh.model.geo.addPlaneSurface(wireTags=[3], tag=3)
gmsh.model.geo.addCurveLoop(curveTags=[-3, 14, 7, -15], tag=4)
gmsh.model.geo.addPlaneSurface(wireTags=[4], tag=4)
gmsh.model.geo.addCurveLoop(curveTags=[-16, -4, 15, 8], tag=5)
gmsh.model.geo.addPlaneSurface(wireTags=[5], tag=5)
gmsh.model.geo.addCurveLoop(curveTags=[9, -17, -5, 20], tag=6)
gmsh.model.geo.addPlaneSurface(wireTags=[6], tag=6)
gmsh.model.geo.addCurveLoop(curveTags=[17, 10, -18, -6], tag=7)
gmsh.model.geo.addPlaneSurface(wireTags=[7], tag=7)
gmsh.model.geo.addCurveLoop(curveTags=[-7, 18, 11, -19], tag=8)
gmsh.model.geo.addPlaneSurface(wireTags=[8], tag=8)
gmsh.model.geo.addCurveLoop(curveTags=[-8, 19, 12, -20], tag=9)
gmsh.model.geo.addPlaneSurface(wireTags=[9], tag=9)

gmsh.model.geo.synchronize()

surfaceList = gmsh.model.getEntities(2)
print(surfaceList)
test = []
for s in surfaceList:
    test.append(s[1])
print(test)

gmsh.model.mesh.setRecombine(dim=2, tag=1)


bottomPlane = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)]
gmsh.model.geo.extrude(dimTags=bottomPlane, dx=0, dy=0, dz=LZ, numElements=[NZ], recombine=True)

gmsh.model.geo.synchronize()

gmsh.model.mesh.setRecombine(dim=2, tag=1)
gmsh.model.mesh.setRecombine(dim=2, tag=2)
gmsh.model.mesh.setRecombine(dim=2, tag=3)
gmsh.model.mesh.setRecombine(dim=2, tag=4)
gmsh.model.mesh.setRecombine(dim=2, tag=5)
gmsh.model.mesh.setRecombine(dim=2, tag=6)
gmsh.model.mesh.setRecombine(dim=2, tag=7)
gmsh.model.mesh.setRecombine(dim=2, tag=8)
gmsh.model.mesh.setRecombine(dim=2, tag=9)

gmsh.model.mesh.setRecombine(dim=3, tag=1)
gmsh.model.mesh.setRecombine(dim=3, tag=2)
gmsh.model.mesh.setRecombine(dim=3, tag=3)
gmsh.model.mesh.setRecombine(dim=3, tag=4)
gmsh.model.mesh.setRecombine(dim=3, tag=5)
gmsh.model.mesh.setRecombine(dim=3, tag=6)
gmsh.model.mesh.setRecombine(dim=3, tag=7)
gmsh.model.mesh.setRecombine(dim=3, tag=8)
gmsh.model.mesh.setRecombine(dim=3, tag=9)

gmsh.model.mesh.setTransfiniteCurve(tag=1, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=2, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=3, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=4, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=5, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=6, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=7, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=8, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=9, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=10, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=11, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=12, numNodes=NC, meshType="Progression", coef=1.0)
gmsh.model.mesh.setTransfiniteCurve(tag=13, numNodes=NM, meshType="Progression", coef=compressRatio_M)
gmsh.model.mesh.setTransfiniteCurve(tag=14, numNodes=NM, meshType="Progression", coef=compressRatio_M)
gmsh.model.mesh.setTransfiniteCurve(tag=15, numNodes=NM, meshType="Progression", coef=compressRatio_M)
gmsh.model.mesh.setTransfiniteCurve(tag=16, numNodes=NM, meshType="Progression", coef=compressRatio_M)
gmsh.model.mesh.setTransfiniteCurve(tag=17, numNodes=NB, meshType="Progression", coef=compressRatio_B)
gmsh.model.mesh.setTransfiniteCurve(tag=18, numNodes=NB, meshType="Progression", coef=compressRatio_B)
gmsh.model.mesh.setTransfiniteCurve(tag=19, numNodes=NB, meshType="Progression", coef=compressRatio_B)
gmsh.model.mesh.setTransfiniteCurve(tag=20, numNodes=NB, meshType="Progression", coef=compressRatio_B)

surfaceList = gmsh.model.getEntities(2)
test = []
for s in surfaceList:
    test.append(s[1])
print(test)
for pp in test:
    print(pp)
    gmsh.model.mesh.setRecombine(dim=2, tag=pp)
    gmsh.model.mesh.setTransfiniteSurface(tag=pp)

wall = [139, 213, 191, 165]
gmsh.model.addPhysicalGroup(2, wall, 11)
gmsh.model.setPhysicalName(2, 11, "WALL")

inlet = [1, 2, 3, 4, 5, 6, 7, 8, 9]
gmsh.model.addPhysicalGroup(2, inlet, 12)
gmsh.model.setPhysicalName(2, 12, "INLET")

outlet = [42, 64, 86, 108, 130, 152, 174, 196, 218]
gmsh.model.addPhysicalGroup(2, outlet, 13)
gmsh.model.setPhysicalName(2, 13, "OUTLET")

v = gmsh.model.getEntities(3)
three_dimension_list = []
for i in range(len(v)):
    three_dimension_list.append(v[i][1])
gmsh.model.addPhysicalGroup(3, three_dimension_list, 100)
gmsh.model.setPhysicalName(3, 100, "INTERNAL")

gmsh.model.mesh.generate(3)
print("finish meshing")

gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("pipe-like-openfoam.msh")
gmsh.write("pipe-like-openfoam.vtk")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
