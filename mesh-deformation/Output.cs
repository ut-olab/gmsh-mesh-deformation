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
        public Output(Mesh mesh, string dirPath, string thisOs, Reference reference) {
            OutputMesh(mesh, dirPath, thisOs, reference);
        }

        private void OutputMesh(Mesh mesh, string dirPath, string thisOs, Reference reference)
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
            else if (thisOs == "Win32NT")
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
                sw.WriteLine($"{mesh.PhysicalInfos.Count}");
                foreach (var physical in mesh.PhysicalInfos)
                {
                    if (physical.PhysicalName == "INTERNAL")
                    {
                        sw.WriteLine($"3 {physical.PhysicalID} \"{physical.PhysicalName}\"");
                    } 
                    else
                    {
                        sw.WriteLine($"2 {physical.PhysicalID} \"{physical.PhysicalName}\"");
                    }
                }
                sw.WriteLine("$EndPhysicalNames");
                sw.WriteLine("$Nodes");
                sw.WriteLine($"{reference.NodeMoved.Length}");
                for (int i = 0; i < reference.NodeMoved.Length; i++)
                {
                    sw.WriteLine($"{i + 1} {reference.NodeMoved[i].X.ToString()} {reference.NodeMoved[i].Y.ToString()} {reference.NodeMoved[i].Z.ToString()}");
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
