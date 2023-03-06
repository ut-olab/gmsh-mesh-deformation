using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace mesh_deformation
{
    public class Mesh
    {
        public Node[] NodesOrigin { get; set; }
        public Node[] NodesMoved { get; set; }
        public Cell[] Cells { get; set; }
        
        public List<PhysicalInfo> PhysicalInfos { get; set; }


        public Mesh(string[] lines)
        {
            (var cellsJugArray, this.PhysicalInfos) = ReadMeshFileGmsh22(lines);
            this.Cells = new Cell[cellsJugArray.Length];
            for (int i = 0; i < cellsJugArray.Length; i++)
            {
                var line = cellsJugArray[i];

                // ここで単体のCellを定義
                var cell = new Cell()
                {
                    CellType = (CellType)line[1],
                    PhysicalID = line[3],
                    EntityID = line[4]
                };

                if (cell.CellType == CellType.Triangle)
                {
                    cell.NodesIndex = new int[]
                    {
                        line[5],
                        line[6],
                        line[7]
                    };
                }
                else if (cell.CellType == CellType.Quadrilateral)
                {
                    cell.NodesIndex = new int[]
                    {
                        line[5],
                        line[6],
                        line[7],
                        line[8]
                    };
                }
                else if (cell.CellType == CellType.Tetrahedron)
                {
                    cell.NodesIndex = new int[]
                    {
                        line[5],
                        line[6],
                        line[7],
                        line[8]
                    };
                }
                else if (cell.CellType == CellType.Hexahedron)
                {
                    cell.NodesIndex = new int[]
                    {
                        line[5],
                        line[6],
                        line[7],
                        line[8],
                        line[9],
                        line[10],
                        line[11],
                        line[12],
                    };
                }
                else if (cell.CellType == CellType.Prism)
                {
                    cell.NodesIndex = new int[]
                    {
                        line[5],
                        line[6],
                        line[7],
                        line[8],
                        line[9],
                        line[10]
                    };
                }

                // ここで複数のCellsにCellを入れる
                this.Cells[i] = cell;
            }
        }

        private (int[][], List<PhysicalInfo>) ReadMeshFileGmsh22(string[] lines)
        {
            float[] nodes = null;
            int[][] elements = null;
            Dictionary<int, string> PhysicalNamesCorrespondence = null;
            var physicalInfos = new List<PhysicalInfo>();
            // Interpret lines.
            for (int currentLine = 0; currentLine < lines.Length; currentLine++)
            {
                if (lines[currentLine] == "$MeshFormat")
                {
                    //Debug.WriteLine("This is MeshFormat.");
                    currentLine += 2;
                }
                else if (lines[currentLine] == "$PhysicalNames")
                {
                    // TODO: PhysicalNamesが定義されていないときには対応できていない
                    currentLine += 1;
                    var physicalNameNumber = int.Parse(lines[currentLine]);
                    PhysicalNamesCorrespondence = new Dictionary<int, string>();
                    for (int index = 0; index < physicalNameNumber; index++)
                    {
                        var physicalInfo = new PhysicalInfo();
                        currentLine += 1;
                        //Debug.WriteLine($"{i}行目は{test[i]}");
                        string[] cols = lines[currentLine].Split(" ");
                        var id = int.Parse(cols[1]);
                        var name = cols[2].Replace("\"", "");
                        PhysicalNamesCorrespondence.Add(id, name);
                        physicalInfo.PhysicalID = id;
                        physicalInfo.PhysicalName = name;
                        physicalInfos.Add(physicalInfo);
                    }
                }
                else if (lines[currentLine] == "$Nodes")
                {
                    //Debug.WriteLine($"Nodes");
                    currentLine += 1;
                    var nodesNumber = int.Parse(lines[currentLine]);
                    this.NodesOrigin = new Node[nodesNumber];
                    for (int index = 0; index < nodesNumber; index++)
                    {
                        currentLine += 1;
                        string[] cols = lines[currentLine].Split(" ");
                        var node = new Node()
                        {
                            Index = index,
                            X = float.Parse(cols[1]),
                            Y = float.Parse(cols[2]),
                            Z = float.Parse(cols[3]),
                            Angle = (float)(Math.PI /16.0) * float.Parse(cols[3]) * 0.1f,
                        };
                        this.NodesOrigin[index] = node;
                    }
                }
                else if (lines[currentLine] == "$Elements")
                {
                    currentLine += 1;
                    var elementsNumber = int.Parse(lines[currentLine]);
                    elements = new int[elementsNumber][];
                    for (int index = 0; index < elementsNumber; index++)
                    {
                        currentLine += 1;
                        string[] splittedLine = lines[currentLine].Split(" ");
                        var array = new int[splittedLine.Length];
                        for (int c = 0; c < splittedLine.Length; c++)
                        {
                            array[c] = int.Parse(splittedLine[c]);
                        }
                        elements[index] = array;
                    }
                }


            }
            if (elements == null)
            {
                //Debug.WriteLine("No ---------------");
            }
            return (elements, physicalInfos);
        }
    }
}
