from ortools.algorithms import pywrapknapsack_solver
from test_loader import test_loader
import os
from os.path import join
from random import sample
import time

# ./tests/kplib
kplib_path = join( "tests", "kplib")

def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    # values = [
    #     360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
    #     78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
    #     87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
    #     312
    # ]
    # weights = [[
    #     7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    #     42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    #     3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
    # ]]
    # capacities = [850]

    # _ , capacities, values, weights = load_test("./tests/kplib/00Uncorrelated/n00050/R01000/s001.kp")
    # _ , capacities, values, weights = load_test("./tests/kplib/00Uncorrelated/n10000/R10000/s004.kp")


    # solver.Init(values, weights, capacities)
    # computed_value = solver.Solve()

    # packed_items = []
    # packed_weights = []
    # total_weight = 0
    # print('Total value =', computed_value)
    # for i in range(len(values)):
    #     if solver.BestSolutionContains(i):
    #         packed_items.append(i)
    #         packed_weights.append(weights[0][i])
    #         total_weight += weights[0][i]
    # print('Total weight:', total_weight)
    # print('Packed items:', packed_items)
    # print('Packed_weights:', packed_weights)
    # test(kplib_path)

    test = test_loader(kplib_path)
    solver.set_time_limit(30)
    
    for t in test.load_types():
        test.set_types(t)

        for s in test.load_sizes():
            test.set_size(s)

            for r in test.load_ranges():
                test.set_range(r)

                for i in sample( test.load_tests(),2):
                    test.set_test(i)

                    _ , capacities, values, weights = test.parse_test()

                    print(test.get_type()," ", test.get_size()," ", test.get_range()," ", test.get_test_name())
                    
                    solver.Init(values, weights, capacities)

                    start_time = time.time()
                    computed_value = solver.Solve()
                    duration = time.time() - start_time

                    packed_items = [item for item in range(0, len(weights[0])) if solver.BestSolutionContains(item_id=item)]
                    
                    total_weight = sum([weights[0][item] for item in packed_items])

                    print("\tvalue: ", computed_value, "\n\tweight: ", total_weight,"\n\tduration: ",round(duration, 4))



if __name__ == '__main__':
    main()