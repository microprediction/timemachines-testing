from timemachines.optimization import optimize
from timemachines.synthetic import brownian_with_exogenous
from timemachines.optimizers.compendium import OPTIMIZERS
from timemachines.skaters.compendium import SKATERS
import time
import random
import os
import json

OFFLINE='offlinetesting'

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def random_json_file_name():
    return ''.join([ random.choice(['a','b','c','d'] for _ in range(12)] )+'.json'


def optimize_random_skater(n=150,n_trials=15):
    start_time = time.time()
    optimizer = random.choice(OPTIMIZERS)
    skater = random.choice(SKATERS)
    experiment_name = optimizer.__name__+'__'+skater.__name__
    ensure_dir(OFFLINE)
    ensure_dir(OFFLINE+'/'+skater.__name__)
    dir = OFFLINE+'/'+skater.__name__+'/'+optimizer.__name__
    success_dir = dir+'/successes'
    failures_dir = dir+'/failures'
    timeouts_dir = dir+'/timeouts'
    ensure_dir(dir)
    ensure_dir(success_dir)
    ensure_dir(failures_dir)
    
    fn = random_json_file_name()
    timeout_file = timeouts_dir+fn
    failure_file = failures_dir+fn
    
    with open(timeout_file) as fp
        json.dump({"epoch_time":time.time()},fp)
        
    # Try to optimize
    try:
      r_star, evaluation = optimize(f=f, ys=brownian_with_exogenous(n=n),
                      n_trials=n_trials, optimizer=optimizer)
      success = True
    except:
      suceess = False
      
    if success:
      os.remove(timeout_file)
      success_file = 'eval_'+str( round(evaluation,6)) + '_r='+str(round(evaluation,6))+'.json'
      data = {'r':r_star,'evaluation':evaluation}
      with open(success_file) as fps:
         json.dump(data,fps)
    except Exception as e: 
      with open(failure_file) as fpf:
         json.dump({'error':str(e)})
       

if __name__=='__main__':
    optimize_random_skater()
