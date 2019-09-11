#!/bin/sh

# Shell script to run n times the genetic algorithm
# Enter as first parameter the number of executions
# example: ./run.sh 30 for 30 executions


for i in `seq $1` ; do
	echo "Running $i execution..."
    python3 genetic.py > results/result_$i.txt
done
echo "Finised!"