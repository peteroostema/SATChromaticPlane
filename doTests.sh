#!/bin/bash

#trap 'kill $(jobs -p)' EXIT

#cadical test1.cnf > cadOut1.txt && exit 0
#cadical test2.cnf > cadOut2.txt && exit 0
#cadical test3.cnf > cadOut3.txt && exit 0
#cadical test4.cnf > cadOut4.txt && exit 0
#cadical test5.cnf > cadOut5.txt && exit 0
#cadical test6.cnf > cadOut6.txt && exit 0
#cadical test7.cnf > cadOut7.txt && exit 0
#cadical test8.cnf > cadOut8.txt && exit 0
#cadical test9.cnf > cadOut9.txt && exit 0
#cadical test10.cnf > cadOut10.txt && exit 0

## run processes and store pids in array
#for i in $(seq 1 $1); do
#   inputFile="test${i}.cnf"
#   outputFile="cadOut${i}.txt"
#   cadical $inputFile > $outputFile &
#   #./procs[${i}] &
#   pids[${i}]=$!
#done

## wait for all pids
#for pid in ${pids[*]}; do
#   wait $pid
#   for i in ${pids[*]}; do
#      echo $i
#      kill $i
#      #echo ${pids[${i}]}
#      #kill ${pids[${i}]}
#   done
#done

## wait for any pids
#wait -n
#for i in ${pids[*]}; do
#   echo $i
#   kill $i
#   #echo ${pids[${i}]}
#   #kill ${pids[${i}]}
#done

# bash < v4.3
set -o monitor
killAll(){
for i in ${pids[*]}; do
   echo $i
   kill $i
   #echo ${pids[${i}]}
   #kill ${pids[${i}]}
done
}

sequence=$(seq 1 $1)

trap killAll SIGCHLD

# run processes and store pids in array
for i in $sequence; do
   inputFile="test${i}.cnf"
   outputFile="cadOut${i}.txt"
   cadical $inputFile > $outputFile &
   #./procs[${i}] &
   pids[${i}]=$!
done

wait
