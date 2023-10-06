from bs4 import BeautifulSoup
import requests

BASE_URL = "https://games.crossfit.com/workouts/open/{year}/"
BASE_URL_WITH_WORKOUT_NUM = "https://games.crossfit.com/workouts/open/{year}/{workout_num}?division=1"

d = {"wall walks", "dumbbell snatches", "box jump-overs"}


def main():

    years = [2022, 2023]

    for year in years:
        resp = requests.get(BASE_URL.format(year=year))
        resp.raise_for_status()
        parsed_html = BeautifulSoup(resp.text, "html.parser")

        data = parsed_html.body.findAll('div', attrs={'class': 'ordinals'})
        links = []
        for div in data:
            links = div.findAll('a')
        workout_nums = range(1, len(links)+1)
        for workout_num in workout_nums:
            resp = requests.get(BASE_URL_WITH_WORKOUT_NUM.format(year=year, workout_num=workout_num))
            resp.raise_for_status()
            parsed_html = BeautifulSoup(resp.text, "html.parser")
            print(parsed_html.body.find('div', attrs={'class': 'exercises'}).text)


if __name__ == '__main__':
    main()