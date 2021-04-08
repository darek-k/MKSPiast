"""
Kopia pliku - gdybym tamtą rozjebał  #todo usuń ten plik
"""

"""
Do usunięcia ten plik jak już zostanie to dodane do widoków
"""

import requests
from bs4 import BeautifulSoup

url = 'http://www.pomorskifutbol.pl/liga.php?id=1309'
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

schedule = soup.find('table', class_='terminarz')
matchweeks = schedule.find_all('tr')

# for i in matchweeks:
#     print(i)
#     print('\n')

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
        match_dict['home_team'] = home_team.text
        match_dict['away_team'] = away_team.text
        match_dict['home_goals'] = goals.text[1:3]
        match_dict['away_goals'] = goals.text[-2:]
        match_dict['day'] = (date.text[-13:-7]).strip()
        match_dict['hour'] = (date.text[-5:]).strip()

        matches_dict[matchweek_number].append(match_dict)

# print(matches_dict)


url = 'https://regiowyniki.pl/druzyna/Pilka_Nozna/Pomorskie/Piast_Czluchow/kadra/'
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

players_table = soup.find('table')
players = players_table.find_all('tr')

players_dict = {}
for player in players:
    player_name = player.find('td')
    player_birthday = player.find('td', class_='text-muted')
    if player_name:
        players_dict[player_name.text] = {'first_name': (player_name.text).split(' ')[0],
                                          'last_name': (player_name.text).split(' ')[1]}
    if player_birthday:
        players_dict[player_name.text]['birth_date'] = player_birthday.text

print(players_dict)
