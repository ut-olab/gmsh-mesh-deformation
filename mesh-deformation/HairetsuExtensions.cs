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
        /// 行列を表示するメソッド
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="mat"></param>
        public static void Print<T>(
            this T[,] mat
            )
        {
            Debug.WriteLine($"---------------------");
            Debug.WriteLine($"{mat.GetType()}, {mat.GetLength(0)} {mat.GetLength(1)}");
            for (int m = 0; m < mat.GetLength(0); m++)
            {
                for (int n = 0; n < mat.GetLength(1); n++)
                {
                    Debug.Write($"{mat[m, n]} ");
                }
                Debug.WriteLine("");
            }
        }
        public static void Pirnt<T>(
            this T[] vec
            )
        {
            Debug.WriteLine($"---------------------");
            for (int i = 0; i < vec.Length; i++)
            {
                Debug.WriteLine($"{vec[i]}");
            }
        }

        
        public static T[,] Add<T>(
            T[,] matA,
            T[,] matB
            )
             where T : INumber<T>
        {
            Confirmation(matA, matB);
            var matRes = new T[matA.GetLength(0), matB.GetLength(1)];
            for (int i = 0; i < matA.GetLength(0); i++)
            {
                for (int j = 0; j < matA.GetLength(1); j++)
                {
                    matRes[i, j] = matA[i, j] + matB[i, j];
                }
            }
            return matRes;
        }

        public static T[,] MatrixMatrix<T>(
            T[,] matA,
            T[,] matB
            )
            where T : INumber<T>
        {
            var matRes = new T[matA.GetLength(0), matB.GetLength(1)];
            for (int i = 0; i < matA.GetLength(0); i++)
            {
                for (int j = 0; j < matA.GetLength(1); j++)
                {
                    for (int k = 0; k < matA.GetLength(0); k++)
                    {
                        matRes[i, j] += matA[i, k] * matB[k, j];
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

        public static T[] MatrixVector<T>(
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



        public static void Confirmation<T>(T[,] matA, T[,] matB)
        {
            if (matA.GetLength(0) != matB.GetLength(0) || matA.GetLength(1) != matB.GetLength(1))
            {
                throw new ArgumentException("足し算する配列の要素数が異なるよ");
            }
        }
    }
}
