from timemachines.optimization import optimize
from timemachines.conventions import from_space
from timemachines.synthetic import brownian_with_exogenous
from timemachines import OPTIMIZERS
from timemachines import SKATERS
from timemachines.evaluation import evaluate_mean_squared_error
import time
import random
import os
import json
import traceback

DATA = './data'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def random_json_file_name():
    return ''.join([random.choice('abcdef1234567890') for _ in range(12)]) + '.json'


def optimize_random_skater(n=150, n_trials=15, n_dim=3):
    start_time = time.time()
    o = random.choice(OPTIMIZERS)
    f = random.choice(SKATERS)
    ensure_dir(DATA)
    ensure_dir(DATA + os.path.sep + f.__name__)
    combo_dir = DATA + os.path.sep + f.__name__ + os.path.sep + o.__name__
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
        best_val, best_x = optimize(f=f, ys=brownian_with_exogenous(n=n),
                               n_trials=n_trials, n_dim=n_dim, n_burn = 20,
                               optimizer=o, evaluator=evaluate_mean_squared_error)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
        os.remove(timeout_file)
        with open(failure_file, 'wt') as fpf:
            json.dump({'error': str(e)}, fpf)
        return None, None

    best_r = from_space(best_x)
    success_file = 'eval_' + str(round(best_val, 6)) + '_r=' + str(round(best_r, 6)) + '.json'
    data = {'best_r': best_r, 'best_x': tuple(list(best_x)), 'best_val': best_val, 'elapsed': time.time() - start_time, 'n': n,
            'n_trials': n_trials}
    with open(success_file, 'wt') as fps:
        json.dump(data, fps)
    return best_val, best_r


if __name__ == '__main__':
    optimize_random_skater()
    pass
