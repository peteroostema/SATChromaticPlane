#!/bin/bash

trap 'kill $(jobs -p)' EXIT

./cadical /home/peter/Documents/sat/project/test1.cnf > /home/peter/Documents/sat/project/cadOut1.txt && exit 0
./cadical /home/peter/Documents/sat/project/test2.cnf > /home/peter/Documents/sat/project/cadOut2.txt && exit 0
./cadical /home/peter/Documents/sat/project/test3.cnf > /home/peter/Documents/sat/project/cadOut3.txt && exit 0
./cadical /home/peter/Documents/sat/project/test4.cnf > /home/peter/Documents/sat/project/cadOut4.txt && exit 0
./cadical /home/peter/Documents/sat/project/test5.cnf > /home/peter/Documents/sat/project/cadOut5.txt && exit 0
./cadical /home/peter/Documents/sat/project/test6.cnf > /home/peter/Documents/sat/project/cadOut6.txt && exit 0
./cadical /home/peter/Documents/sat/project/test7.cnf > /home/peter/Documents/sat/project/cadOut7.txt && exit 0
./cadical /home/peter/Documents/sat/project/test8.cnf > /home/peter/Documents/sat/project/cadOut8.txt && exit 0
./cadical /home/peter/Documents/sat/project/test9.cnf > /home/peter/Documents/sat/project/cadOut9.txt && exit 0
./cadical /home/peter/Documents/sat/project/test10.cnf > /home/peter/Documents/sat/project/cadOut10.txt && exit 0

