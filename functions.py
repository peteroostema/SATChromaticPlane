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

def dfsOneDist(polygons, centerID, thisID):
   id = 0;
   # check for 1 dist away
   hasLess = 0;
   hasGreater = 0;
   distOne = 0;
   for i in range(len(polygons[centerID][1])):
      # iterate over vertices
      for j in range(len(polygons[thisID][1])):
         dist = la.norm(polygons[centerID][1][i] - polygons[thisID][1][j], 2);
         #print(i, j, k, l);
         #print(polygons[i][1][j]);
         #print(dist);
         if (dist < 1.0):
            hasLess = 1;
         elif (dist > 1.0):
            hasGreater = 1;
         elif (dist == 1.0):
            if ((i < int(math.floor(len(polygons[centerID][1]) / 2))) and (j < int(math.floor(len(polygons[thisID][1]) / 2)))):
            #if ((i < int(math.floor(len(polygons[centerID][1]) / 2))) or (j < math.floor(len(polygons[thisID][1])))):
               # assume two open faces not on opposite sides
               hasGreater = 1;
            else:
               distOne = 1;
      if ((hasLess == 1) and (hasGreater == 1)):
         distOne = 1;
   if (distOne == 1):
      # graph.append((i, j));
      return thisID;
   for i in range(len(polygons[thisID][4])): # negihbors
      id = dfsOneDist(polygons, centerID, polygons[thisID][4][i]);
      #print("id");
      #print(id);
      if (id != 0):
         return id;

def dfsFindCircle(polygons, centerID, searchID, circleIDs):
   # check dist 1
   # check for 1 dist away
   hasLess = 0;
   hasGreater = 0;
   distOne = 0;
   for i in range(len(polygons[centerID][1])):
      # iterate over vertices
      for j in range(len(polygons[searchID][1])):
         dist = la.norm(polygons[centerID][1][i] - polygons[searchID][1][j], 2);
         #print(i, j, k, l);
         #print(polygons[i][1][j]);
         #print(dist);
         if (dist < 1.0):
            hasLess = 1;
         elif (dist > 1.0):
            hasGreater = 1;
         elif (dist == 1.0):
            if ((i < int(math.floor(len(polygons[i][1]) / 2))) or (j < math.floor(len(polygons[j][1])))):
               # assume two open faces not on opposite sides
               hasGreater = 1;
            else:
               distOne = 1;
      if ((hasLess == 1) and (hasGreater == 1)):
         distOne = 1;
   if (distOne == 1):
      # graph.append((i, j));
      #if (searchID+1) not in circleIDs :
      #   circleIDs.append(searchID + 1);
      if searchID not in circleIDs :
         circleIDs.append(searchID);
      else:
         return circleIDs;
   else:
      return circleIDs;
   for i in range(len(polygons[searchID][4])): # negihbors
      circleIDs = dfsFindCircle(polygons, centerID, polygons[searchID][4][i], circleIDs);
      #print("searchID");
      #print(searchID);
   return circleIDs;

def polyToGraph(polygons, indexMap):
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
   
   # DFS for hexagon 1 dist away
   
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
   #if ((colID % 2) == 1):
   #   colID += 1;
   #centerID = colID*maxRow + math.ceil(0.5*maxRow);# + 1;
   print("centerID");
   print(centerID);
#   print(polygons[centerID][2]);
#   print(polygons[centerID][3]);
#   id = dfsOneDist(polygons, centerID, centerID);
#   circleIDs = [];
#   circleIDs = dfsFindCircle(polygons, centerID, id, circleIDs);
#   print("circleIDs");
#   print(circleIDs);
#   circleOffsets = [];
#   for i in range(len(circleIDs)):
#      #print("i's j's, dif");
#      #print(polygons[centerID][2]);
#      #print(polygons[i][2]);
#      #print(polygons[centerID][3]);
#      #print(polygons[i][3]);
#      #print(polygons[centerID][2] - polygons[i][2]);
#      #print(polygons[centerID][3] - polygons[i][3]);
#      circleOffsets.append((-polygons[centerID][2] + polygons[circleIDs[i]][2], -polygons[centerID][3] + polygons[circleIDs[i]][3]));
#   print("circleOffsets");
#   print(circleOffsets);

   # just check all possiblities
   circleIDs = [];
   #circleIDs = dfsFindCircle(polygons, centerID, id, circleIDs);
   for k in range(len(polygons)):
      hasLess = 0;
      hasGreater = 0;
      distOne = 0;
      # iterate over vertices
      for i in range(len(polygons[centerID][1])):
         for j in range(len(polygons[k][1])):
            dist = la.norm(polygons[centerID][1][i] - polygons[k][1][j], 2);
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
         #if (((polygons[i][2] % 2) == 1) and ((destI % 2) == 0)):#((circleOffsets[j][1] % 2) == 1)):
            #if (circleOffsets[j][1] > 0):
            #   destI += 1;
            #else:
            #destI -= 1;
         #print("pos");
         #print((polygons[i][2], polygons[i][3]));
         #print(circleOffsets[j])
         #print("destIJ");
         #print((destI, destJ));
         #if ((col > destI >= 0) and (row > destJ >= 0)):
         #   if ((destI >= polygons[i][2]) and (destJ >= polygons[i][3]) ):
         #      graph.append((i+1, destI*row + destJ + 1));
         #      # con to 11, 2,
         try:
            shapeID = indexMap[(destI, destJ)];
            print("shapeID");
            print(shapeID);
            if (shapeID):
               graph.append((i+1, shapeID+1));
         except KeyError as error:
            error = 0;
   i = (row+1);
   print(polygons[i][2]);
   for j in range(len(circleOffsets)):
      destI = circleOffsets[j][0];
      destJ = circleOffsets[j][1];
      if ((polygons[i][2] % 2) == 1) and ((circleOffsets[j][1] % 2) == 1):
         #if (circleOffsets[j][1] > 0):
         #   destI += 1;
         #else:
         destI -= 1;
      agumentedOffsets.append((destI, destJ));
   print("agumentedOffsets");
   print(agumentedOffsets);
   print("graph");
   print(graph);
   
#   graph = [];
#   # iterate over polygons
#   for i in range(len(polygons)):
#      # iterate over all over polygons/verts
#      for k in range((i+1), len(polygons)):
#         # track polygon has dist 1
#         distOne = 0;
#         hasLess = 0;
#         hasGreater = 0;
#         # iterate over vertices
#         for j in range(len(polygons[i][1])):
#            # iterate over vertices
#            for l in range(len(polygons[k][1])):
#               dist = la.norm(polygons[i][1][j] - polygons[k][1][l], 2);
#               #print(i, j, k, l);
#               #print(polygons[i][1][j]);
#               #print(dist);
#               if (dist < 1.0):
#                  hasLess = 1;
#               elif (dist > 1.0):
#                  hasGreater = 1;
#               elif (dist == 1.0):
#                  if ((j < int(math.floor(len(polygons[i][1]) / 2))) and (l < int(math.floor(len(polygons[j][1]) / 2)))):
#                     # assume two open faces not on opposite sides
#                     hasGreater = 1;
#                  else:
#                     distOne = 1;
#            if ((hasLess == 1) and (hasGreater == 1)):
#               distOne = 1;
#         if (distOne == 1):
#            # graph.append((i, j));
#            graph.append((polygons[i][0]+1, polygons[k][0]+1));
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

# copy/paste file
#def readAssignemnt(satFile):
#   with open(satFile) as file:
#      #w, h = [int(x) for x in next(f).split()] # read first line
#      assignment = []
#      for line in file: # read rest of lines
#         #assignment.append([int(x) for x in line.split()])
#         for x in line.split():
#            assignment.append(int(x));
#   return assignment;

# read from cadical output
def readAssignemnt(satFile):
   with open(satFile) as file:
      fileInString = file.read()
      #print(fileInString.split("\ns ",1));
      outputSecondHalf = fileInString.split("\ns ", 1)[1];
      assignmentText = outputSecondHalf.split("\nc ", 1)[0];
      print("assignmentText");
      print(assignmentText);
      #w, h = [int(x) for x in next(f).split()] # read first line
      assignment = []

      for x in assignmentText.split():
         #print("x");
         #print(x);
         if (x == "UNSATISFIABLE"):
            print("UNSAT");
         elif (x == "SATISFIABLE"):
            print("SAT");
         elif (not(x == "v")):
            assignment.append(int(x));
   return assignment;

def displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum):
   basePixels = 600;
   win = GraphWin("test", basePixels, basePixels * (gridHeight/gridWidth));
   n = len(vertList);
   scaling = basePixels/gridWidth;
   for i in range(n):
      # find color #
      colorNum = 0;
      counter = 0;
      for j in range(i*k, (i+1)*k):
         counter += 1;
         print("assignemnt[j]");
         print(assignment[j]);
         if (assignment[j] > 0):
            colorNum = counter;
      if (gonNum == 4):
         # make rectangle with opposite corners
         print("points");
   #      print(vertList[i][1][0]);
   #      print(vertList[i][1][2]);
   #      print(tuple(vertList[i][1][2]));
   #      #print(Point(tuple(vertList[i][1][2])));
   #      print(Point(vertList[i][1][0][0], vertList[i][1][2][1]));
         pt1 = Point(vertList[i][1][0][0] * scaling, vertList[i][1][0][1] * scaling);
         pt2 = Point(vertList[i][1][2][0] * scaling, vertList[i][1][2][1] * scaling);
         print(pt1);
         print(pt2);
         print(colorNum);
         rect = Rectangle(pt1, pt2);
      elif (gonNum == 6):
         scaledPoints = [];
         for j in range(len(vertList[i][1])):
            scaledPoints.append(Point(vertList[i][1][j][0] * scaling, vertList[i][1][j][1] * scaling));
         print("scaledPoints");
         print(scaledPoints);
         rect = Polygon(scaledPoints);
      # set color from number
      if (colorNum == 1):
         rect.setOutline('black');
         rect.setFill('red');
      elif (colorNum == 2):
         rect.setOutline('black');
         rect.setFill('blue');
      elif (colorNum == 3):
         rect.setOutline('black');
         rect.setFill('orange');
      elif (colorNum == 4):
         rect.setOutline('black');
         rect.setFill('yellow');
      elif (colorNum == 5):
         rect.setOutline('black');
         rect.setFill('green');
      elif (colorNum == 6):
         rect.setOutline('black');
         rect.setFill('cyan');
      elif (colorNum == 7):
         rect.setOutline('black');
         rect.setFill('magenta');
      else:
         print("invalid asisngment or color");
      rect.draw(win);
   # draw line
   line = Line(Point(0.00 * scaling, 0.05 * scaling), Point(1.0 * scaling, 0.05 * scaling));
   line.setOutline('white');
   line.draw(win);


# colors
k = 7;
# edge number, sides of the polygon
gonNum = 6;
#gridSize = 1;
gridWidth = 6;
gridHeight = 6;
(vertList, indexMap) = generate_normal_shape(gonNum, 0.1, gridWidth, gridHeight)
#vertList = [];
# list of 4 squares
#vertList.append([1, np.array([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]);
#vertList.append([2, np.array([(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (1.0, 1.0)])]);
#vertList.append([3, np.array([(1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 0.0)])]);
#vertList.append([4, np.array([(1.0, 1.0), (1.0, 2.0), (2.0, 2.0), (2.0, 1.0)])]);
print("vertList");
print(vertList);
graph = polyToGraph(vertList, indexMap);
print("graph")
print(graph);
printCNF(graph, k);

name = input("Enter to proceed ")

assignment = readAssignemnt("cadicalOut.txt"); #satAssignment.txt
print("assignment");
print(assignment);
displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum);

name = input("Enter to close ")

