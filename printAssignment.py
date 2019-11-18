import numpy as np
from numpy import linalg as la
import math
import copy
from graphics import *

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

def displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum, edgeLength, percentWiggle):
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
         xCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
         xCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
         yCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
         yCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
         shrunkPoints = np.array(shrinkShape(xCen, yCen, edgeLength*percentWiggle));
         for j in range(len(shrunkPoints)):
            scaledPoints.append(Point(shrunkPoints[j][0] * scaling, shrunkPoints[j][1] * scaling));
         print("scaledPoints");
         print(scaledPoints);
         rect = Polygon(scaledPoints);
      # set color from number
      if (colorNum == 1):
         rect.setOutline('red');
         rect.setFill('red');
      elif (colorNum == 2):
         rect.setOutline('blue');
         rect.setFill('blue');
      elif (colorNum == 3):
         rect.setOutline('orange');
         rect.setFill('orange');
      elif (colorNum == 4):
         rect.setOutline('yellow');
         rect.setFill('yellow');
      elif (colorNum == 5):
         rect.setOutline('green');
         rect.setFill('green');
      elif (colorNum == 6):
         rect.setOutline('cyan');
         rect.setFill('cyan');
      elif (colorNum == 7):
         rect.setOutline('magenta');
         rect.setFill('magenta');
      else:
         print("invalid asisngment or color");
      rect.draw(win);
   # draw line
   line = Line(Point(0.00 * scaling, 0.05 * scaling), Point(1.0 * scaling, 0.05 * scaling));
   line.setOutline('white');
   line.draw(win);

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

# colors
k = 6;
# edge number, sides of the polygon
gonNum = 6;
edgeLength = 0.05;
percentWiggle = 0.7;
#gridSize = 1;
gridWidth = 4;
gridHeight = 4;
(vertList, indexMap) = generate_normal_shape(gonNum, edgeLength, gridWidth, gridHeight)

assignment = readAssignemnt("cadicalOut.txt"); #satAssignment.txt
print("assignment");
print(assignment);
displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum, edgeLength, 1);
