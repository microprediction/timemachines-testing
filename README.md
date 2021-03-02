# timemachines-testing ![skater-elo-ratings](https://github.com/microprediction/timemachines-testing/workflows/skater-elo-ratings/badge.svg)

Testing the [timemachines](https://github.com/microprediction/timemachines) package. This generates [Elo ratings](https://github.com/microprediction/timemachines-testing/tree/main/skater_elo_ratings/leaderboards) for popular time series packages as a byproduct. 


### Model Elo ratings and leaderboards

Ratings for time series models, including some widely used packages such as fbprophet, are produced separately for different horizons. Specifically, we create a different Elo rating for looking k=1 steps ahead versus k=13 steps ahead, say. A rating is produced for each k in the Fibonacci sequence. See [skater_elo_ratings/leaderboards](https://github.com/microprediction/timemachines-testing/tree/main/skater_elo_ratings/leaderboards) sub-directories. For example some good ways to predict univariate time series 8 steps in advance might be suggested by the rankings at [/leaderboards/univariate_008](https://github.com/microprediction/timemachines-testing/tree/main/skater_elo_ratings/leaderboards/univariate_008) but of course their are caveats. 

### Optimizer Elo ratings and leaderboards

If you are looking for optimizer leaderboards, I moved those to [HumpDay](https://github.com/microprediction/humpday). The precise methodology is revealed in [comparison/eloratings.py](https://github.com/microprediction/humpday/blob/main/humpday/comparison/eloratings.py) and explained in the article [HumpDay: A Package to Help You Choose a Python Global Optimizer](http://www.microprediction.com/blog/humpday).
