import numpy as np
from numpy import linalg as la

def polyToGraph(polygons):
#   print("polygon id and verts");
#   print(polygons[1]);
#   print("num of gons");
#   print(len(polygons));
#   print("vertices");
#   print(polygons[1][1]);
#   print("num vertices");
#   print(len(polygons[1][1]));
#   print("one vertex");
#   print(polygons[1][1][1]);
#   print("difference of vertices");
#   print(polygons[1][1][1] - polygons[1][1][2]);
#   print("dimensions of vertex");
#   print(len(polygons[1][1][1]));
#   print("y pos of vertex");
#   print(polygons[1][1][1][1]);
#   print("f");
#
#   print("idk");
   graph = [];
   # iterate over polygons
   for i in range(len(polygons)):
      # iterate over all over polygons/verts
      for k in range((i+1), len(polygons)):
         # track polygon has dist 1
         distOne = 0;
         hasLess = 0;
         hasGreater = 0;
         # iterate over vertices
         for j in range(len(polygons[i][1])):
            # iterate over vertices
            for l in range(len(polygons[k][1])):
               dist = la.norm(polygons[i][1][j] - polygons[k][1][l], 2) * 0.4;
               print(i, j, k, l);
               print(polygons[i][1][j]);
               print(dist);
               if (dist < 1.0):
                  hasLess = 1;
               elif (dist > 1.0):
                  hasGreater = 1;
               elif (dist == 1.0):
                  distOne = 1;
            if ((hasLess == 1) and (hasGreater == 1)):
               distOne = 1;
         if (distOne == 1):
            # graph.append((i, j));
            graph.append((polygons[i][0], polygons[k][0]));
   return graph;

# graph of edges
# k colors
def printCNF(graph, k):
   file = open("tile.cnf","w+")
   n = max(graph);
   n = max(n);
   n += 1;
   m = len(graph);
   file.write("p cnf %d %d\n" % (n*k, n + m*k));
   print(n);
   for i in range(n):
      mustHaveColorString = "";
      for j in range(1, k+1):
         mustHaveColorString += ("%d " % (i*k + j));
      mustHaveColorString += "0\n";
      file.write(mustHaveColorString);
   for i in range(m):
      for j in range(1, k+1):
         vert1 = graph[i][0] - 1;
         vert2 = graph[i][1] - 1;
         file.write("-%d -%d 0\n" % (vert1 * k + j, vert2 * k + j));
               


vertList = [];
# list of 4 squares
vertList.append([1, np.array([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]);
vertList.append([2, np.array([(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (1.0, 1.0)])]);
vertList.append([3, np.array([(1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 0.0)])]);
vertList.append([4, np.array([(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)])]);

print(vertList);
graph = polyToGraph(vertList);
print(graph);
printCNF(graph, 6);




