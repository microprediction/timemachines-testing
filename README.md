# timemachines-testing ![tests](https://github.com/microprediction/timemachines/workflows/tests/badge.svg) ![regression-tests](https://github.com/microprediction/timemachines-testing/workflows/regression-tests/badge.svg) ![optimizer-elo-ratings](https://github.com/microprediction/timemachines-testing/workflows/optimizer-elo-ratings/badge.svg) ![skater-elo-ratings](https://github.com/microprediction/timemachines-testing/workflows/skater-elo-ratings/badge.svg)

Standalone time intensive testing of the timemachines package that generates Elo ratings as a byproduct. 

### Optimizer Elo ratings and leaderboards

See [optimizer_elo_ratings/leaderboards](https://github.com/microprediction/timemachines-testing/tree/main/optimizer_elo_ratings/leaderboards/overall) for current rankings and Elo ratings of global optimization strategies. These are computed by random match-ups where an [objective](https://github.com/microprediction/timemachines/blob/main/timemachines/optimizers/objectives.py) function is chosen at random and the dimensionality of the search and number of allowed iterations is also randomly selected. The precise methodology is revealed in [optimizers/eloratings.py](https://github.com/microprediction/timemachines/blob/main/timemachines/optimizers/eloratings.py). 


### Model Elo ratings and leaderboards

Arranged by how many steps ahead we predict. See [skater_elo_ratings/leaderboards](https://github.com/microprediction/timemachines-testing/tree/main/skater_elo_ratings/leaderboards) sub-directories. For example some good ways to predict univariate time series 8 steps in advance might be suggested by the rankings at [/leaderboards/univariate_008](https://github.com/microprediction/timemachines-testing/tree/main/skater_elo_ratings/leaderboards/univariate_008) but of course their are caveats. 

