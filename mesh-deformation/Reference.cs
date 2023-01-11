using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Numerics;

namespace mesh_deformation
{
    public class Reference
    {
        private List<float[]> OriPoints { get; set; }
        private List<float[]> MovedPoints { get; set; }
        private List<float[]> Difference { get; set; }
        public List<float[,]> Matrixs { get; set; }

        public Reference()
        {
            Debug.WriteLine("Reference");
            SetOriginalPoints();
            SetMovedPoints();
            if (this.OriPoints.Count != this.MovedPoints.Count)
            {
                throw new ArgumentException("配列の要素数が異なるよ");
            }
            CalculateDifference();
            CalculateMatrixs();
            Output();
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
            this.Difference = new List<float[]>();
            for (int i = 0; i < OriPoints.Count; i++)
            {
                var diff = new float[]
                {
                    MovedPoints[i][0] - OriPoints[i][0],
                    MovedPoints[i][1] - OriPoints[i][1],
                    MovedPoints[i][2] - OriPoints[i][2]
                };
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
                mat.Print();
            }
        }
    }
}
