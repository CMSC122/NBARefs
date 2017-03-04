import re
import util 
import bs4
import queue
import json
import sys
import csv
import string
import urllib.parse
import requests
import os

home_team_dict = {'76ers':'PHI', 'Bucks':'MIL', 'Bulls': 'CHI', 'Cavaliers':'CLE',
'Celtics':'BOS', 'Clippers': 'LAC', 'Grizzlies':'MEM', 'Hawks':'ATL', 'Heat':'MIA',
'Hornets':'CHO', 'Jazz':'UTA', 'Kings':'SAC', 'Knicks':'NYK', 'Lakers':'LAL', 'Magic':'ORL',
'Mavericks':'DAL', 'Nets': 'BRK', 'Nuggets':'DEN', 'Pacers':'IND', 'Pelicans':'NOP',
'Pistons':'DET', 'Raptors':'TOR', 'Rockets':'HOU', 'Spurs':'SAS', 'Suns':'PHO',
'Thunder':'OKC', 'Timberwolves':'MIN', 'Trail Blazers':'POR', 'Warriors':'GSW','Wizards':'WAS'}

months_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03','Apr':'04', 'May':'05',
'Jun':'06', 'June':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

def get_referees(url):

    base_url = 'http://www.basketball-reference.com/boxscores/'
    comp_url = base_url + url + '.html'

    request = util.get_request(comp_url)

    if request != None:
        html = util.read_request(request)
        if html != None:
            soup = bs4.BeautifulSoup(html, "html5lib")
    div_tags = soup.find_all('div')
    good_tags = str(div_tags)
    string = re.findall(r'(?<=Officials:)(.*?)(?=\<br)', good_tags)
    
    rv = re.findall(r'(?<=.html\"\>)(.*?)(?=<\/a)',string[0])
    return rv

def get_code(filename):
    rv = []
    myfile = open(filename, 'r')
    data = myfile.read().replace('\n', ' ')
    
    teams = re.findall(r'@ (.*?) \(?[0-9]*\)? ?\((.*?) (.*?), (.*?)\)', data)
    

    for element in teams:
        rv.append(element[3]+months_dict[element[1]]+ element[2]+ '0' + home_team_dict[element[0]])

    return list(set(rv))


def extract_refs(filename):
    rv = []
    codes = get_code(filename)
    for item in codes:
        print(item + ' Still getting it')
        for index in range(len(get_referees(item))):
            rv.append((item, get_referees(item)[index]))

    with open('Output.csv', 'w', newline='') as csvf:
        line_writer = csv.writer(csvf, delimiter = '|')
        for tuple in rv:
            print('Writing')
            line_writer.writerow([str(tuple[0]), tuple[1]])
        return csvf