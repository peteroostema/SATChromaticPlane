import sys
import numpy as np
from numpy import linalg as la
import math
import copy
from graphics import *
from pysat.solvers  import Cadical, Solver
from pysat.formula import CNF
from graphics import *

col = 0;
row = 0;

def makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0, index1):
   xCord = index0 * edge_length * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
   xCord += index1 * edge_length * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
   yCord = index0 * edge_length * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
   yCord += index1 * edge_length * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   #print("startPos");
   #print((xCord, yCord));
   
   # check center in bounds
   if (la.norm((xCord, yCord), 2) > radius):
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
#   for i in range(len(pointArray)):
#      #print("bf");
#      #print(pointArray[i]);
#      for j in range(len(pointArray[i])):
#         if (pointArray[i][j] < 0.0):
#            #pointArray[i][j] = 0.0;
#            if (j == 0):
#               pointArray[i] = (0.0, pointArray[i][j+1]);
#            else:
#               pointArray[i] = (pointArray[i][j-1], 0.0);
#      if (pointArray[i][0] > plane_width):
#         #pointArray[i][j] = plane_width;
#         pointArray[i] = (plane_width, pointArray[i][1]);
#      if (pointArray[i][1] > plane_height):
#         pointArray[i] = (pointArray[i][0], plane_height);

   shape_list.append([shapeNum, np.array(pointArray), index0, index1])
   indexMap.update({(index0, index1): shapeNum});
   shapeNum += 1;
   shapeNum = makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0+1, index1);
   shapeNum = makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0-1, index1);
   shapeNum = makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0, index1+1);
   shapeNum = makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0, index1-1);
   return shapeNum;
   #shapeNum += 1;
   #return np.array(pointArray);

def generate_normal_shapeDisc(num_of_edges, edge_length, radius):
   shape_list = []
   indexMap = {};
   if num_of_edges == 6:
      shapeNum = 0;
      index0 = 0;
      index1 = 0;
      shapeNum = makeHexagonDisc(edge_length, radius, shape_list, indexMap, shapeNum, index0, index1);
   return (shape_list, indexMap);


def makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1):
   xCord = index0 * edge_length * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
   xCord += index1 * edge_length * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
   yCord = index0 * edge_length * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
   yCord += index1 * edge_length * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   #print("startPos");
   #print((xCord, yCord));
   
   # check center in bounds
   if ((xCord > plane_width + edge_length) or (xCord < 0 - edge_length) or (yCord > plane_height + edge_length) or (yCord < 0 - edge_length)):
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


def makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1):
   xCord = index0 * edge_length;
   yCord = index1 * edge_length;
   #print("startPos");
   #print((xCord, yCord));
   
   # check center in bounds
   if ((xCord >= plane_width) or (xCord <= 0 - edge_length) or (yCord >= plane_height) or (yCord <= 0 - edge_length)):
         return shapeNum;

   for gon in shape_list:
      if ((gon[2] == index0) and (gon[3] == index1)):
         return shapeNum;
   
   pointArray = [];
   pointArray.append((xCord, yCord));
   pointArray.append((xCord + edge_length, yCord));
   pointArray.append((xCord, yCord + edge_length));
   pointArray.append((xCord + edge_length, yCord + edge_length));

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

   shape_list.append([shapeNum, np.array(pointArray), index0, index1])
   indexMap.update({(index0, index1): shapeNum});
   shapeNum += 1;
   shapeNum = makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0+1, index1);
   shapeNum = makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0-1, index1);
   shapeNum = makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1+1);
   shapeNum = makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1-1);
   return shapeNum;

def generate_normal_shape(num_of_edges, edge_length, plane_width, plane_height):
   shape_list = []
   indexMap = {};
   global col
   global row
   if num_of_edges == 4:
      shapeNum = 0;
      index0 = 0;
      index1 = 0;
      shapeNum = makeSquare(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1);
   if num_of_edges == 6:
      shapeNum = 0;
      index0 = 0;
      index1 = 0;
      shapeNum = makeHexagon(edge_length, plane_width, plane_height, shape_list, indexMap, shapeNum, index0, index1);
   return (shape_list, indexMap);

def dfsOneDist(cenID1, cenID2, searchID1, searchID2, edgeLength, gonNum):
   dist1ID = (0,0);
   # check for 1 dist away
   hasLess = 0;
   hasGreater = 0;
   distOne = 0;

   if (gonNum == 6):
      xCenCen = cenID1 * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
      xCenCen += cenID2 * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
      yCenCen = cenID1 * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
      yCenCen += cenID2 * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
      xCenK = searchID1 * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
      xCenK += searchID2 * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
      yCenK = searchID1 * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
      yCenK += searchID2 * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   elif (gonNum == 4):
      xCenCen = cenID1 * edgeLength;
      yCenCen = cenID2 * edgeLength;
      xCenK = searchID1 * edgeLength;
      yCenK = searchID2 * edgeLength;
   centerPoints = np.array(shrinkShape(xCenCen, yCenCen, edgeLength*1, gonNum));
   searchPoints = np.array(shrinkShape(xCenK, yCenK, edgeLength*1, gonNum));
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
            if ((i < int(math.floor(gonNum / 2))) and (j < int(math.floor(gonNum / 2)))):
               # assume two open faces not on opposite sides
               hasGreater = 1;
            else:
               distOne = 1;
      if ((hasLess == 1) and (hasGreater == 1)):
         distOne = 1;
   if (distOne == 1):
      # graph.append((i, j));
      return (searchID1, searchID2);
   dist1ID = dfsOneDist(cenID1, cenID2, searchID1+1, searchID2, edgeLength, gonNum);
   if (dist1ID != (0,0)):
      return dist1ID;
#   for i in range(len(polygons[thisID][4])): # negihbors
#      dist1ID = dfsOneDist(id1+1, id2);
#      #print("id");
#      #print(id);
#      if (dist1ID != (0,0)):
#         return dist1ID;


def dfsFindCircle(cenID1, cenID2, searchID1, searchID2, edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum):
   # return if this has been visited before
   if (searchID1, searchID2) not in visitedIDs :
      visitedIDs.append((searchID1, searchID2));
   else:
      return circleIDs;

   # check dist 1
   # check for 1 dist away
   hasLess = 0;
   hasGreater = 0;
   distOne = 0;
   
   if (gonNum == 6):
      xCenCen = cenID1 * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
      xCenCen += cenID2 * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
      yCenCen = cenID1 * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
      yCenCen += cenID2 * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
      xCenK = searchID1 * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
      xCenK += searchID2 * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
      yCenK = searchID1 * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
      yCenK += searchID2 * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
   elif (gonNum == 4):
      xCenCen = cenID1 * edgeLength;
      yCenCen = cenID2 * edgeLength;
      xCenK = searchID1 * edgeLength;
      yCenK = searchID2 * edgeLength;
   centerPoints = np.array(shrinkShape(xCenCen, yCenCen, edgeLength*1, gonNum));
   searchPoints = np.array(shrinkShape(xCenK, yCenK, edgeLength*1, gonNum));
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
            if ((i > int(math.floor(gonNum / 2))) and (j > int(math.floor(gonNum / 2)))):
               distOne = 1;
            else:
               # assume two open faces not on opposite sides
               hasGreater = 1;
      if ((hasLess == 1) and (hasGreater == 1)):
         distOne = 1;
   if (distOne == 1):
      a = 0;
   else:
      return circleIDs;

   # check connection on graph with reduced shapes
   hasLess = 0;
   hasGreater = 0;
   distOne = 0;
   centerPoints = np.array(shrinkShape(xCenCen, yCenCen, edgeLength*percentWiggle, gonNum));
   searchPoints = np.array(shrinkShape(xCenK, yCenK, edgeLength*percentWiggle, gonNum));
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
            if ((i > int(math.floor(gonNum / 2))) and (j > int(math.floor(gonNum / 2)))):
               distOne = 1;
            else:
               # assume two open faces not on opposite sides
               hasGreater = 1;
      if ((hasLess == 1) and (hasGreater == 1)):
         distOne = 1;
   if (distOne == 1):
      # graph.append((i, j));
      if (searchID1, searchID2) not in circleIDs :
         circleIDs.append((searchID1, searchID2));
      else:
         return circleIDs;
   
   #print("searchIDs");
   #print(searchID1);
   #print(searchID2);
   circleIDs = dfsFindCircle(cenID1, cenID2, searchID1+1, searchID2, edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum);
   circleIDs = dfsFindCircle(cenID1, cenID2, searchID1, searchID2+1, edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum);
   circleIDs = dfsFindCircle(cenID1, cenID2, searchID1-1, searchID2, edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum);
   circleIDs = dfsFindCircle(cenID1, cenID2, searchID1, searchID2-1, edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum);
   #for i in range(len(polygons[searchID][4])): # negihbors
   #   circleIDs = dfsFindCircle(polygons, centerID, polygons[searchID][4][i], circleIDs);
      #print("searchID");
      #print(searchID);
   return circleIDs;

# hexagons only
def shrinkShape(xCord, yCord, edge_length, gonNum):
   pointArray = [];
   if (gonNum == 6):
      pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
      pointArray.append((xCord - edge_length, yCord));
      pointArray.append((xCord - edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
      pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord + edge_length * math.sin(math.pi / 3)));
      pointArray.append((xCord + edge_length, yCord));
      pointArray.append((xCord + edge_length * math.cos(math.pi / 3), yCord - edge_length * math.sin(math.pi / 3)));
   elif (gonNum == 4):
      pointArray.append((xCord, yCord));
      pointArray.append((xCord + edge_length, yCord));
      pointArray.append((xCord, yCord + edge_length));
      pointArray.append((xCord + edge_length, yCord + edge_length));
   return pointArray;

def polyToGraphCenReduce(polygons, indexMap, edgeLength, percentWiggle, gonNum):
   graph = [];
   
   # ensure center is on a primary column
   maxCol = 0;
   maxRow = 0;
   for gon in polygons:
      xCord = gon[1][0][0];
      yCord = gon[1][0][1];
      ###print("cords");
      ###print(xCord);
      ###print(yCord);
      if (xCord > 1):
         if (yCord > 1):
            centerID = indexMap[(gon[2], gon[3]+1)];
            break;
   colID = math.ceil(0.5*maxCol);

#   print("centerID");
#   print(centerID);

   # just check all possiblities
   circleIDs = [];
   
   
   # generate graph independant of grid
   visitedIDs = [];
   hexOnUnitCircle = dfsOneDist(0, 0, 0, 0, edgeLength, gonNum);
   ###print("1dist");
   ###print(hexOnUnitCircle);
   circlesIDs = dfsFindCircle(0, 0, hexOnUnitCircle[0], hexOnUnitCircle[1], edgeLength, percentWiggle, circleIDs, visitedIDs, gonNum)
   ###print("circleIDs");
   ###print(circleIDs);
   circleOffsets = circleIDs;

   agumentedOffsets = [];

   # check circles offset from each polygon
   for i in range(len(polygons)):
      for j in range(len(circleOffsets)):
         destI = polygons[i][2] + circleOffsets[j][0];
         destJ = polygons[i][3] + circleOffsets[j][1];
         try:
            shapeID = indexMap[(destI, destJ)];
            #print("shapeID");
            #print(shapeID);
            if (shapeID):
               graph.append((i+1, shapeID+1));
         except KeyError as error:
            error = 0;
   ###print("graph");
   ###print(graph);
   return graph;

def polyToGraph(polygons, indexMap):
   graph = [];
   
   # DFS for hexagon 1 dist away
   
   # ensure center is on a primary column
   maxCol = 0;
   maxRow = 0;
   for gon in polygons:
      xCord = gon[1][0][0];
      yCord = gon[1][0][1];
      ###print("cords");
      ###print(xCord);
      ###print(yCord);
      if (xCord > 1):
         if (yCord > 1):
            centerID = indexMap[(gon[2], gon[3]+1)];
            break;
   colID = math.ceil(0.5*maxCol);
   #if ((colID % 2) == 1):
   #   colID += 1;
   #centerID = colID*maxRow + math.ceil(0.5*maxRow);# + 1;
   ###print("centerID");
   ###print(centerID);

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
   ###print("circleIDs");
   ###print(circleIDs);
   circleOffsets = [];
   for i in range(len(circleIDs)):
      circleOffsets.append((-polygons[centerID][2] + polygons[circleIDs[i]][2], -polygons[centerID][3] + polygons[circleIDs[i]][3]));
   ###print("circleOffsets");
   ###print(circleOffsets);

   agumentedOffsets = [];
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
            ###print("shapeID");
            ###print(shapeID);
            if (shapeID):
               graph.append((i+1, shapeID+1));
         except KeyError as error:
            error = 0;
   i = (row+1);
   ###print(polygons[i][2]);
   for j in range(len(circleOffsets)):
      destI = circleOffsets[j][0];
      destJ = circleOffsets[j][1];
      if ((polygons[i][2] % 2) == 1) and ((circleOffsets[j][1] % 2) == 1):
         #if (circleOffsets[j][1] > 0):
         #   destI += 1;
         #else:
         destI -= 1;
      agumentedOffsets.append((destI, destJ));
   ###print("agumentedOffsets");
   ###print(agumentedOffsets);
   ###print("graph");
   ###print(graph);

   return graph;

# graph of edges
# k colors
def printCNF(graph, k, fileName):
   file = open(fileName,"w+")
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
   file.write("p cnf %d %d\n" % (n*k, n + m*k + 3)); # constrain two colors, +3 triangle
   ###print("n");
   ###print(n);

   # triangle finding
   triEdgeIndex = 0;
   triNodeIndex = 0;
   triFound = 0;
   for i in range(m):
      foundConnections = np.zeros((n, 2), dtype=int);
      firstNode = graph[i][0];
      secondNode = graph[i][1];
      firstFound = 0;
      secondFound = 0;
      for j in range(m):
         if (j != firstNode and j != secondNode):
            if (graph[j][0] == firstNode):
               foundConnections[graph[j][1]-1, 0] = 1;
            if (graph[j][0] == secondNode):
               foundConnections[graph[j][1]-1, 1] = 1;
            if (graph[j][1] == firstNode):
               foundConnections[graph[j][0]-1, 0] = 1;
            if (graph[j][1] == secondNode):
               foundConnections[graph[j][0]-1, 1] = 1;
      for j in range(n):
         if ((foundConnections[j, 0] == 1) and (foundConnections[j, 1] == 1)):
            #print(foundConnections[j, 0]);
            #print(foundConnections[j, 1]);
            #np.set_printoptions(threshold = np.inf)
            #print(foundConnections);
            triFound = 1;
            triNodeIndex = j+1;
            triEdgeIndex = i;
            break;
      if (triFound == 1):
         break;
   # constrain triangle
   file.write("%d 0\n" % ((graph[triEdgeIndex][0] -1)*k + 1));
   file.write("%d 0\n" % ((graph[triEdgeIndex][1] -1)*k + 2));
   file.write("%d 0\n" % ((triNodeIndex -1)*k + 3));
   ###print("triangle");
   ###print(graph[triEdgeIndex]);
   ###print(triNodeIndex);

   for i in range(n):
      mustHaveColorString = "";
      for j in range(1, k+1):
         mustHaveColorString += ("%d " % (i*k + j));
      mustHaveColorString += "0\n";
      file.write(mustHaveColorString);
   for i in range(m):
      #if (i == 0):
      #   constrainColorStr = ("%d ");
      #   file.write("%d 0\n" % ((graph[i][0] -1)*k + 1));
      #   file.write("%d 0\n" % ((graph[i][1] -1)*k + 2));
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
      fileInString = file.read();
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

def displayPlaneDisc(vertList, k, assignment, radius, gonNum, edgeLength, percentWiggle):
   basePixels = 600;
   win = GraphWin("test", basePixels, basePixels, autoflush=False);
   n = len(vertList);
   scaling = basePixels/radius / 2;
   for i in range(n):
      # find color #
      colorNum = 0;
      counter = 0;
      for j in range(i*k, (i+1)*k):
         counter += 1;
         if (assignment[j] > 0):
            colorNum = counter;
      if (gonNum == 4):
         # make rectangle with opposite corners
         print("points");
         pt1 = Point(vertList[i][1][0][0] * scaling, vertList[i][1][0][1] * scaling);
         pt2 = Point(vertList[i][1][2][0] * scaling, vertList[i][1][2][1] * scaling);
         rect = Rectangle(pt1, pt2);
      elif (gonNum == 6):
         scaledPoints = [];
         xCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
         xCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
         yCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
         yCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
         shrunkPoints = np.array(shrinkShape(xCen, yCen, edgeLength*percentWiggle, gonNum));
         for j in range(len(shrunkPoints)):
            scaledPoints.append(Point(shrunkPoints[j][0] * scaling + basePixels/2, shrunkPoints[j][1] * scaling + basePixels/2));
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
   line.setOutline('black');
   line.draw(win);
   win.flush();


def displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum, edgeLength, percentWiggle):
   basePixels = 1050;
   colorPixels = 1000;
   vertColorPixels = colorPixels * (gridHeight/gridWidth);
   gridExPixels = basePixels - colorPixels;
   win = GraphWin("test", basePixels, colorPixels * (gridHeight/gridWidth) + gridExPixels, autoflush=False);
   n = len(vertList);
   scaling = colorPixels/gridWidth;
   for i in range(n):
      # find color #
      colorNum = 0;
      counter = 0;
      for j in range(i*k, (i+1)*k):
         counter += 1;
         #print("assignemnt[j]");
         #print(assignment[j]);
         if (assignment[j] > 0):
            colorNum = counter;
            break;
      if (gonNum == 4):
         # make rectangle with opposite corners
         #print("points");
   #      print(vertList[i][1][0]);
   #      print(vertList[i][1][2]);
   #      print(tuple(vertList[i][1][2]));
   #      #print(Point(tuple(vertList[i][1][2])));
   #      print(Point(vertList[i][1][0][0], vertList[i][1][2][1]));
         xCen = vertList[i][2] * edgeLength;
         yCen = vertList[i][3] * edgeLength;
         scalingAmount = (1 - percentWiggle) * edgeLength;
         pt1 = Point((xCen + scalingAmount) * scaling + gridExPixels, (yCen + scalingAmount) * scaling);
         pt2 = Point((xCen + edgeLength - scalingAmount) * scaling + gridExPixels, (yCen + edgeLength - scalingAmount) * scaling);
         #pt1 = Point(vertList[i][1][0][0] * scaling, vertList[i][1][0][1] * scaling);
         #pt2 = Point(vertList[i][1][2][0] * scaling, vertList[i][1][2][1] * scaling);
         #print(pt1);
         #print(pt2);
         #print(colorNum);
         rect = Rectangle(pt1, pt2);
      elif (gonNum == 6):
         scaledPoints = [];
         xCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.cos(11*math.pi / 6);
         xCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.cos(1*math.pi / 6);
         yCen = vertList[i][2] * edgeLength * 2*math.sqrt(0.75) * math.sin(11*math.pi / 6);
         yCen += vertList[i][3] * edgeLength * 2*math.sqrt(0.75) * math.sin(1*math.pi / 6);
         shrunkPoints = np.array(shrinkShape(xCen, yCen, edgeLength*percentWiggle, gonNum));
         for j in range(len(shrunkPoints)):
            scaledPoints.append(Point(shrunkPoints[j][0] * scaling + gridExPixels, vertColorPixels + -1 * shrunkPoints[j][1] * scaling));
            #scaledPoints.append(Point(shrunkPoints[j][0] * scaling + gridExPixels, shrunkPoints[j][1] * scaling));
         #print("scaledPoints");
         #print(scaledPoints);
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
      
   # draw grid lines
   line = Line(Point(0.0 * scaling + gridExPixels, gridHeight * scaling), Point(gridWidth * scaling + gridExPixels, gridHeight * scaling));
   line.setOutline('black');
   line.draw(win);
   for i in range(int(gridWidth+1)):
      line = Line(Point(i * scaling + gridExPixels, (gridHeight - 0.2) * scaling), Point(i * scaling + gridExPixels, (gridHeight + 0.2) * scaling));
      line.setOutline('black');
      line.draw(win);
      label = Text(Point(i * scaling + gridExPixels - 10, (gridHeight + 0.2) * scaling), i)
      label.draw(win)
      if (i != gridHeight):
         for j in range(1,10):
            lineLength = 0.1;
            if (j == 5):
               lineLength = 0.1;
            else:
               lineLength = 0.05;
            line = Line(Point((i + j*0.1) * scaling + gridExPixels, (gridHeight - lineLength) * scaling), Point((i + j*0.1) * scaling + gridExPixels, (gridHeight + lineLength) * scaling));
            line.setOutline('black');
            line.draw(win);
   
   line = Line(Point(0.0 * scaling + gridExPixels, 0 * scaling), Point(0.0 * scaling + gridExPixels, gridHeight * scaling));
   line.setOutline('black');
   line.draw(win);
   for i in range(int(gridHeight+1)):
      line = Line(Point(-0.2 * scaling + gridExPixels, (-i + gridHeight) * scaling), Point(0.2 * scaling + gridExPixels, (-i + gridHeight) * scaling));
      line.setOutline('black');
      line.draw(win);
      if (i != 0):
         label = Text(Point(-0.2 * scaling + gridExPixels, (-i + gridHeight) * scaling + 10), i); # -i + int(gridHeight)
         label.draw(win)
      if (i != gridHeight):
         for j in range(1,10):
            lineLength = 0.1;
            if (j == 5):
               lineLength = 0.1;
            else:
               lineLength = 0.05;
            line = Line(Point(-lineLength * scaling + gridExPixels, ((-i + gridHeight) - j*0.1) * scaling), Point(lineLength * scaling + gridExPixels, ((-i + gridHeight) - j*0.1) * scaling));
            line.setOutline('black');
            line.draw(win);
   win.flush();

def fixColors(assignment, polygons, indexMap, k, gonNum):
   cadi = Cadical()
   cnfFile = CNF(from_file='tile.cnf');
   #cadi.add_clause("tile.cnf")
   cadi.append_formula(cnfFile.clauses, no_return=False)
   #print(assignment);
   #assignment2 = [var for var in assignment if var >= 0];
   #assignment = assignment2;
   #assignment.remove(0);
   assignment.pop();
   for i in range(10):
      oldAssignment = copy.deepcopy(assignment);
      print(assignment);
      solution = cadi.solve(assumptions=assignment);
      print(solution);
      trueSolution = solution; #idk python stuff
      #for var in assignment:
      #   if (var < 0):
      #      print(var);
      #      print(assignment.remove(var));
      print("assignmentpre");
      #print(cadi.get_model())
      for gon in polygons:
         numNeighbors = 0;
         neighborColors = [0] * k;
         try:
            if (indexMap[gon[2] + 1, gon[3] + 0]):
               id = indexMap[gon[2] + 1, gon[3] + 0];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         try:
            if (indexMap[gon[2] - 1, gon[3] + 0]):
               id = indexMap[gon[2] - 1, gon[3] + 0];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         try:
            if (indexMap[gon[2] + 0, gon[3] + 1]):
               id = indexMap[gon[2] + 0, gon[3] + 1];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         try:
            if (indexMap[gon[2] + 0, gon[3] - 1]):
               id = indexMap[gon[2] + 0, gon[3] - 1];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         try:
            if (indexMap[gon[2] + 1, gon[3] - 1]):
               id = indexMap[gon[2] + 1, gon[3] - 1];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         try:
            if (indexMap[gon[2] - 1, gon[3] + 1]):
               id = indexMap[gon[2] - 1, gon[3] + 1];
               numNeighbors += 1;
               for i in range(0,k):
                  if (assignment[i + polygons[id][0]*k] > 0):
                     neighborColors[i] += 1;
                     break;
         except KeyError as error:
            error = 0;
         if (gonNum == 4):
            try:
               if (indexMap[gon[2] + 1, gon[3] + 1]):
                  id = indexMap[gon[2] + 1, gon[3] + 1];
                  numNeighbors += 1;
                  for i in range(0,k):
                     if (assignment[i + polygons[id][0]*k] > 0):
                        neighborColors[i] += 1;
                        break;
            except KeyError as error:
               error = 0;
            try:
               if (indexMap[gon[2] - 1, gon[3] - 1]):
                  id = indexMap[gon[2] - 1, gon[3] - 1];
                  numNeighbors += 1;
                  for i in range(0,k):
                     if (assignment[i + polygons[id][0]*k] > 0):
                        neighborColors[i] += 1;
                        break;
            except KeyError as error:
               error = 0;

         newAssignment = -1;
         for i in range(0,k):
            if (neighborColors[i] > numNeighbors/2):
               newAssignment = i;
               break;
         currentAssignment = -1;
         for i in range(0,k):
            #print("assignment search");
            #print(assignment[gon[0]*k+i]);
            if (assignment[gon[0]*k+i] > 0):
               currentAssignment = i;
               break;
         print("gon[0]");
         print(gon[0]);
         print(currentAssignment);
         print(newAssignment);
         print(neighborColors);
         print(numNeighbors/2);
         if ((newAssignment >= 0) and (currentAssignment != newAssignment)):
            print("newAssign");
            print(currentAssignment);
            print(newAssignment);
            print(gon[0]);
            altAssignment = copy.deepcopy(assignment);
            for i in range(0,k):
               if (i == newAssignment):
                  if (assignment[gon[0]*k + i] < 0):
                     print("assignment fliped");
                     #print(altAssignment[gon[0]*k + i]);
                     #altAssignment[gon[0]*k + i] = -altAssignment[gon[0]*k + i];
                     #print(altAssignment[gon[0]*k + i]);
                     print(assignment[gon[0]*k + i]);
                     assignment[gon[0]*k + i] = gon[0]*k + i + 1;
                     print(assignment[gon[0]*k + i]);
                  print("assignment at new");
                  print(assignment[gon[0]*k + i]);
               elif (assignment[gon[0]*k + i] > 0):
                  print("positive fliped");
                  #print(altAssignment[gon[0]*k + i]);
                  #altAssignment[gon[0]*k + i] = -altAssignment[gon[0]*k + i];
                  #print(altAssignment[gon[0]*k + i]);
                  print(assignment[gon[0]*k + i]);
                  assignment[gon[0]*k + i] = -(gon[0]*k + i + 1); # assignment[gon[0]*k + i]
                  print(assignment[gon[0]*k + i]);
            #if (indexMap[gon[2], gon[3]]):
            #print(cadi.solve(assumptions=assignment))
            #print(assignment);
            #print("SAT check");
            solution = cadi.solve(assumptions=assignment);
            print(solution);
            if (solution == trueSolution):
               #assignment = altAssignment[:];
               #assignment = copy.deepcopy(altAssigment);
               error = 0;
               print("changed!");
            else:
               assignment[gon[0]*k + currentAssignment] = gon[0]*k + currentAssignment+1;
               assignment[gon[0]*k + newAssignment] = -(gon[0]*k + newAssignment+1);
            solution = cadi.solve(assumptions=assignment);
            print(solution); # needs to be true
               #print(cadi.model);
      #print("oldAssignment");
      #print(oldAssignment);
      #print("altAssignment");
      #print(altAssignment);
      #print("assignment");
      #print(assignment);
      if (oldAssignment == assignment):
         print("no change");
         break;
   
   print(assignment);
   print("assignmentpost");

   return assignment;

print(sys.getrecursionlimit());
sys.setrecursionlimit(40000000);

# colors
k = 4;
# edge number, sides of the polygon
gonNum = 4;
edgeLength = 0.01;
percentWiggle = 1;
#gridSize = 1;
gridWidth = 8;
gridHeight = 0.90;
inputFileName = "tile.cnf";

# format: filename edgeLength percentWiggle gonNum gridWidth gridHeight
print(len(sys.argv));
for i in range(len(sys.argv)):
   print(sys.argv[i]);
   if (i == 1):
      k = int(sys.argv[i]);
   elif (i == 2):
      gonNum = int(sys.argv[i]);
   elif (i == 3):
      edgeLength = float(sys.argv[i]);
   elif (i == 4):
      percentWiggle = float(sys.argv[i]);
   elif (i == 5):
      gridWidth = float(sys.argv[i]);
      gridHeight = float(sys.argv[i]);
   elif (i == 6):
      gridHeight = float(sys.argv[i]);      
   elif (i == 7):
      inputFileName = sys.argv[i];
   elif (i == 8):
      outputFileName = sys.argv[i];

print("k: ", k);
print("gonNum: ", gonNum);
print("edgeLength: ", edgeLength);
print("percentWiggle: ", percentWiggle);
print("gridWidth: ", gridWidth);
print("gridHeight: ", gridHeight);
print("fileName: ", inputFileName);

(vertList, indexMap) = generate_normal_shape(gonNum, edgeLength, gridWidth, gridHeight)
#radius = 1;
#(vertList, indexMap) = generate_normal_shapeDisc(gonNum, edgeLength, radius)

###print("vertList");
###print(vertList);
#graph = polyToGraph(vertList, indexMap);


# uncomment to work again
graph = polyToGraphCenReduce(vertList, indexMap, edgeLength, percentWiggle, gonNum)
#print("graph")
#print(graph);
printCNF(graph, k, inputFileName);

name = input("Enter to proceed ")

assignment = readAssignemnt(outputFileName); #satAssignment.txt
assignment = fixColors(assignment, vertList, indexMap, k, gonNum);
#assignment = fixColors(assignment, vertList, indexMap, k);
#name = input("Enter to close ");

print("assignment");
print(assignment);
# To change to polygons showing scaling factor change 1 to percentWiggle
displayPlane(vertList, k, assignment, gridWidth, gridHeight, gonNum, edgeLength, 1);
#displayPlaneDisc(vertList, k, assignment, radius, gonNum, edgeLength, 1);

name = input("Enter to close ");

