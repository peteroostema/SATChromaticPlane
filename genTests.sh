#!/bin/bash

FILE="tile.cnf"
FILE2="tile2.cnf"
#FILE3="test1.cnf"
#FILE4="test2.cnf"
#FILE5="test3.cnf"
#FILE6="test4.cnf"
#FILE7="test5.cnf"
#FILE8="test6.cnf"
#FILE10="test7.cnf"
#FILE11="test8.cnf"
#FILE12="test9.cnf"
#FILE13="test10.cnf"
line=$(head -n 1 $FILE)
tail -n +2 "$FILE" > "$FILE2"
#gshuf $FILE2 > $FILE3
#gshuf $FILE2 > $FILE4
#gshuf $FILE2 > $FILE5
#gshuf $FILE2 > $FILE6
#gshuf $FILE2 > $FILE7
#gshuf $FILE2 > $FILE8
#gshuf $FILE2 > $FILE10
#gshuf $FILE2 > $FILE11
#gshuf $FILE2 > $FILE12
#gshuf $FILE2 > $FILE13
#echo "$line\n$(cat $FILE3)" > $FILE3
#echo "$line\n$(cat $FILE4)" > $FILE4
#echo "$line\n$(cat $FILE5)" > $FILE5
#echo "$line\n$(cat $FILE6)" > $FILE6
#echo "$line\n$(cat $FILE7)" > $FILE7
#echo "$line\n$(cat $FILE8)" > $FILE8
#echo "$line\n$(cat $FILE10)" > $FILE10
#echo "$line\n$(cat $FILE11)" > $FILE11
#echo "$line\n$(cat $FILE12)" > $FILE12
#echo "$line\n$(cat $FILE13)" > $FILE13

echo $line
# run processes and store pids in array
for i in $(seq 1 $1); do
   echo $i
   inputFile="test${i}.cnf"
   echo $inputFile
   shuf $FILE2 > $inputFile
   printf "$line\n$(cat $inputFile)" > $inputFile
done
