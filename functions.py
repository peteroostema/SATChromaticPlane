import numpy as np
from numpy import linalg as la
import math
import copy

#def generate_normal_shape(num_of_edges, edge_length, plane_size):
#    shape_list = []
#    if num_of_edges == 4:
#        shape = [1, np.array([(0,0),(0,edge_length),(edge_length,edge_length),(edge_length,0)])]
#        shape_list.append(shape)
#        col = int(math.floor(plane_size/edge_length))
#        firstOfRow = shape[:];
#        for i in range(col):
#            new_shape = firstOfRow.copy();
#            new_shape[0] += i*col;
#            for k in range(num_of_edges):
#               new_shape[1][k] += (0, i*edge_length);
#            print("firstOfRow");
#            print(firstOfRow);
#            print("new_shape");
#            print(new_shape);
#            for j in range(col):
#               new_shape[0] += 1;
#               for k in range(num_of_edges):
#                  new_shape[1][k] = new_shape[1][k] + (edge_length, 0);
#               #add_new = new_shape[:]
#               add_new = new_shape.copy();
#               print(add_new);
#               shape_list.append(add_new.copy())
#               #shape = add_new[:]
#    return shape_list

def makeSquare(xCord, yCord, edge_length):
   return np.array([(xCord,yCord),(xCord, yCord + edge_length),(xCord + edge_length, yCord + edge_length),(xCord + edge_length, yCord)]);


def generate_normal_shape(num_of_edges, edge_length, plane_size):
    shape_list = []
    if num_of_edges == 4:
        #shape = [1, np.array([(0,0),(0,edge_length),(edge_length,edge_length),(edge_length,0)])]
        col = int(math.ceil(plane_size/edge_length))
        for i in range(col):
            for j in range(col):
               npArray = makeSquare(i*edge_length, j*edge_length, edge_length);
               shape_list.append([i*col + j, npArray.copy()])
    return shape_list

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
               dist = la.norm(polygons[i][1][j] - polygons[k][1][l], 2);
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
               

vertList = generate_normal_shape(4, 0.51, 2)
#vertList = [];
# list of 4 squares
#vertList.append([1, np.array([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]);
#vertList.append([2, np.array([(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (1.0, 1.0)])]);
#vertList.append([3, np.array([(1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 0.0)])]);
#vertList.append([4, np.array([(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)])]);
print("vertList");
print(vertList);
graph = polyToGraph(vertList);
print("graph")
print(graph);
printCNF(graph, 6);




