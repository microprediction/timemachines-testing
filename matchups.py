# Matches and Elo ratings for optimizers against synthetic objective functions
from timemachines.optimization import optimize
from timemachines import OPTIMIZERS
from timemachines.optimizers.odious import optimizer_name
from timemachines.evaluation import EVALUATORS
from timemachines import SKATERS
from microprediction import MicroWriter
import time
import random
import json
import os
import numpy as np
from ratings.elo import elo_expected
from pprint import pprint

try:
    from config_private import DOOMSDAY_STOAT as write_key
except:
    write_key = os.environ.get('WRITE_KEY')

mw = MicroWriter(write_key=write_key)
print(mw.animal)


MATCHUPS_DIR = './matchups'



def random_json_file_name():
    return ''.join([random.choice('abcdef1234567890') for _ in range(12)]) + '.json'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir(MATCHUPS_DIR)


def random_optimizer_matchup():
    """ Field test two optimizers and assign a win/loss/draw """

    white,black = np.random.choice(OPTIMIZERS,2,replace=False)
    f = random.choice(SKATERS)
    print('Skater is '+f.__name__)
    evaluator = random.choice(EVALUATORS)
    names = mw.get_stream_names()
    n_lagged = 0
    n = random.choice([150])
    while n_lagged<n:
        name = random.choice(names)
        ys = list(reversed(mw.get_lagged_values(name=name, count=2000)))
        n_lagged = len(ys)

    n_trials = random.choice([5,10,20])
    n_dim = random.choice([2,3])
    n_burn = n-50

    # White plays
    print('White is '+white.__name__)
    start_time = time.time()
    best_val_white, best_x_white, count_white = optimize(f=f, ys=ys, n_trials=n_trials, n_dim=n_dim, n_burn=n_burn, optimizer=white, evaluator=evaluator, with_count=True)
    white_elapsed = time.time()-start_time

    # Black plays
    print('Black is ' + black.__name__)
    start_time = time.time()
    best_val_black, best_x_black, count_black = optimize(f=f, ys=ys, n_trials=n_trials, n_dim=n_dim, n_burn=n_burn, optimizer=black, evaluator=evaluator, with_count=True)
    black_elapsed = time.time()-start_time

    valid_white, valid_black = count_white < 2 * n_trials, count_black <= n_trials

    tol = 1e-3 * (abs(best_val_white) + abs(best_val_black))
    if valid_white and valid_black:
        if best_val_white < best_val_black - tol:
            points = 1.0
        elif best_val_black < best_val_white - tol:
            points = 0.0
        else:
            points = 0.5
    else:
        points = None

    report = {'white': optimizer_name(white),
              'black': optimizer_name(black),
              'points':points,
              'epoch_time':time.time(),
              'f': f.__name__,
              'name': name,
              'stream_url': 'https://www.microprediction.org/stream_dashboard.html?stream=' + name.replace('.json', ''),
              'white_name':'optimizer_elo_' + optimizer_name(white) + '.json',
              'black_name':'optimizer_elo_' + optimizer_name(black) + '.json',
              'white_stream_url': 'https://www.microprediction.org/stream_dashboard.html?stream=optimizer_elo_' + optimizer_name(white) + '.json',
              'black_stream_url': 'https://www.microprediction.org/stream_dashboard.html?stream=optimizer_elo_' + optimizer_name(
                  black) + '.json',
              'evaluator': evaluator.__name__,
              'n': n, 'n_trials': n_trials, 'n_dim': n_dim, 'n_burn': n_burn,
              'white_elapsed':white_elapsed,
              'black_elapsed':black_elapsed,
              'best_val_white':best_val_white,
              'best_val_black':best_val_black,
              'count_white':count_white,
              'count_black':count_black,
              'valid_white':valid_white,
              'valid_black':valid_black
              }

    return report


def random_optimizer_matchup_and_elo_update():
    report = random_optimizer_matchup()
    white_name = report['white_name']
    black_name = report['black_name']

    # Initialize Elo rating if they don't exist
    names = mw.get_stream_names()
    if len(names)>100:
        for name in [white_name,black_name]:
            if white_name not in names:
                mw.set(name=name,value=2000)
    else:
        raise Exception('Cannot get streams')

    white_elo = float(mw.get_current_value(name=white_name))
    black_elo = float(mw.get_current_value(name=black_name))
    d = black_elo-white_elo
    e = elo_expected(d=d,f=400)
    w = report['points']-e
    K = 16
    white_new_elo = white_elo + K*e
    black_new_elo = black_elo - K*e

    mw.set(name=white_name,value=white_new_elo)
    mw.set(name=black_name,value=black_new_elo)

    match_report_log = MATCHUPS_DIR + os.path.sep + random_json_file_name()
    with open(match_report_log, 'wt') as fpt:
        json.dump(report, fpt)

    return report


if __name__=='__main__':
    report=random_optimizer_matchup()
    pprint(report)




