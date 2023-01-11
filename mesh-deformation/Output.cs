using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace mesh_deformation
{
    public class Output
    {
        public Output(Mesh mesh, string dirPath, string thisOs) {
            OutputMesh(mesh, dirPath, thisOs);
        }

        private void OutputMesh(Mesh mesh, string dirPath, string thisOs)
        {
            Debug.WriteLine($"{dirPath}");
            string folder = "";
            string fileName = "";
            if (thisOs == "Unix")
            {
                folder = $@"{dirPath}";
                fileName = $@"{folder}" + @"/" + "model-after.msh";
                Console.WriteLine($"{fileName}");
            }
            else if (thisOs == "windows")
            {
                folder = $@"{dirPath}";
                fileName = $@"{folder}" + @"\" + "model-after.msh";
            }
            using (var sw = new StreamWriter(fileName))
            {
                sw.WriteLine("$MeshFormat");
                sw.WriteLine("2.2 0 8");
                sw.WriteLine("$EndMeshFormat");
                sw.WriteLine("$PhysicalNames");
                sw.WriteLine($"1");
                sw.WriteLine($"2 10 \"surface\"");
                sw.WriteLine("$EndPhysicalNames");
                sw.WriteLine("$Nodes");
                sw.WriteLine($"{mesh.UpdatedNodes.Length / 3}");
                for (int i = 0; i < mesh.UpdatedNodes.Length / 3; i++)
                {
                    sw.WriteLine($"{i + 1} {mesh.UpdatedNodes[(i * 3) + 0].ToString()} {mesh.UpdatedNodes[(i * 3) + 1].ToString()} {mesh.UpdatedNodes[(i * 3) + 2].ToString()}");
                }
                sw.WriteLine("$EndNodes");
                sw.WriteLine("$Elements");
                sw.WriteLine($"{mesh.Cells.Length}");
                int wholeIndex = 1;
                foreach (var cell in mesh.Cells)
                {
                    string line = $"";
                    line += $"{wholeIndex} ";
                    line += $"{(int)cell.CellType} ";
                    line += $"2 ";
                    line += $"{cell.PhysicalID} ";
                    line += $"{cell.EntityID} ";
                    for (int j = 0; j < cell.NodesIndex.Length; j++)
                    {
                        if (j == cell.NodesIndex.Length - 1)
                        {
                            line += $"{cell.NodesIndex[j]}";
                        } else
                        {
                            line += $"{cell.NodesIndex[j]} ";
                        }
                    }
                    wholeIndex++;
                    sw.WriteLine(line);
                }
                sw.WriteLine("$EndElements");
            }
        }
    }
}
