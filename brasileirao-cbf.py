# This script extracts from the CBF website (www.cbf.com.br), for
# years 2007-2010, all the rounds of Campeonato Brasileiro de Futebol
# (Serie A), containing 10 matches each.
#
# Author: Andre Lima (twitter: @andlima)
# Licensed under the MIT license:
#  - http://www.opensource.org/licenses/mit-license.php

import urllib
import time
import os
from BeautifulSoup import BeautifulSoup

import championship

BASE_URL = ("http://www.cbf.com.br/ServiceJogosDaRodadaCampeonatoBrasileiro?"
            "serie=S%%C3%%A9rie%%20A&ano=%d&rodada=%d")
BASE_DIR = os.path.join(".", "cache")
BASE_FILE_NAME = "campeonato-brasileiro-year-%d-round-%02d.html"
FILE_PATH = os.path.join(BASE_DIR, BASE_FILE_NAME)

def make_sure_dir_exists():
    try:
        os.mkdir(BASE_DIR)
    except OSError as e:
        if e.errno != 17:
            exit()

def handle_file(year, round_):
    file_path = FILE_PATH % (year, round_)
    try:
        with open(file_path, 'r') as f:
            #print(" - Cache of file found on %s." % file_path)
            lines = [line.strip() for line in f]
        content = '\n'.join(lines)
    except IOError:
        url = BASE_URL % (year, round_)
        #print(" - Cache not found. Downloading file from %s..." % url)
        lines = urllib.urlopen(url).readlines()
        with open(file_path, 'w') as f:
            f.writelines(lines)
        content = ''.join(lines)
    return content

def set_result(results_dict, home, away, result):
    try:
        results_dict[home][away] = result
    except KeyError:
        results_dict[home] = {away: result}

def handle_match(match):
    home, away = [team['title'] for team in match.findAll('img')]
    score = [item.string for item in match.findAll('strong')[:2]]
    home_score, away_score = [int(item) for item in score]
    return (home, away, (home_score, away_score))

make_sure_dir_exists()

for year in range(2007, 2011):
    results_dict = {}
    for round_ in range(1, 39):
        soup = BeautifulSoup(handle_file(year, round_))
        matches = soup.findAll('dd')
        for match in matches:
            (home, away, result) = handle_match(match)
            set_result(results_dict, home, away, result)
    teams = results_dict.keys()
    teams.sort()
    matrix = [[i != j and results_dict[home][away]
               for j, away in enumerate(teams)]
              for i, home in enumerate(teams)]
    print 'year', year
    championship.process(teams, matrix)
    print '----'
    print
