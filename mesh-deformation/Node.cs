using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{
    public class Node
    {
        public int Index { get; set; }
        public float X { get; set; }
        public float Y { get; set; }
        public float Z { get; set; }
        public float Angle { get; set; }
        public Vector3 Destination { get; set; }
        public float[,] RotationMatrix { get; set; }
    }
}
