using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{
    public class Matrix
    {
        public float[,] Mat { get; set; }

        public Matrix(float[,] mat)
        {
            this.Mat = mat;
        }

        public void Print()
        {
            Debug.WriteLine($"---------------------");
            for (int m = 0; m < this.Mat.GetLength(0); m++)
            {
                for (int n = 0; n < this.Mat.GetLength(1); n++)
                {
                    Debug.Write($"{this.Mat[m, n]} ");
                }
                Debug.WriteLine("");
            }
        }

        public void Add()
        {
            for (int m = 0; m < this.Mat.GetLength(0); m++)
            {
                for (int n = 0; n < this.Mat.GetLength(1); n++)
                {
                    this.Mat[m, n] += 1;
                }
            }
        }

    }
}
