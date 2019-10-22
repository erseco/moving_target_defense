#!/bin/sh

# Shell script to run n times the genetic algorithm
# Enter as first parameter the number of executions
# example: ./run.sh 30 for 30 executions



python3 genetic.py --individuals 16 --crossover-one-point --random-mutation 		> results/results_16_1_random_$1.txt
python3 genetic.py --individuals 16 --crossover-one-point --no-random-mutation 	> results/results_16_1_one_$1.txt
python3 genetic.py --individuals 16 --crossover-two-points --random-mutation 	> results/results_16_2_random_$1.txt
python3 genetic.py --individuals 16 --crossover-two-points --no-random-mutation  > results/results_16_2_one_$1.txt

# python3 genetic.py --individuals 32 --crossover-one-point --random-mutation		> results/results_32_1_random_$1.txt
# python3 genetic.py --individuals 32 --crossover-one-point --no-random-mutation		> results/results_32_1_one_$1.txt
# python3 genetic.py --individuals 32 --crossover-two-points --random-mutation		> results/results_32_2_random_$1.txt
# python3 genetic.py --individuals 32 --crossover-two-points --no-random-mutation		> results/results_32_2_one_$1.txt

# python3 genetic.py --individuals 64 --crossover-one-point --random-mutation	> results/results_64_1_random_$1.txt
# python3 genetic.py --individuals 64 --crossover-one-point --no-random-mutation	> results/results_64_1_one_$1.txt
# python3 genetic.py --individuals 64 --crossover-two-points --random-mutation	> results/results_64_2_random_$1.txt
# python3 genetic.py --individuals 64 --crossover-two-points --no-random-mutation	> results/results_64_2_one_$1.txt



for i in `seq $1` ; do
	echo "Running $i execution..."
    
    python3 genetic.py --individuals 16 --crossover-one-point --random-mutation 		> results/results_16_1_random_$1.txt
	python3 genetic.py --individuals 16 --crossover-one-point --no-random-mutation 	> results/results_16_1_one_$1.txt
	python3 genetic.py --individuals 16 --crossover-two-points --random-mutation 	> results/results_16_2_random_$1.txt
	python3 genetic.py --individuals 16 --crossover-two-points --no-random-mutation  > results/results_16_2_one_$1.txt


done
echo "Finised!"