"""
Do usunięcia ten plik jak już zostanie to dodane do widoków #todo usuń ten plik
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime


def take_soup(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def take_match_data():
    schedule = take_soup('http://www.pomorskifutbol.pl/liga.php?id=1309').find('table', class_='terminarz')
    matchweeks = schedule.find_all('tr')

    matches_dict = {}
    for data in matchweeks:
        matchweek = data.find_all('td', class_='kolejka')
        if matchweek:
            matchweek_number = int(matchweek[0].text[11:13])
            matches_dict[matchweek_number] = []

        home_team = data.find('td', class_='druzyna-1')
        away_team = data.find('td', class_='druzyna-2')
        goals = data.find('td', class_='wynik')
        date = data.find('td', class_='data-meczu')

        if home_team:
            match_dict = {}
            match_dict['matchweek_number'] = matchweek_number
            match_dict['home_team'] = home_team.text
            match_dict['away_team'] = away_team.text
            match_dict['home_goals'] = goals.text[1:3]
            match_dict['away_goals'] = goals.text[-2:]

            if date.text != '':
                day = date.text.split(' ')[0].strip()
                month = date.text.split(' ')[3][-2:]
                year = date.text.split(' ')[3][:4]
                time = date.text.split(' ')[5]
                full_date = f"{day} {month} {year} {time}"
                date_as_datetime = datetime.strptime(full_date, '%d %m %Y %H:%M')
                print(type(date_as_datetime))
                match_dict['date'] = date_as_datetime

            matches_dict[matchweek_number].append(match_dict)

    return matches_dict


# print(take_match_data())


def download_teams():
    table = take_soup('http://www.pomorskifutbol.pl/liga.php?id=1309').find('table', class_='tabela')
    rows = table.find_all('tr')[2:]

    team_dict = {}
    for row in rows:
        cells = row.find_all('td')
        club_name = cells[1].text.strip()
        team_dict[club_name] = {}
        team_dict[club_name]['matches'] = int(cells[2].text)
        team_dict[club_name]['points'] = int(cells[3].text)
        team_dict[club_name]['win'] = int(cells[4].text)
        team_dict[club_name]['draw'] = int(cells[5].text)
        team_dict[club_name]['loose'] = int(cells[6].text)
        team_dict[club_name]['goals_shot'] = int(cells[7].text[:3])
        team_dict[club_name]['goals_lost'] = int(cells[7].text[-3:])

    return team_dict


def download_matches():
    schedule = take_soup('http://www.pomorskifutbol.pl/liga.php?id=1309').find('table', class_='terminarz')
    matchweeks = schedule.find_all('tr')

    matches_dict = {}
    for data in matchweeks:
        matchweek = data.find_all('td', class_='kolejka')
        if matchweek:
            matchweek_number = int(matchweek[0].text[11:13])
            matches_dict[matchweek_number] = []

        home_team = data.find('td', class_='druzyna-1')
        away_team = data.find('td', class_='druzyna-2')
        goals = data.find('td', class_='wynik')
        date = data.find('td', class_='data-meczu')

        if home_team:
            match_dict = {}
            match_dict['matchweek_number'] = matchweek_number
            match_dict['home_team'] = home_team.text
            match_dict['away_team'] = away_team.text
            match_dict['home_team_goals'] = goals.text[1:3]
            match_dict['away_team_goals'] = goals.text[-2:]
            if date.text != '':
                day = date.text.split(' ')[0].strip()
                month = date.text.split(' ')[3][-2:]
                year = date.text.split(' ')[3][:4]
                try:
                    time = date.text.split(' ')[5]
                except:
                    time = '00:00'
                full_date = f"{day} {month} {year} {time}"
                date_as_datetime = datetime.strptime(full_date, '%d %m %Y %H:%M')
                match_dict['date'] = date_as_datetime
            elif date.text == '':
                match_dict['date'] = "2021-01-01"

            matches_dict[matchweek_number].append(match_dict)

    return matches_dict

matches_dict = download_matches()
print(matches_dict)

for key, value in matches_dict.items():
    print(value)