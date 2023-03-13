using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Numerics;

namespace mesh_deformation
{
    public partial class Program
    {
        private string DirPath;
        public Mesh Mesh { get; set; }

        private static void Main(string[] args)
        {
            var os = Environment.OSVersion;
            Console.WriteLine("Current OS Information:\n");
            string thisOs = os.Platform.ToString();
            Console.WriteLine("Platform: {0:G}", os.Platform);
            Console.WriteLine("Version String: {0}", os.VersionString);
            Console.WriteLine("Version Information:");
            Console.WriteLine("   Major: {0}", os.Version.Major);
            Console.WriteLine("   Minor: {0}", os.Version.Minor);
            Console.WriteLine("Service Pack: '{0}'", os.ServicePack);
            var program = new Program();
            if (args.Length == 0)
            {
                Console.Write("引数がうまく設定されていません。");
                return;
            }
            var filePath = args[0];
            string[] lines;
            lines = File.ReadAllLines(args[0]);
            program.DirPath = Path.GetDirectoryName(args[0]);

            if (lines == null)
            {
                return;
            }

            Mesh mesh = new Mesh(lines);
            program.Mesh = mesh;


            var reference = new Reference(mesh.NodesOrigin);

            //mesh.CalculateUpdatePoints(reference.Matrixs, program.Mesh.Nodes);
            Output output;
            output = new Output(program.Mesh, program.DirPath, thisOs, reference);


            //var matA = new float[,] {
            //    {1, 2, 3 },
            //    {4, 5, 6 },
            //    {7, 8, 9 }
            //};
            //matA.Print();
            //var matB =new float[,] {
            //    { 1, 4, 8 },
            //    { 6, 2, 5 },
            //    { 9, 7, 3 }
            //};
            //matB.Print();
            //var add = HairetsuExtensions.Add(matA, matB);
            //add.Print();
            //var mul = HairetsuExtensions.Multiple(matA, matB);
            //mul.Print();

            var mat = new float[,] {
                {1, 2, 3 },
                {4, 5, 6 },
                {7, 8, 9 }
            };
            var vec = new float[] { 1, 2, 3 };
            var res = HairetsuExtensions.MultipleMatVec(mat, vec);
            res.PrintVec();
        }
    }
}