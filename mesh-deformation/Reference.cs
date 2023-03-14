using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Numerics;
using System.Threading;
using System.Xml.Xsl;

namespace mesh_deformation
{
    public class Reference
    {
        private List<float[]> OriPoints { get; set; }
        private List<float[]> MovedPoints { get; set; }
        public List<float[,]> Matrixs { get; set; }

        public Node[] NodeOrigin { get; set; }
        public Node[] NodeMoved { get; set; }
        private List<Vector3> Difference { get; set; }
        private HashSet<float> ZHashSet { get; set; }
        private SortedSet<float> ZSortedSet { get; set; }

        public Reference(Node[] nodeOrigin)
        {

            Debug.WriteLine("Reference");
            SetNodeOrigin(nodeOrigin);

            CalculateNodeMoved();
        }

        public void CalculateNodeMoved()
        {
            var numberOfNode = this.NodeOrigin.Length;
            this.NodeMoved = new Node[numberOfNode];
            for (int index = 0; index < numberOfNode; index++)
            {
                float[] xyz = new float[3]
                {
                    this.NodeOrigin[index].X,
                    this.NodeOrigin[index].Y,
                    this.NodeOrigin[index].Z,
                };
                //HairetsuExtensions.PrintVec(xyz);
                float[] delta1 = new float[3]
                {
                    0.0f,
                    0.0f,
                    -this.NodeOrigin[index].Z,
                };
                float[] delta2 = new float[3]
                {
                    0.0f,
                    //-(float)Math.Pow((this.NodeOrigin[index].Z * 0.1f), 2),
                    -(float)Math.Sin(this.NodeOrigin[index].Z * 0.5f),
                    this.NodeOrigin[index].Z,
                };
                float angle = 5;
                var shiftedPoint = CoordinateTransformer.Parallel(xyz, delta1);
                //var rotatePoint = CoordinateTransformer.RotateX(shiftedPoint, angle * this.NodeOrigin[index].Z);
                var rotatePoint = CoordinateTransformer.RotateX(shiftedPoint, (float)Math.Cos(this.NodeOrigin[index].Z * 0.5f));
                var res = CoordinateTransformer.Parallel(rotatePoint, delta2);
                var node = new Node()
                {
                    Index = index,
                    X = res[0],
                    Y = res[1],
                    Z = res[2],
                };
                this.NodeMoved[index] = node;
            }
        }

        private void SetNodeOrigin(Node[] nodeOrigin)
        {
            this.NodeOrigin = nodeOrigin;
            this.ZHashSet = new HashSet<float>();
            this.ZSortedSet = new SortedSet<float>();
            foreach (var node in NodeOrigin)
            {
                SetZHashSet(node.Z);
            }
        }


        private void SetZHashSet(float z)
        {
            this.ZHashSet.Add(z);
            this.ZSortedSet.Add(z);
        }
    }
}
