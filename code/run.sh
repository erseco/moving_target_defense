#!/bin/sh

# Shell script to run n times the genetic algorithm
# Enter as first parameter the number of executions
# example: ./run.sh 30 for 30 executions

INDIVIDUALS=16

for i in `seq $1` ; do
	echo "Running $i execution..."
    
    python3 genetic.py --individuals $INDIVIDUALS --crossover-one-point --random-mutation > results/results_$INDIVIDUALS_1_random_$i.txt
	python3 genetic.py --individuals $INDIVIDUALS --crossover-one-point --no-random-mutation > results/results_$INDIVIDUALS_1_one_$i.txt
	python3 genetic.py --individuals $INDIVIDUALS --crossover-two-points --random-mutation > results/results_$INDIVIDUALS_2_random_$i.txt
	python3 genetic.py --individuals $INDIVIDUALS --crossover-two-points --no-random-mutation  > results/results_$INDIVIDUALS_2_one_$i.txt

done
echo "Finised!"