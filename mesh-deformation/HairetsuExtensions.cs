using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{

    // 配列の拡張メソッドを管理するクラス
    // https://qiita.com/baba_s/items/807523551a0c79e6a3c2
    public static class HairetsuExtensions
    {
        /// <summary>
        /// output vector
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="vec"></param>
        public static void PrintVec<T>(
            this T[] vec
        )
        {
            Debug.WriteLine($"---------------------");
            int row = vec.Length;
            for (int m = 0; m < vec.Length; m++)
            {
                Debug.WriteLine($"{vec[m]}");
            }
        }


        /// <summary>
        /// output matrix
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="mat"></param>
        public static void PrintMat<T>(
            this T[,] mat
        )
        {
            Debug.WriteLine($"---------------------");
            int row = mat.GetLength(0);
            int col = mat.GetLength(1);
            Debug.WriteLine($"{mat.GetType()}, {row} {col}");
            for (int m = 0; m < row; m++)
            {
                for (int n = 0; n < col; n++)
                {
                    Debug.Write($"{mat[m, n]} ");
                }
                Debug.WriteLine("");
            }
        }
        
        public static T[] AddVec<T>(
            T[] vecA,
            T[] vecB
            )
            where T : INumber<T>
        {
            ConfirmationVec(vecA, vecB);
            int row = vecA.GetLength(0);
            var resVec = new T[row];
            for (int m = 0; m < row; m++)
            {
                resVec[m] = vecA[m] + vecB[m];
            }
            return resVec;
        }

        public static T[,] AddMat<T>(
            T[,] matA,
            T[,] matB
            )
             where T : INumber<T>
        {
            ConfirmationMat(matA, matB);
            int row = matA.GetLength(0);
            int col = matA.GetLength(1);
            var matRes = new T[row, col];
            for (int m = 0; m < row; m++)
            {
                for (int n = 0; n < col; n++)
                {
                    matRes[m, n] = matA[m, n] + matB[m, n];
                }
            }
            return matRes;
        }

        public static T[,] MultipleMatMat<T>(
            T[,] matA,
            T[,] matB
            )
            where T : INumber<T>
        {
            ConfirmationMat(matA, matB);
            int row = matA.GetLength(0);
            int col = matA.GetLength(1);
            var matRes = new T[row, col];
            for (int m = 0; m < row; m++)
            {
                for (int n = 0; n < col; n++)
                {
                    for (int l = 0; l < row; l++)
                    {
                        matRes[m, n] += matA[m, l] * matB[l, n];
                    }
                }
            }
            return matRes;
        }
        //public static T[,] MatrixMatrix<T>(
        //    this T[,] matA,
        //    T[,] matB
        //    )
        //    where T : INumber<T>
        //{
        //    var matRes = new T[matA.GetLength(0), matB.GetLength(1)];
        //    for (int i = 0; i < matA.GetLength(0); i++)
        //    {
        //        for (int j = 0; j < matA.GetLength(1); j++)
        //        {
        //            for (int k = 0; k < matA.GetLength(0); k++)
        //            {
        //                matRes[i, j] += matA[i, k] * matB[k, j];
        //            }
        //        }
        //    }
        //    return matRes;
        //}

        public static T[] MultipleMatVec<T>(
            T[,] mat,
            T[] vec
            )
            where T : INumber<T>
        {
            var vecRes = new T[mat.GetLength(0)];
            for (int i = 0; i < mat.GetLength(0); i++)
            {
                for (int j = 0; j < mat.GetLength(1); j++)
                {
                    vecRes[i] += mat[i, j] * vec[j]; 
                }
            }
            return vecRes;
        }

        public static void ConfirmationVec<T>(T[] vecA, T[] vecB)
        {
            if (vecA.GetLength(0) != vecB.GetLength(0))
            {
                throw new ArgumentException("足し算するvectorの要素数が異なるよ");
            }
        }
        public static void ConfirmationMat<T>(T[,] matA, T[,] matB)
        {
            if (matA.GetLength(0) != matB.GetLength(0) || matA.GetLength(1) != matB.GetLength(1))
            {
                throw new ArgumentException("足し算するmatrixの要素数が異なるよ");
            }
        }
    }
}
