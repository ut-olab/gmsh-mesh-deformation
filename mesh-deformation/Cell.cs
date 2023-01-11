using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{
    public class Cell
    {
        public int[] NodesIndex { get; set; }
        public CellType CellType { get; set; }
        public int PhysicalID { get; set; }
        public int EntityID { get; set; }
    }
    public enum CellType
    {
        Triangle = 2,
        Quadrilateral = 3,
        Tetrahedron = 4,
        Prism = 6
    }
}
