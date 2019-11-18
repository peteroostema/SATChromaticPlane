import numpy as np
from numpy import linalg as la
import math
import copy
from graphics import *

col = 0;
row = 0;

def makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1):
   xCord = index0 * edge_length * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
   xCord += index1 * edge_length * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
   yCord = index0 * edge_length * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
   yCord += index1 * edge_length * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   #print("startPos");
   #print((xCord, yCord));
   
   # check center in bounds
   if ((xCord > plane_width) or (xCord < 0) or (yCord > plane_height) or (yCord < 0)):
         return shapeNum;

   for gon in shape_list:
      if ((gon[2] == index0) and (gon[3] == index1)):
         return shapeNum;
   
   pointArray = [];
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord - edge_length, yCord));
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length, yCord));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   # adjust verticies to bounds
   for i in range(len(pointArray)):
      #print("bf");
      #print(pointArray[i]);
      for j in range(len(pointArray[i])):
         if (pointArray[i][j] < 0.0):
            #pointArray[i][j] = 0.0;
            if (j == 0):
               pointArray[i] = (0.0, pointArray[i][j+1]);
            else:
               pointArray[i] = (pointArray[i][j-1], 0.0);
      if (pointArray[i][0] > plane_width):
         #pointArray[i][j] = plane_width;
         pointArray[i] = (plane_width, pointArray[i][1]);
      if (pointArray[i][1] > plane_height):
         pointArray[i] = (pointArray[i][0], plane_height);
      #print("af");
      #print(pointArray[i]);
#   print(pointArray);
#   print("index");
#   print(index0);
#   print(index1);
#   print(xCord);
#   print(yCord);

   shape_list.append([shapeNum, np.array(pointArray), index0, index1])
   indexMap.update({(index0, index1): shapeNum});
   shapeNum += 1;
   shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0+1, index1);
   shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0-1, index1);
   shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1+1);
   shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1-1);
   return shapeNum;
   #shapeNum += 1;
   #return np.array(pointArray);


def makeSquare(xCord, yCord, edge_length, plane_width, plane_height):
   xMax = xCord + edge_length;
   if (xMax > plane_width):
      xMax = plane_width;
   yMax = yCord + edge_length
   if (yMax > plane_height):
      yMax = plane_height;
   return np.array([(xCord,yCord),(xCord, yMax),(xMax, yMax),(xMax, yCord)]);


def generate_normal_shape(num_of_edges, edge_length, plane_width, plane_height):
   shape_list = []
   indexMap = {};
   global col
   global row
   if num_of_edges == 4:
      #shape = [1, np.array([(0,0),(0,edge_length),(edge_length,edge_length),(edge_length,0)])]
      col = int(math.ceil(plane_width/edge_length));
      row = int(math.ceil(plane_height/edge_length));
      for i in range(col):
         for j in range(row):
            npArray = makeSquare(i*edge_length, j*edge_length, edge_length, plane_width, plane_height);
            shape_list.append([i*row + j + 1, npArray.copy()]);
   if num_of_edges == 6:
      shapeNum = 0;
      index0 = 0;
      index1 = 0;
      shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1);
   return (shape_list, indexMap);

# hexagons only
def shrinkShape(xCord, yCord, edge_length):
   pointArray = [];
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord - edge_length, yCord));
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length, yCord));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   return pointArray;

def polyToGraphCenReduce(polygons, indexMap, edgeLength, percentWiggle):
   graph = [];
   
   # ensure center is on a primary column
   maxCol = 0;
   maxRow = 0;
   for gon in polygons:
      xCord = gon[1][0][0];
      yCord = gon[1][0][1];
      print("cords");
      print(xCord);
      print(yCord);
      if (xCord > 1):
         if (yCord > 1):
            centerID = indexMap[(gon[2], gon[3]+1)];
            break;
   colID = math.ceil(0.5*maxCol);

   print("centerID");
   print(centerID);

   # just check all possiblities
   circleIDs = [];
   # shape_list.append([shapeNum, np.array(pointArray), index0, index1])
   # check dist of center
   xCenCen = polygons[centerID][2] * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
   xCenCen += polygons[centerID][3] * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
   yCenCen = polygons[centerID][2] * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
   yCenCen += polygons[centerID][3] * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   centerPoints = np.array(shrinkShape(xCenCen, yCenCen, edgeLength*percentWiggle));
   #circleIDs = dfsFindCircle(polygons, centerID, id, circleIDs);
   for k in range(len(polygons)):
      hasLess = 0;
      hasGreater = 0;
      distOne = 0;
      
      xCenK = polygons[k][2] * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
      xCenK += polygons[k][3] * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
      yCenK = polygons[k][2] * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
      yCenK += polygons[k][3] * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
      searchPoints = np.array(shrinkShape(xCenK, yCenK, edgeLength*percentWiggle));
      cenDist = la.norm((xCenCen - xCenK, yCenCen - yCenK), 2);
      for i in range(len(centerPoints)):
         for j in range(len(searchPoints)):
            dist = la.norm(centerPoints[i] - searchPoints[j], 2);
            #print(i, j, k, l);
            #print(polygons[i][1][j]);
            #print(dist);
            if (dist < 1.0):
               hasLess = 1;
            elif (dist > 1.0):
               hasGreater = 1;
            elif (dist == 1.0):
               if ((i < int(math.floor(len(polygons[centerID][1]) / 2))) and (j < int(math.floor(len(polygons[k][1]) / 2)))):
                  # assume two open faces not on opposite sides
                  hasGreater = 1;
               else:
                  distOne = 1;
         if ((hasLess == 1) and (hasGreater == 1)):
            distOne = 1;
      if (distOne == 1):
         # graph.append((i, j));
         #if polygons[k][0] not in circleIDs :
         #   circleIDs.append(polygons[k][0]);
         if k not in circleIDs :
            circleIDs.append(k);
   print("circleIDs");
   print(circleIDs);
   circleOffsets = [];
   for i in range(len(circleIDs)):
      circleOffsets.append((-polygons[centerID][2] + polygons[circleIDs[i]][2], -polygons[centerID][3] + polygons[circleIDs[i]][3]));
   print("circleOffsets");
   print(circleOffsets);

   agumentedOffsets = [];
   print("row col");
   print(row);
   print(col);
   # check circles offset from each polygon
   for i in range(len(polygons)):
      for j in range(len(circleOffsets)):
         destI = polygons[i][2] + circleOffsets[j][0];
         destJ = polygons[i][3] + circleOffsets[j][1];
         try:
            shapeID = indexMap[(destI, destJ)];
            print("shapeID");
            print(shapeID);
            if (shapeID):
               graph.append((i+1, shapeID+1));
         except KeyError as error:
            error = 0;
   print("graph");
   print(graph);
   return graph;

# graph of edges
# k colors
def printCNF(graph, k):
   file = open("tile.cnf","w+")
   #n = max(graph);
   #n = max(max(graph)[0], max(graph)[1]);
   n = 0;
   for i in range(len(graph)):
      if (n < graph[i][0]):
         n = graph[i][0];
      if (n < graph[i][1]):
         n = graph[i][1];
   print(n);
   #n = max(n);
   #n += 1;
   m = len(graph);
   file.write("p cnf %d %d\n" % (n*k, n + m*k));
   print("n");
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
         
# colors
k = 6;
# edge number, sides of the polygon
gonNum = 6;
edgeLength = 0.05;
percentWiggle = 0.7;
#gridSize = 1;
gridWidth = 4;
gridHeight = 4;
print(sys.getrecursionlimit());
sys.setrecursionlimit(40000);
# format: filename edgeLength percentWiggle gonNum gridWidth gridHeight
print(len(sys.argv));
for i in range(len(sys.argv)):
   print(sys.argv[i]);
   if (i == 1):
      edgeLength = sys.argv[i];
   elif (i == 2):
      percentWiggle = sys.argv[i];
   elif (i == 3):
      gonNum = sys.argv[i];
   elif (i == 4):
      gridWidth = sys.argv[i];
      gridHeight = sys.argv[i];
   elif (i == 5):
      gridHeight = sys.argv[i];
(vertList, indexMap) = generate_normal_shape(gonNum, edgeLength, gridWidth, gridHeight)
#vertList = [];
# list of 4 squares
#vertList.append([1, np.array([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]);
#vertList.append([2, np.array([(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (1.0, 1.0)])]);
#vertList.append([3, np.array([(1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 0.0)])]);
#vertList.append([4, np.array([(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)])]);
print("vertList");
print(vertList);
#graph = polyToGraph(vertList, indexMap);
graph = polyToGraphCenReduce(vertList, indexMap, edgeLength, percentWiggle)
print("graph")
print(graph);
printCNF(graph, k);


