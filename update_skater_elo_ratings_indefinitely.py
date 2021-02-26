from update_skater_elo_ratings import update_skater_elo_ratings_once
import traceback

if __name__=='__main__':
    while True:
        try:
            update_skater_elo_ratings_once()
        except Exception:
            traceback.print_tb()