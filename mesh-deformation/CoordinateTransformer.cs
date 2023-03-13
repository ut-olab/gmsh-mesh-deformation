using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{
    public static class CoordinateTransformer
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="coord"></param>
        /// <param name="delta"></param>
        /// <returns></returns>
        public static float[] Parallel(float[] coord, float[] delta)
        {
            var res = HairetsuExtensions.AddVec(coord, delta);
            return res;
        }

        /// <summary>
        /// theta is normal angle['], not radian[rad]
        /// </summary>
        /// <param name="coord"></param>
        /// <param name="theta"></param>
        /// <returns></returns>
        public static float[] RotateX(float[] coord, float theta)
        {
            const float RADIAN = (float)Math.PI / 180;
            float thetaRadian = theta * RADIAN;
            float c = (float)Math.Cos(-thetaRadian);
            float s = (float)Math.Sin(-thetaRadian);
            float[,] mat = new float[3, 3]
            {
                {1.0f, 0.0f, 0.0f},
                {0.0f, c, s},
                {0.0f, -s, c},
            };
            var res = HairetsuExtensions.MultipleMatVec(mat, coord);
            return res;
        }

        /// <summary>
        /// theta is normal angle['], not radian[rad]
        /// </summary>
        /// <param name="coord"></param>
        /// <param name="theta"></param>
        /// <returns></returns>
        public static float[] RotateY(float[] coord, float theta)
        {
            const float RADIAN = (float)Math.PI / 180;
            float thetaRadian = theta * RADIAN;
            float c = (float)Math.Cos(-thetaRadian);
            float s = (float)Math.Sin(-thetaRadian);
            float[,] mat = new float[3, 3]
            {
                {c, 0.0f, -s},
                {0.0f, 1.0f, 0.0f},
                {s, 0.0f, c},
            };
            var res = HairetsuExtensions.MultipleMatVec(mat, coord);
            return res;
        }

        /// <summary>
        /// theta is normal angle['], not radian[rad]
        /// </summary>
        /// <param name="coord"></param>
        /// <param name="theta"></param>
        /// <returns></returns>
        public static float[] RotateZ(float[] coord, float theta)
        {
            const float RADIAN = (float)Math.PI / 180;
            float thetaRadian = theta * RADIAN;
            float c = (float)Math.Cos(-thetaRadian);
            float s = (float)Math.Sin(-thetaRadian);
            float[,] mat = new float[3, 3]
            {
                {c, s, 0.0f},
                {-s, c, 0.0f},
                {0.0f, 0.0f, 1.0f},
            };
            var res = HairetsuExtensions.MultipleMatVec(mat, coord);
            return res;
        }
    }
}
