import collections
import json
import re
from collections import defaultdict
from pprint import pprint

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://games.crossfit.com/workouts/open/{year}/"
BASE_URL_WITH_WORKOUT_NUM = "https://games.crossfit.com/workouts/open/{year}/{workout_num}?division=1"
BASE_URL_WITH_WORKOUT_NUM_OLD = "https://games.crossfit.com/workouts/open/{year}/#workoutsTab{workout_num}"

# bar muscle-ups


# ground-to-overheads -> snatch

mapping = {
    # snatches
    "ground-to-overheads": "snatches",
    "dumbbell snatches": "snatches",
    # thrusters
    "dumbbell thrusters": "thrusters",
    # muscle ups
    "bar muscle-ups": "muscle-ups",
    "ring muscle-ups": "muscle-ups",
}

all_movements = {
    "wall walks",
    "snatches",
    "dumbbell snatches",
    "chest-to-bar pull-ups",
    "deadlifts",
    "bar-facing burpees",
    "pull-ups",
    "thrusters",
    "dumbbell thrusters"
    "double-unders",
    "muscle-ups"
    "bar muscle-ups",
    "row",
    "toes-to-bars",
    "wall-ball shots",
    "cleans",
    "hang clean",
    "squat cleans",
    "jerk",
    "burpee pull-ups",
    "shuttle runs",
    "strict handstand push-ups",
    "handstand push-ups",
    "handstand walk",
    "snatches",
    "burpee box jump-overs",
    "box jump-overs",
    "front squats",
    "ground-to-overheads",
    "clean and jerks",
    "box jumps",
    "dumbbell box step-ups",
    "single-leg squats",
    "dumbbell overhead lunge",
    "dumbbell hang clean and jerks",
}

# 2017-2023
# 2011-2016


def main():
    years = range(2011, 2023 + 1)
    d = defaultdict(collections.Counter)
    d1 = defaultdict(dict)
    for year in years:
        print(f"Year = {year}")
        resp = requests.get(BASE_URL.format(year=year))
        resp.raise_for_status()
        parsed_html = BeautifulSoup(resp.text, "html.parser")

        if year < 2017:
            data = parsed_html.body.findAll('div', attrs={'class': 'tabs js-workout-tabs'})
        else:
            data = parsed_html.body.findAll('div', attrs={'class': 'ordinals'})

        links = []
        for div in data:
            links = div.findAll('a')
        workout_nums = range(1, len(links) + 1)
        for workout_num in workout_nums:
            print(f"workout = {workout_num}")
            if year < 2017:
                resp = requests.get(BASE_URL_WITH_WORKOUT_NUM_OLD.format(year=year, workout_num=workout_num))
                resp.raise_for_status()
                parsed_html = BeautifulSoup(resp.text, "html.parser")
                section = parsed_html.body.find('li', {'id': f'workoutsTab{workout_num}'})
                text = section.find('div', attrs={'class': 'drupal-inline-reset'}).text
                text = text.lower().split("women")[0]
            else:
                resp = requests.get(BASE_URL_WITH_WORKOUT_NUM.format(year=year, workout_num=workout_num))
                resp.raise_for_status()
                parsed_html = BeautifulSoup(resp.text, "html.parser")
                text = parsed_html.body.find('div', attrs={'class': 'exercises'}).text
            d1[year][workout_num] = text
            # for line in text.splitlines():
            #     movement = find_movement(line)
            #     if movement:
            #         d[year][movement] += 1
    with open("opens_raw.json", "w") as f:
        f.write(json.dumps(d1, indent=2))
    print("End")


def find_movement(line):
    for movement in all_movements:
        if movement in line.lower():
            return movement
        singular = movement.rstrip("s")

        if singular in line.lower():
            return movement


if __name__ == '__main__':
    main()
