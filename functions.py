import numpy as np
from numpy import linalg as la
import math
import copy
from graphics import *

def makeHexagon(xCord, yCord, edge_length, plane_width, plane_height, shape_list):
   print("startPos");
   print((xCord, yCord));
   
   pointArray = [];
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord - edge_length, yCord));
   pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
   pointArray.append((xCord + edge_length, yCord));
   pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   for i in range(len(pointArray)):
      #print("bf");
      #print(pointArray[i]);
      for j in range(len(pointArray[i])):
         #print("i");
         #print(i);
         #print("j");
         #print(j);
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
   print(pointArray);

   #shape_list.append([shapeNum, np.array(pointArray)])
   #shapeNum += 1;
   return np.array(pointArray);


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
    if num_of_edges == 4:
       #shape = [1, np.array([(0,0),(0,edge_length),(edge_length,edge_length),(edge_length,0)])]
       col = int(math.ceil(plane_width/edge_length));
       row = int(math.ceil(plane_height/edge_length));
       for i in range(col):
          for j in range(row):
             npArray = makeSquare(i*edge_length, j*edge_length, edge_length, plane_width, plane_height);
             shape_list.append([i*row + j + 1, npArray.copy()]);
    if num_of_edges == 6:
      hexHeight = edge_length*math.sqrt(0.75);
      hexWidth = 3*edge_length;
      #shape = [1, np.array([(0,0),(0,edge_length),(edge_length,edge_length),(edge_length,0)])]
      col = int(math.ceil(plane_width/hexWidth));
      row = int(math.ceil(plane_height/hexHeight));
      for i in range(col):
         for j in range(row):
            npArray = np.empty;
            if ((j % 2) == 0):
               npArray = makeHexagon(i*hexWidth, j*hexHeight, edge_length, plane_width, plane_height, shape_list);
            else:
               npArray = makeHexagon((i+0.5)*hexWidth, j*hexHeight, edge_length, plane_width, plane_height, shape_list);
            shape_list.append([i*row + j + 1, npArray.copy()]);
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
               #print(i, j, k, l);
               #print(polygons[i][1][j]);
               #print(dist);
               if (dist < 1.0):
                  hasLess = 1;
               elif (dist > 1.0):
                  hasGreater = 1;
               elif (dist == 1.0):
                  if ((j < int(math.floor(len(polygons[i][1]) / 2))) or (l < math.floor(len(polygons[k][1])))):
                     # assume two open faces not on opposite sides
                     hasGreater = 1;
                  else:
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
   line.draw(win);


# colors
k = 6;
# edge number, sides of the polygon
gonNum = 6;
#gridSize = 1;
gridWidth = 2;
gridHeight = 2;
vertList = generate_normal_shape(gonNum, 0.1, gridWidth, gridHeight)
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
printCNF(graph, k);

name = input("Enter to proceed ")

assignment = readAssignemnt("cadicalOut.txt"); #satAssignment.txt
print("assignment");
print(assignment);
displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum);

name = input("Enter to close ")

