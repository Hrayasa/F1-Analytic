import fastf1 as ff1
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup cache for faster data loading
if not os.path.exists('cache'):
    os.makedirs('cache')
ff1.Cache.enable_cache('cache')

def get_race_data(season, race_name):
    """Loads and prepares race data for analysis."""
    try:
        race = ff1.get_session(season, race_name, 'R')
        race.load()
        laps = race.laps
        laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
        laps = laps.dropna(subset=['LapTimeSeconds'])
        return laps
    except Exception as e:
        print(f"Oops! Couldn't load {race_name} in {season}: {e}")
        return None

def analyze_race(season, race_name):
    """Analyzes a single race, calculating key metrics."""
    laps = get_race_data(season, race_name)
    if laps is None:
        return None

    results = {
        'season': season,
        'race': race_name,
        'driver_count': laps['Driver'].nunique(),
        'total_laps': laps['LapNumber'].max(),
        'average_lap_times': laps.groupby('Driver')['LapTimeSeconds'].mean().sort_values(),
        'fastest_lap_times': laps.groupby('Driver')['LapTimeSeconds'].min().sort_values(),
        'position_tracking': {
            driver: laps[laps['Driver'] == driver].sort_values(by='LapNumber')[['LapNumber', 'Position']]
            for driver in laps['Driver'].unique()
        },
        'lap_time_stats': laps.groupby('Driver')['LapTimeSeconds'].agg(['mean', 'min', 'max', 'std'])
    }
    return results

def analyze_seasons(start_year, end_year):
    """Analyzes multiple seasons, collecting data for each race."""
    season_data = {}
    for year in range(start_year, end_year + 1):
        try:
            schedule = ff1.get_event_schedule(year)
            season_results = {}
            for race in schedule['EventName']:
                analysis = analyze_race(year, race)
                if analysis:
                    season_results[race] = analysis
            season_data[year] = season_results
        except Exception as e:
            print(f"Whoops! Something went wrong with season {year}: {e}")
    return season_data

def visualize_season_trends(all_seasons_data):
    """Visualizes fastest lap trends across seasons."""
    fastest_laps_by_season = {}
    for year, races in all_seasons_data.items():
        fastest_laps = {race: data['fastest_lap_times'].min() for race, data in races.items() if 'fastest_lap_times' in data}
        fastest_laps_by_season[year] = fastest_laps

    plt.figure(figsize=(15, 8))
    for year, laps in fastest_laps_by_season.items():
        plt.plot(list(laps.keys()), list(laps.values()), label=str(year))

    plt.title('Fastest Lap Times: Season by Season')
    plt.xlabel('Races')
    plt.ylabel('Fastest Lap Time (seconds)')
    plt.xticks(rotation=45)
    plt.legend(title='Season')
    plt.tight_layout()
    plt.show()

# Let's go!
if __name__ == "__main__":
    start_year = 2018
    end_year = 2023

    all_season_results = analyze_seasons(start_year, end_year)
    visualize_season_trends(all_season_results)

    # Quick summary
    for year, races in all_season_results.items():
        print(f"\nQuick look at {year}:")
        print(f"  Races: {len(races)}")



'''
TO RUN THE PROGRAM, YOU CAN EITHER OPEN THE TERMINAL AND WHERE THE FILE IS PRESENT OR OPEN AND INTERGRATED TERMINAL 
The enter the command 

                                        python f1_analysis.py
'''