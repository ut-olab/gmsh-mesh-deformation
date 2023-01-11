import gmsh
import sys

def OptionSetting():
    gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
    # gmsh.option.setNumber("Mesh.VolumeFaces", 1)
    gmsh.option.setNumber("Mesh.Lines", 1)
    gmsh.option.setNumber("Geometry.PointLabels", 1)
    gmsh.option.setNumber("General.MouseInvertZoom", 1)
    gmsh.option.setNumber("Mesh.LineWidth", 4)
    gmsh.option.setNumber("Mesh.OptimizeThreshold", 0.1)
    gmsh.option.setNumber("General.Axes", 3)
    gmsh.option.setNumber("General.Trackball", 0)
    gmsh.option.setNumber("General.RotationX", 0)
    gmsh.option.setNumber("General.RotationY", 0)
    gmsh.option.setNumber("General.RotationZ", 0)
    gmsh.option.setNumber("General.Terminal", 1)

def Syncronize():
    gmsh.model.geo.synchronize()

def ShapeCreation():
    gmsh.model.add("t1")
    lc = 1.5
    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(1.0, 0, 0, lc, 2)
    gmsh.model.geo.addPoint(1.0, 4.0, 0, lc, 3)
    p4 = gmsh.model.geo.addPoint(0, 4.0, 0, lc)
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(3, 2, 2)
    gmsh.model.geo.addLine(3, p4, 3)
    gmsh.model.geo.addLine(4, 1, p4)
    gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)

    Syncronize()

def NamingBoundary():
    gmsh.model.addPhysicalGroup(2, [1], 10)
    gmsh.model.setPhysicalName(2, 10, name = "My surface")
    Syncronize()

def Meshing():
    gmsh.model.mesh.optimize('Netgen', True)
    gmsh.model.mesh.generate(2)
    print("finish meshing")

def OutputMshVtk():
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write("model-before.msh")
    gmsh.write("model-before.vtk")

def ConfirmMesh():
    if "-nopopup" not in sys.argv:
        gmsh.fltk.run()


gmsh.initialize()

OptionSetting()
ShapeCreation()
NamingBoundary()
Meshing()
OutputMshVtk()
ConfirmMesh()


gmsh.finalize()
