import re
import json
import sys
import csv

def main(filename):
    '''
    When I first took a crack at the data, I tried to just plug in each pdf 
    into a pdf readerthat would convert the data into a txt file. 
    I spent then several days and many hours trying to fix as many of the problems
    and base cases as I could. However, for every problem I fixed, I would 
    find a new one. So after talking with Professor Wachs,
    it was decided to take a new approach that would normalize the data.
    I then first used Adobe Acrobat to fist combine all of the pdfs into one large 
    pdf, instead of combining the separate txt files as I did in my first attempt.
    One of the major advtanges of Adobe Acrobat is its ability to convert pdfs 
    into excel spread sheets. From there, I was able to much more easily parse the data
    and return a text file with different categories. These are listed here:

    0 Game
    1 Name
    2 Period
    3 Time
    4 Call Type
    5 Committing Player
    6 Disadvantaged Player
    7 Review Decision
    8 UnMatched_Names
    9 Comments
    13 GameNo
    14 Line Type:
        1) Call 
        2) Comment 
        3) UnMatchedName

    There were many cases where the data was often misalligned, such as comments 
    would not always follow their corresponding call, so I primarily fixed this
    by manually fixing the data, which was now a lot easier to see and accomplish.
    '''


    data = open(filename, encoding="iso8859")
    data = data.readlines()

    result_list = []
    index_tracker = 0
    bad_dict = {}
    bad_list = []

    home_team_dict = {'76ers':'PHI', 'Bucks':'MIL', 'Bulls': 'CHI', 'Cavaliers':'CLE',
    'Celtics':'BOS', 'Clippers': 'LAC', 'Grizzlies':'MEM', 'Hawks':'ATL', 'Heat':'MIA',
    'Hornets':'CHO', 'Jazz':'UTA', 'Kings':'SAC', 'Knicks':'NYK', 'Lakers':'LAL', 'Magic':'ORL',
    'Mavericks':'DAL', 'Nets': 'BRK', 'Nuggets':'DEN', 'Pacers':'IND', 'Pelicans':'NOP',
    'Pistons':'DET', 'Raptors':'TOR', 'Rockets':'HOU', 'Spurs':'SAS', 'Suns':'PHO',
    'Thunder':'OKC', 'Timberwolves':'MIN', 'Trail Blazers':'POR', 'Warriors':'GSW','Wizards':'WAS'}

    months_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03','Apr':'04', 'May':'05',
    'Jun':'06', 'June':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'} 


    for index, line in enumerate(data):

        holder_dict = {}

        x = line.replace('"', '')
        x = x.strip()
        x = x.split("\t")

        if x[14] == '1.00':
            '''
            this code just create the appropiate key,val pairs 
            of the known calls in our txt file
            '''

            index_tracker = index 

            if x[13] == "25.00":
                holder_dict['game_name'] = "Hawks (114) @ Bucks (110) (Dec 09, 2016)"

            elif x[13] == "277.00":
                holder_dict['game_name'] = "Rockets (102) @ Thunder (99) (Dec 09, 2016)"

            elif x[13] == "489.00":
                holder_dict['game_name'] = "Knicks (103) @ Kings (100) (Dec 09, 2016)"

            elif x[13] == "596.00":
                holder_dict['game_name'] = x[0] + ')'

            elif x[13] == "602.00":
                holder_dict['game_name'] = x[0] + '17)'

            else: 
                holder_dict['game_name'] = x[0]

            if len(x[2]) != 0:
                holder_dict['period'] = x[2][1]
            else:
                holder_dict['period'] = '4'

            holder_dict['time'] = x[3]

            holder_dict['call_type'] = x[4]

            holder_dict['committing_player'] = x[5]
            holder_dict['disadvantaged_player'] = x[6]

            holder_dict['call_accuracy'] = x[7]

            if '*' in x[7]:
                w = x[7].replace('*','') 
                holder_dict['call_accuracy'] = x

            if len(x[9]) > 0:
                holder_dict['unmatched_names'] = x[8]


            holder_dict['comment'] = x[9]
            holder_dict['game_number'] = x[13]
            holder_dict['type'] = x[14]

        elif x[14] == '2.00':

            result_list[index_tracker]['comment'] += x[9]

        elif x[14] == '3.00':
            '''
            the purpose of this code is just to collect all of the 
            unmatched_names from each game (based on the title)
            and then to create a new dictionary (bad_dict) with the name 
            of the game as the key and a list of unmatched_names as the val
            '''

            if x[0] in bad_dict.keys():

                bad_dict[x[0]].append(x[8])

            else:

                bad_dict[x[0]] = [x[8]] 

        result_list.append(holder_dict)


    '''
    this code below is just to merely act a secondly check to make sure
    that all items in our list of dictionarys do no include any empty
    exceptions
    '''
    new_result_list = []
    for x in result_list:
        if len(x.keys()) > 0:
            new_result_list.append(x)



    for key, name_list in bad_dict.items():
        '''
        this code takes the list of unmatched_names for each game and matches
        to each game in the appropiate spot, disadvantaged_player or  
        committing_player. We accomplish this by first finding the
        last_name of each player and then searching in the comments for that
        last name so we know which call to attach the unmatched_names to. 
        '''

        for name in name_list:

            holder_boolean = False 

            x = name.split() 

            if len(x) == 3:
                last_name = x[-2:][0] + ' ' + x[-1]
                #this is just to address the issue if players have Jr. in their last name

            else:
                last_name = x[-1:][0]

            for dict_item in new_result_list:

                if dict_item['game_name'] == key:

                    if last_name in dict_item['comment'] and \
                        last_name not in dict_item['committing_player'] and \
                        last_name not in dict_item['disadvantaged_player']:

                        if holder_boolean == False:

                            if dict_item['committing_player'] == '':
                                dict_item['committing_player'] = name
                                holder_boolean = True 
                        
                            else: 
                                dict_item['disadvantaged_player'] = name
                                holder_boolean = True 


    for dict_item in new_result_list:
        '''
        this final part of the code serves as the 'everything else' category.
        Here we handle base cases that can actually be resolved, and we also
        find the game_code that will be used for extracting the ref names associated
        with each game. In addition, find the names of the home and away teams. 
        I have put comments for each section so it is clear which part 
        of the code handles what.
        '''


        x = dict_item['game_name']

        bad_string = "questions, please contact the NBA  here."

        if dict_item['game_number'] == '25.00':
            dict_item['game_name'] = 'Hawks (114) @ Bucks (110) (Dec 09, 2016)'

        if dict_item['game_number'] == '277.00':
            dict_item['game_name'] = 'Rockets (102) @ Thunder (99) (Dec 09, 2016)'

        if dict_item['game_number'] == '489.00':
            dict_item['game_name'] = 'Knicks (103) @ Kings (100) (Dec 09, 2016)'

        if bad_string in dict_item['comment']:
            dict_item['comment'] = dict_item['comment'].replace(bad_string, '')

        '''
        the above just handles base cases where some of the parsing 
        caused game names to not match properly 
        '''


        team = re.findall(r'@ (.*?) \(?[0-9]*\)? ?\((.*?) (.*?), (.*?)\)', x)
        if len(team) == 1:
            team = team[0]
            team_code = team[3] + months_dict[team[1]] + team[2] + '0' + home_team_dict[team[0]] 
            dict_item['game_code'] = team_code

        '''
        the above finds the game code for each game based on the 
        team code and date of the game
        '''


        w = dict_item['game_name'].split()

        check_boolean = False

        for word in w:

            if word == 'Blazers':

                word = 'Trail Blazers'

            if word in home_team_dict.keys():


                if check_boolean == False:

                    dict_item['away_team'] = word  
                    check_boolean = True 

                else:

                    dict_item['home_team'] = word

        if 'home_team' not in dict_item.keys():
            dict_item['home_team'] = 'None'

        if 'away_team' not in dict_item.keys():
            dict_item['away_team'] = 'None'

        '''
        the above code finds the names of the home and away teams based 
        on whether or not they appear in our database of NBA teams and team codes
        '''


        y = dict_item['comment'].split()

        for index, word in enumerate(y):
            if '(' in word:
                team_code = word[1:4]

                team_name = ''
                for key, val in home_team_dict.items():
                    if val == team_code:
                        team_name = key

                if team_code == 'PHX':
                    team_name = 'Suns'

                if team_code == 'CHA':
                    team_name = 'Hornets'

                if team_code == 'BKN':
                    team_name = 'Nets'

                last_name = y[index - 1]

                if '.' in last_name:
                    last_name = y[index - 2]

                if last_name[-2:] == "'s":
                    last_name = last_name[:-2]
                elif last_name[-1:] == "'":
                    last_name = last_name[:-1]
                else:
                    last_name = last_name

                x = dict_item['committing_player']
                z = dict_item['disadvantaged_player']

                if last_name in x:
                    dict_item['offending_team'] = team_name                
                elif last_name in z:
                    dict_item['defending_team'] = team_name

        if 'offending_team' not in dict_item.keys():
            dict_item['offending_team'] = 'None'
        if 'defending_team' not in dict_item.keys():
            dict_item['defending_team'] = 'None'

        '''
        similar to the away/home team code, the above code will look in the comment
        to figure out which team the committing player and disadvantaged player
        are apart of
        '''


        if dict_item['offending_team'] == '':

            if dict_item['defending_team'] == dict_item['home_team']:
                dict_item['offending_team'] = dict_item['away_team']

            elif dict_item['defending_team'] == dict_item['away_team']:
                dict_item['offending_team'] = dict_item['home_team']

        elif dict_item['defending_team'] == '':

            if dict_item['offending_team'] == dict_item['home_team']:
                dict_item['defending_team'] = dict_item['away_team']

            elif dict_item['offending_team'] == dict_item['away_team']:
                dict_item['defending_team'] = dict_item['home_team']

        if (dict_item['game_name'] == "Mavericks (96) @ Trail Blazers (95)" 
                                        and dict_item['time'] == "00:45.4"):

            dict_item['disadvantaged_player'] = "Damian Lillard"
            dict_item['defending_team'] = 'Trail Blazers'

        if dict_item['game_name'] == "Heat @ Jazz (Dec 01, 2016)":

            if dict_item['time'] == '01:37.0':
                dict_item['disadvantaged_player'] = 'James Johnson'
                dict_item['defending_team'] = 'Jazz'

            if dict_item['time'] == '00:01.0':
                dict_item['disadvantaged_player'] = 'James Johnson'
                dict_item['defending_team'] = 'Jazz'

        '''
        the code above is just used to act as a secondary backup. 
        In other words, the code will check to make sure that in every call
        the correct the team names are found in the defending team and 
        offending_team categories. In addition, this also fixes some mistakes
        that were found later using the code below
        '''

        '''
        The code below is solely used for the purposes of identifying where there are 
        gaps in the data. In other words, this code belows just finds out when fields
        are empty in each dictionary of our list. There are 472~ call items that are 
        missing some information, primarily call_accuracy. Howevever, about half 
        of these problems, are actually found in the original data from the NBA website.
        That is to say the original pdfs have gaps in their data as well.  
        '''

        for key, value in dict_item.items():
            if len(value) == 0:
                if key != 'disadvantaged_player' and key != 'committing_player':
                    bad_list.append(dict_item)
    

    return new_result_list     

def csv_writer(result_from_main):
    '''
    As is probably quite apparent, this code just creates a csv file from 
    result of the main function
    '''

    new_result_list = result_from_main

    writer = csv.writer(open('data_dict.csv', 'w', newline = ''), delimiter = "|")
    writer.writerow(['game_name', 'away_team', 'home_team', 'time', 
                    'period', 'call_type', 'committing_player', 'offending_team', 
                    'disadvantaged_player', 'defending_team', 'call_accuracy', 
                    'comment', 'game_code'])
    for dict_item in new_result_list:
        writer.writerow([dict_item['game_name'],
                        dict_item['away_team'],
                        dict_item['home_team'], 
                        dict_item['time'], 
                        dict_item['period'], 
                        dict_item['call_type'], 
                        dict_item['committing_player'],
                        dict_item['offending_team'], 
                        dict_item['disadvantaged_player'],
                        dict_item['defending_team'], 
                        dict_item['call_accuracy'], 
                        dict_item['comment'],
                        dict_item['game_code']])

