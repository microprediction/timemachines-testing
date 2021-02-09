from timemachines.optimizers.eloratings import optimizer_population_elo_update, random_optimizer_game
from timemachines.objectives.allobjectives import CLASSIC_OBJECTIVES
from timemachines.optimizers.alloptimizers import OPTIMIZERS
from pprint import pprint
import json
import os
import numpy as np

INITIAL_ELO = 1600
N_DIM_CHOICES = [2, 3, 5, 8, 13, 21, 34]
N_TRIALS_CHOICES = [ 30, 50, 80, 130, 210, 340, 550, 890]

# To include specific Elo ratings, add another category - if necessary with a singleton set of objectives
CATEGORIES = {'classic':CLASSIC_OBJECTIVES}
cand = set()
for cat, objs in CATEGORIES.items():
    cand = cand.union(objs)
CANDIDATE_OBJECTIVES = list(cand)


import random
import string


def get_random_string(n):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))


def update_optimizer_elo_ratings_once():
    # Arranges a head-to-head contest between two optimizers
    # Based on this the overall Elo rating is updated, as are sub-category elo ratings pertaining to
    # the choice of dimension, number of trials, and the set of objective functions

    game_result = random_optimizer_game(optimizers=OPTIMIZERS, objectives=CANDIDATE_OBJECTIVES, n_dim_choices=N_DIM_CHOICES, n_trials_choices=N_TRIALS_CHOICES, tol=0.001 )
    print(' Game...')
    pprint(game_result)

    # Save the game
    OPTIMIZER_ELO_PATH = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'optimizer_elo_ratings'
    GAME_LOG_PATH = OPTIMIZER_ELO_PATH+os.path.sep+'games'
    sanitized_game = dict([(k,list(v) if isinstance(v,np.ndarray) else v) for k,v in game_result.items()])
    sanitized_game['white'] = sanitized_game['white'].__name__.replace('_cube','')
    sanitized_game['black'] = sanitized_game['black'].__name__.replace('_cube','')
    game_file = GAME_LOG_PATH + os.path.sep + sanitized_game['white'] + '_versus_'+ sanitized_game['black'] + '_'+get_random_string(6)+'.json'

    try:
        js = json.dumps(sanitized_game)
        serializable = True
    except:
        serializable = False
        import warnings
        warnings.warn('Game state is no longer serializable - not saving. ')
    if serializable:
        try:
            os.makedirs(GAME_LOG_PATH)
        except FileExistsError:
            pass
        with open(game_file, 'wt') as fp:
            json.dump(sanitized_game, fp)

    relevant_categories = ['overall']+[cat for cat,cat_objs in CATEGORIES.items() if game_result['objective'] in [obj.__name__ for obj in cat_objs]]
    for category in relevant_categories:
        n_dim = game_result['n_dim']
        n_trials = game_result['n_trials']
        label = category+'_d'+str(n_dim).zfill(2)+'_n'+str(n_trials) if category is not 'overall' else 'overall'
        LEADERBOARD_PATH = OPTIMIZER_ELO_PATH+os.path.sep+'leaderboards'+os.path.sep+label
        try:
            os.makedirs(LEADERBOARD_PATH)
        except FileExistsError:
            pass
        ELO_FILE = OPTIMIZER_ELO_PATH + os.path.sep + label+'.json'

        # Try to resume
        try:
            with open(ELO_FILE,'rt') as fp:
                elo = json.load(fp)
        except:
            elo = {}

        # Update
        elo = optimizer_population_elo_update(optimizers=OPTIMIZERS, game_result=game_result, elo=elo, initial_elo=INITIAL_ELO)

        print(' Category: '+label)
        pprint(sorted(list(zip(elo['rating'],elo['name'],elo['count']))))

        # Try to save
        with open(ELO_FILE, 'wt') as fp:
            json.dump(elo,fp)

        # Write individual files so that the directory serves as a leaderboard
        try:
            os.makedirs(LEADERBOARD_PATH)
        except FileExistsError:
            pass

        # Clean out the old
        import glob
        fileList = glob.glob(LEADERBOARD_PATH+ os.path.sep + '*.json')
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)

        # Write the new files in order
        pos = 1
        for rating, name, count,active, traceback in sorted(list(zip(elo['rating'],elo['name'],elo['count'],elo['active'],elo['traceback'])),reverse=True):
            package = name.split('_')[0]
            strategy = name.replace('_cube','')
            SCORE_FILE = LEADERBOARD_PATH + os.path.sep +str(pos).zfill(3)+'-'+str(int(rating)).zfill(4)+'-'+strategy+'-'+str(count)
            pos+=1
            if not active:
                SCORE_FILE += '_inactive_'
            if len(traceback) > 20 and 'naughty' in traceback:
                SCORE_FILE += '_naughty_'
            elif len(traceback)>100:
                SCORE_FILE += '_FAILING_'
            SCORE_FILE+='.json'
            with open(SCORE_FILE, 'wt') as fp:
                json.dump(obj={'name':name,'package':package,'strategy':strategy,
                               'traceback':traceback}, fp=fp)


if __name__=='__main__':
    update_optimizer_elo_ratings_once()


