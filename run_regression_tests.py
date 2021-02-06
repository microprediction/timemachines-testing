from timemachines.skaters.optimization import optimal_r
from timemachines.skaters.conventions import from_space
from timemachines.data.synthetic import brownian_with_exogenous
from timemachines import OPTIMIZERS
from timemachines.skaters.allskaters import SKATERS_R2, SKATERS_R1, SKATERS_R3
from timemachines.skaters.evaluation import evaluate_mean_squared_error
import time
import random
import os
import json
import traceback

DATA = './regression_test_results'
NAME = 'brownian'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def random_json_file_name():
    return ''.join([random.choice('abcdef1234567890') for _ in range(12)]) + '.json'


def random_dim_and_skaters():
    n_dim = random.choice([1, 2, 3])
    if n_dim == 1:
        skaters = SKATERS_R1
    elif n_dim == 2:
        skaters = SKATERS_R2
    elif n_dim == 3:
        skaters = SKATERS_R3
    return n_dim, skaters


def optimize_random_skater(k=1, n=425, n_trials=15, n_burn=400):
    start_time = time.time()
    o = random.choice(OPTIMIZERS)
    n_dim, candidate_skaters = random_dim_and_skaters()
    if candidate_skaters:
        f = random.choice(candidate_skaters)

        ensure_dir(DATA)
        STREAM = DATA+os.path.sep+NAME  # Later we may include different streams
        ensure_dir(STREAM)
        ensure_dir(STREAM + os.path.sep + f.__name__)
        combo_dir = STREAM + os.path.sep + f.__name__ + os.path.sep + o.__name__
        ensure_dir(combo_dir)
        success_dir = combo_dir + os.path.sep + 'successes'
        failures_dir = combo_dir + os.path.sep + 'failures'
        timeouts_dir = combo_dir + os.path.sep + 'timeouts'
        ensure_dir(success_dir)
        ensure_dir(failures_dir)
        ensure_dir(timeouts_dir)

        fn = random_json_file_name()
        timeout_file = timeouts_dir + os.path.sep + fn
        failure_file = failures_dir + os.path.sep + fn

        with open(timeout_file, 'wt') as fpt:
            json.dump({"epoch_time": time.time()}, fpt)

        # Try to optimize
        try:
            best_r, best_val, info = optimal_r(f=f, y=brownian_with_exogenous(n=n), k=k,a=None,t=None, e=None,
                                   n_trials=n_trials, n_dim=n_dim, n_burn=n_burn,
                                   optimizer=o, evaluator=evaluate_mean_squared_error,
                                         test_objective_first=True)
        except Exception as e:
            traceback.print_exc()
            tb = traceback.format_exc()
            print(str(e))
            os.remove(timeout_file)
            with open(failure_file, 'wt') as fpf:
                json.dump({'error': str(e),'traceback':tb}, fpf)
            return None, None

        os.remove(timeout_file)
        best_r = from_space(best_r)
        success_file = success_dir + os.path.sep + 'best_val=' + str(round(best_val, 6)) + '_r=' + str(round(best_r, 6)) + '.json'
        data = {'best_r': best_r, 'best_x': tuple(list(best_r)), 'best_val': best_val, 'elapsed': time.time() - start_time, 'n': n,
                'n_trials': n_trials}
        from pprint import pprint
        print(success_file)
        pprint(data)
        with open(success_file, 'wt') as fps:
            json.dump(data, fps)
        return best_val, best_r


if __name__ == '__main__':
    optimize_random_skater()
    pass
