from timemachines.optimizers.eloratings import optimizer_elo_update
from pprint import pprint
import json
import os
import random


N_DIM_CHOICES = [2, 3, 5, 8, 13, 21]
N_TRIALS_CHOICES = [ 30, 50, 80, 130, 210, 340]


def update_optimizer_elo_ratings_once():
    # For now, just the overall performance is updated

    ELO_PATH = os.path.dirname(os.path.realpath(__file__))+os.path.sep+'optimizer_elo_ratings'

    try:
        os.makedirs(ELO_PATH)
    except FileExistsError:
        pass
    ELO_FILE = ELO_PATH + os.path.sep + 'overall.json'

    # Try to resume
    try:
        with open(ELO_FILE,'rt') as fp:
            elo = json.load(fp)
    except:
        elo = {}

    # Update elo skater_elo_ratings
    elo, match_params = optimizer_elo_update(elo=elo,n_dim_choices = N_DIM_CHOICES, n_trials_choices=N_TRIALS_CHOICES)
    pprint(sorted(list(zip(elo['rating'],elo['name']))))

    # Try to save
    with open(ELO_FILE, 'wt') as fp:
        json.dump(elo,fp)

    # Write individual files so that the directory serves as a leaderboard
    LEADERBOARD_DIR = ELO_PATH + os.path.sep + 'leaderboards'+os.path.sep+'overall'
    try:
        os.makedirs(LEADERBOARD_DIR)
    except FileExistsError:
        pass

    # Clean out the old
    import glob
    fileList = glob.glob(LEADERBOARD_DIR+ os.path.sep + '*.json')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

    pos = 1
    for rating, name, count,active, traceback in sorted(list(zip(elo['rating'],elo['name'],elo['count'],elo['active'],elo['traceback'])),reverse=True):
        package = name.split('_')[0]
        strategy = name.replace('_cube','')
        SCORE_FILE = LEADERBOARD_DIR + os.path.sep +str(pos).zfill(3)+'-'+str(int(rating)).zfill(4)+'-'+strategy+'-'+str(count)
        pos+=1
        if not active:
            SCORE_FILE += '_inactive'
        if len(traceback) > 20 and 'naughty' in traceback:
            SCORE_FILE += '_naughty'
        if len(traceback)>50:
            SCORE_FILE += '_FAILING'
        SCORE_FILE+='.json'
        with open(SCORE_FILE, 'wt') as fp:
            json.dump(obj={'name':name,'package':package,'strategy':strategy,
                           'traceback':traceback}, fp=fp)


if __name__=='__main__':
    update_optimizer_elo_ratings_once()


