from datetime import datetime
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
import requests
import os
os.chdir("G:\\My Drive\\Freelancing\\Web Scraping")  # set the directory if you'll need to save files
import lxml





home = "https://salarysport.com"
domain = "https://salarysport.com/football/"
html = requests.get(domain)
bs = BS(html.text, features="lxml", exclude_encodings=["ISO-8859-1"])
bs = BS(html.content, 'html.parser')

PremierLeagueTeams = 0
LaLiga = 4
Budensliga = 5
Ligue_1 = 6
Seria_A = 7

ChosenLeague = Ligue_1 # Change the league you want the data for


League = bs.find_all('div', {'class':"Layout__Box-sc-19mb7gg-0 Layout__Flex-sc-19mb7gg-1 OtherLinks__LinkContainer-sc-nrnd7r-0 jykxYM hkTbms bsemwg"})[ChosenLeague]

FootballLeagueTeamsLinks = League.find_all('a',href=True)
links = [home + link['href'] for link in FootballLeagueTeamsLinks]


dta = pd.DataFrame({"PlayerName": [], "WeeklyWage":[], "AGE":[], "Positions":[], "Nationality":[]})



    
###########

DT = pd.DataFrame({"Player Name": [], "Weekly Wage":[], "Yearly Salary": [], "Age":[], "Position":[], "Nationality":[], "Team":[]})
for link in links:
    html2 = requests.get(link)
    bs2 = BS(html2.content, 'html.parser')
    Players = bs2.find(lambda tag: tag.name=='table')
    TeamPlayers = pd.read_html(str(Players))[0]
    
    print("Extracting page: ", links.index(link)+1)

    team = bs2.find('h1',{'class':'Typography__H1-sc-1byk2c7-0 gjjWeX'}).text
    team = team[0:len(team)-20]
    TeamPlayers['Team'] = team
    if team[-11:] != 'Highest Pai':
        TeamPlayers["Weekly Wage"] = pd.to_numeric(TeamPlayers["Weekly Wage"].str[1:].str.replace(',',''))
        TeamPlayers["Yearly Salary"] = pd.to_numeric(TeamPlayers["Yearly Salary"].str[1:].str.replace(',',''))
        TeamPlayers = TeamPlayers.dropna(axis=0, subset= ["Weekly Wage","Yearly Salary"])
    
    if team[-11:] != 'Highest Pai':
        DT  = pd.concat([DT, TeamPlayers], ignore_index=True)
    print(team)


DT.to_csv("Ligue 1 Players Salary.csv", index=False,encoding='utf-8-sig')