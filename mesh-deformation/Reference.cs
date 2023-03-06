using System;
using System.Collections.Generic;
using System.Diagnostics;
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

        public Reference(Node[] nodeOrigin)
        {

            Debug.WriteLine("Reference");
            SetNodeOrigin(nodeOrigin);
            SetNodeOriginDestination();
            SetRotationMatrixNodeOrigin();
            SetNodeMoved();
            //SetNodeMoved();
            //SetOriginalPoints();
            //SetMovedPoints();
            //if (this.OriPoints.Count != this.MovedPoints.Count)
            //{
            //    throw new ArgumentException("配列の要素数が異なるよ");
            //}
            //CalculateDifference();
            //CalculateMatrixs();
            //Output();
        }

        private void SetNodeOrigin(Node[] nodeOrigin)
        {
            this.NodeOrigin = nodeOrigin;
            this.ZHashSet = new HashSet<float>();
            foreach (var node in NodeOrigin)
            {
                SetZHashSet(node.Z);
            }
        }

        private void SetNodeMoved()
        {
            var numberOfNode = this.NodeOrigin.Length;
            this.NodeMoved = new Node[numberOfNode];
            for (int index = 0; index < numberOfNode; index++)
            {
                float tempX = this.NodeOrigin[index].X;
                float tempY = this.NodeOrigin[index].Y;
                float tempZ = this.NodeOrigin[index].Z;
                var tempCoordinate = new float[3] { 0.0f, 0.0f, tempZ };
                float normalizedX = this.NodeOrigin[index].X;
                float normalizedY = this.NodeOrigin[index].Y;
                float normalizedZ = 0.0f;
                var normalizedCoordinate = new float[3] { normalizedX, normalizedY, normalizedZ };
                var array = new float[3];
                for (int i = 0; i < 3; i++)
                {
                    for (int j = 0; j < 3; j++)
                    {
                        array[i] += this.NodeOrigin[index].RotationMatrix[i, j] * normalizedCoordinate[j];
                    }
                }
                for (int i = 0; i < 3; i++)
                {
                    array[i] += tempCoordinate[i];
                }

                var node = new Node()
                {
                    Index = index,
                    //X = this.NodeOrigin[index].X + this.NodeOrigin[index].Destination[0],
                    //Y = this.NodeOrigin[index].Y + this.NodeOrigin[index].Destination[1],
                    //Z = this.NodeOrigin[index].Z + this.NodeOrigin[index].Destination[2],
                    X = array[0] + this.NodeOrigin[index].Destination[0],
                    Y = array[1] + this.NodeOrigin[index].Destination[1],
                    Z = array[2] + this.NodeOrigin[index].Destination[2],
                };
                this.NodeMoved[index] = node;
            }
        }

        private void SetNodeOriginDestination()
        {
            foreach (var node in NodeOrigin)
            {
                //node.Destination = new Vector3(0.0f, 0.02f, 0.0f);
                node.Destination = new Vector3(0.0f, -(float)(node.Z * 1.0), 0.0f);
            }
        }

        private void SetRotationMatrixNodeOrigin()
        {
            foreach (var node in this.NodeOrigin)
            {
                node.RotationMatrix = new float[3, 3] { { 1.0f, 0.0f, 0.0f }, {0.0f, (float)Math.Cos(node.Angle), -(float)Math.Sin(node.Angle) }, {  0.0f, (float)Math.Sin(node.Angle), (float)Math.Cos(node.Angle) }};
            }
        }

        private void SetZHashSet(float z)
        {
            this.ZHashSet.Add(z);
        }

        public void CalculateUpdatePoints(List<float[,]> matrixs, Node[] nodes)
        {
            ////this.UpdatedNodes = new float[this.Nodes.Length];
            //this.NodesUpdated = new Node[this.NodesClass.Length];
            //for (int i = 0; i < nodes.Length / 3; i++)
            //{
            //    var oriXYZ = new float[] { nodes[i * 3 + 0], nodes[i * 3 + 1], nodes[i * 3 + 2], 1f };
            //    var updatedXYZ = HairetsuExtensions.MultipleMatVec(matrixs[1], oriXYZ);
            //    this.UpdatedNodes[i * 3 + 0] = updatedXYZ[0];
            //    this.UpdatedNodes[i * 3 + 1] = updatedXYZ[1];
            //    this.UpdatedNodes[i * 3 + 2] = updatedXYZ[2];
            //    //var node = new Node()
            //    //{
            //    //    Index = index,
            //    //    X = float.Parse(cols[1]),
            //    //    Y = float.Parse(cols[2]),
            //    //    Z = float.Parse(cols[3]),
            //    //};
            //    //this.NodesClass[index] = node;
            //}

            //this.NodesUpdated = new Node[this.Nodes.Length];
            //for (int index = 0; index < nodes.Length; index++)
            //{
            //    var node = new Node()
            //    {
            //        Index = index,
            //        X = nodes[index].X + 1,
            //        Y = nodes[index].Y + 1,
            //        Z = nodes[index].Z + 1,
            //    };
            //    this.NodesUpdated[index] = node;
            //}
        }

        private void SetOriginalPoints()
        {
            this.OriPoints = new List<float[]>();
            this.OriPoints.Add(new float[]
            {
                0.5f, 0.0f, 0.0f
            });
            this.OriPoints.Add(new float[]
            {
                0.5f, 2.0f, 0.0f
            });
            this.OriPoints.Add(new float[]
            {
                0.5f, 4.0f, 0.0f
            });
        }
        private void SetMovedPoints()
        {
            this.MovedPoints = new List<float[]>();
            this.MovedPoints.Add(new float[]
            {
                0.5f, 0.0f, 0.0f
            });
            this.MovedPoints.Add(new float[]
            {
                0.75f, 2.0f, 0.0f
            });
            this.MovedPoints.Add(new float[]
            {
                0.5f, 4.0f, 0.0f
            });
        }

        private void CalculateDifference()
        {
            this.Difference = new List<Vector3>();
            for (int i = 0; i < OriPoints.Count; i++)
            {
                var diff = new Vector3(
                    MovedPoints[i][0] - OriPoints[i][0],
                    MovedPoints[i][1] - OriPoints[i][1],
                    MovedPoints[i][2] - OriPoints[i][2]
                );
                this.Difference.Add(diff);
            }
        }

        private void CalculateMatrixs()
        {
            this.Matrixs = new List<float[,]>();
            foreach (var p in this.Difference)
            {
                var mat = new float[,]
                {
                    { 1, 0, 0, p[0] },
                    { 0, 1, 0, p[1] },
                    { 0, 0, 1, p[2] },
                    { 0, 0, 0, 1 }
                };
                this.Matrixs.Add(mat);
            }
        }

        private void CalculateUpdatePoints(Mesh nodes)
        {

        }

        private void Output()
        {
            foreach (var r in this.OriPoints)
            {
                Debug.WriteLine($"{r[0]}, {r[1]}, {r[2]}");
            }
            foreach (var m in this.MovedPoints)
            {
                Debug.WriteLine($"{m[0]}, {m[1]}, {m[2]}");
            }
            foreach (var d in this.Difference)
            {
                Debug.WriteLine($"{d[0]}, {d[1]}, {d[2]}");
            }
            foreach (var mat in this.Matrixs)
            {
                mat.PrintMat();
            }
        }
    }
}
