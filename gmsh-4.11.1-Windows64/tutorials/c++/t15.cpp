// -----------------------------------------------------------------------------
//
//  Gmsh C++ tutorial 15
//
//  Embedded points, lines and surfaces
//
// -----------------------------------------------------------------------------

// By default, across geometrical dimensions meshes generated by Gmsh are only
// conformal if lower dimensional entities are on the boundary of higher
// dimensional ones (i.e. if points, curves or surfaces are part of the boundary
// of volumes).

// Embedding constraints allow to force a mesh to be conformal to other lower
// dimensional entities.

#include <set>
#include <gmsh.h>

int main(int argc, char **argv)
{
  gmsh::initialize();

  gmsh::model::add("t15");

  // Copied from `t1.cpp':
  double lc = 1e-2;
  gmsh::model::geo::addPoint(0, 0, 0, lc, 1);
  gmsh::model::geo::addPoint(.1, 0, 0, lc, 2);
  gmsh::model::geo::addPoint(.1, .3, 0, lc, 3);
  gmsh::model::geo::addPoint(0, .3, 0, lc, 4);
  gmsh::model::geo::addLine(1, 2, 1);
  gmsh::model::geo::addLine(3, 2, 2);
  gmsh::model::geo::addLine(3, 4, 3);
  gmsh::model::geo::addLine(4, 1, 4);
  gmsh::model::geo::addCurveLoop({4, 1, -2, 3}, 1);
  gmsh::model::geo::addPlaneSurface({1}, 1);

  // We change the mesh size to generate a coarser mesh
  lc *= 4;
  gmsh::model::geo::mesh::setSize({{0, 1}, {0, 2}, {0, 3}, {0, 4}}, lc);

  // We define a new point
  gmsh::model::geo::addPoint(0.02, 0.02, 0., lc, 5);

  // We have to synchronize before embedding entites:
  gmsh::model::geo::synchronize();

  // One can force this point to be included ("embedded") in the 2D mesh, using
  // the `embed()' function:
  gmsh::model::mesh::embed(0, {5}, 2, 1);

  // In the same way, one can use `embed()' to force a curve to be embedded in
  // the 2D mesh:
  gmsh::model::geo::addPoint(0.02, 0.12, 0., lc, 6);
  gmsh::model::geo::addPoint(0.04, 0.18, 0., lc, 7);
  gmsh::model::geo::addLine(6, 7, 5);
  gmsh::model::geo::synchronize();
  gmsh::model::mesh::embed(1, {5}, 2, 1);

  // Points and curves can also be embedded in volumes
  std::vector<std::pair<int, int> > ext;
  gmsh::model::geo::extrude({{2, 1}}, 0, 0, 0.1, ext);

  int p = gmsh::model::geo::addPoint(0.07, 0.15, 0.025, lc);

  gmsh::model::geo::synchronize();
  gmsh::model::mesh::embed(0, {p}, 3, 1);

  gmsh::model::geo::addPoint(0.025, 0.15, 0.025, lc, p + 1);
  int l = gmsh::model::geo::addLine(7, p + 1);

  gmsh::model::geo::synchronize();
  gmsh::model::mesh::embed(1, {l}, 3, 1);

  // Finally, we can also embed a surface in a volume:
  gmsh::model::geo::addPoint(0.02, 0.12, 0.05, lc, p + 2);
  gmsh::model::geo::addPoint(0.04, 0.12, 0.05, lc, p + 3);
  gmsh::model::geo::addPoint(0.04, 0.18, 0.05, lc, p + 4);
  gmsh::model::geo::addPoint(0.02, 0.18, 0.05, lc, p + 5);

  gmsh::model::geo::addLine(p + 2, p + 3, l + 1);
  gmsh::model::geo::addLine(p + 3, p + 4, l + 2);
  gmsh::model::geo::addLine(p + 4, p + 5, l + 3);
  gmsh::model::geo::addLine(p + 5, p + 2, l + 4);

  int ll = gmsh::model::geo::addCurveLoop({l + 1, l + 2, l + 3, l + 4});
  int s = gmsh::model::geo::addPlaneSurface({ll});

  gmsh::model::geo::synchronize();
  gmsh::model::mesh::embed(2, {s}, 3, 1);

  // Note that with the OpenCASCADE kernel (see `t16.cpp'), when the
  // `fragment()' function is applied to entities of different dimensions, the
  // lower dimensional entities will be autmatically embedded in the higher
  // dimensional entities if necessary.

  gmsh::model::mesh::generate(3);

  gmsh::write("t15.msh");

  // Launch the GUI to see the results:
  std::set<std::string> args(argv, argv + argc);
  if(!args.count("-nopopup")) gmsh::fltk::run();

  gmsh::finalize();
  return 0;
}
