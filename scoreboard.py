#!/usr/bin/env python3
import requests
import os

from os import getenv
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

class ascii_scoreboard():
  def __init__(self):
    self.url = "https://ctf.uia.no"
    self.token = getenv('ctfd_token')
    self.s = requests.session()
    self.s.headers.update({'Content-Type': 'application/json'})
    self.s.headers.update({"Authorization": f"Token {self.token}"})
    self.api = lambda route: self.s.get(f"{self.url}/api/v1/{route}").json()['data']

  def getTeams(self):
    return (self.api('teams'))

  def formatScoreboard(self):
    onsite = []
    offsite = []
    for data in self.getScoreboard():
      team_id = data['account_id']
      if team_id in self.getOnsite():
        onsite.append((data['pos'], data['name'], data['score']))

      else:
        offsite.append([data['pos'], data['name'], data['score']])

    print ("\n===\tONSITE\t===")
    print(tabulate(onsite, headers=["POS","NAME", "SCORE"])) 

    print ("\n===\tOFFSITE\t===")
    print(tabulate(offsite, headers=["POS","NAME", "SCORE"]))

  def getScoreboard(self):
    return (self.api('scoreboard'))

  def getOnsite(self):
    onsite = ([(team['fields'][0]['value'], team['id']) for team in self.api('teams') if team['fields'][0]['value'] == True])
    return [teams[-1]for teams in onsite]

score = ascii_scoreboard()
(score.formatScoreboard())
quit(137)
