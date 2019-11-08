#!/bin/sh

# Shell script to run n times the genetic algorithm
# Enter as first parameter the number of executions
# example: ./run.sh 30 16 for 30 executions and a population of 16 individuals

export INDIVIDUALS=$2

for i in `seq $1` ; do
	echo "Running $i execution..."
    
    python3 genetic.py --individuals ${INDIVIDUALS} --crossover-one-point --random-mutation > results/results_juice_${INDIVIDUALS}_1_random_$i.txt
	python3 genetic.py --individuals ${INDIVIDUALS} --crossover-one-point --no-random-mutation > results/results_juice_${INDIVIDUALS}_1_one_$i.txt
	python3 genetic.py --individuals ${INDIVIDUALS} --crossover-two-points --random-mutation > results/results_juice_${INDIVIDUALS}_2_random_$i.txt
	python3 genetic.py --individuals ${INDIVIDUALS} --crossover-two-points --no-random-mutation  > results/results_juice_${INDIVIDUALS}_2_one_$i.txt

done
echo "Finised!"