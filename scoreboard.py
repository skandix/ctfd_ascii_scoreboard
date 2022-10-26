#!/usr/bin/env python3
import requests
import os

from os import getenv
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()


class ascii_scoreboard:
    def __init__(self):
        self.url = "https://ctf.uia.no"
        self.token = getenv("ctfd_token")
        self.s = requests.session()
        self.s.headers.update({"Content-Type": "application/json"})
        self.s.headers.update({"Authorization": f"Token {self.token}"})
        self.api = lambda route: self.s.get(f"{self.url}/api/v1/{route}").json()["data"]

    def getTeams(self):
        return self.api("teams")

    def getOnsiteList(self):
        return [
            (data["pos"], data["name"], data["score"])
            for data in self.getScoreboard()
            if data["account_id"] in self.getOnsite()
        ]

    def getOffsiteList(self):
        return [
            (data["pos"], data["name"], data["score"])
            for data in self.getScoreboard()
            if data["account_id"] not in self.getOnsite()
        ]

    def formatScoreboard(self):
        HEADER = ["SITE POS", "POS", "NAME", "SCORE"]

        print("\t=== OFFSITE ===")
        offsite = self.re_indexTeam(self.getOffsiteList())
        print(tabulate(offsite, headers=HEADER), "\n")

        print("\t=== ONSITE ===")
        onsite = self.re_indexTeam(self.getOnsiteList())
        print(tabulate(onsite, headers=HEADER))

    def re_indexTeam(self, site_list: list):
        return [[key + 1, val[0], val[1], val[2]] for key, val in enumerate(site_list)]

    def getScoreboard(self):
        return self.api("scoreboard")

    def getOnsite(self):
        onsite = [
            (team["fields"][0]["value"], team["id"])
            for team in self.api("teams")
            if team["fields"][0]["value"] == True
        ]
        return [teams[-1] for teams in onsite]


score = ascii_scoreboard()
(score.formatScoreboard())
quit(137)
