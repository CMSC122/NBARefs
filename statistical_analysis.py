#Statistical Analysis of NBA Referees
#Amanda Li, Connor Turkatte, Fernando De Stefanis, Steven Wei

import pandas
import math
import sqlite3
import csv

top_refs = ['Mark Lindsay',
'Tony Brothers',
'Lauren Holtkamp',
'Steve Anderson',
'Kevin Scott',
'Bill Kennedy',
'J.T. Orr',
'Nick Buchert',
'James Capers',
'Derek Richardson']
top_10 = ['Jason Phillips', 
'Monty McCutchen',  
'Scott Foster', 
'Josh Tiven',   
'Kane Fitzgerald', 
'Eric Lewis',   
'Marc Davis',
'Ken Mauer',  
'Tom Washington',
'Tony Brothers']  
top_teams = ['Warriors', 'Spurs', 'Cavaliers', 'Raptors',
    'Thunder', 'Clippers', 'Hawks', 'Celtics']
bottom_refs = ['Bennie Adams',
'Gary Zielinski',
'David Jones',
'Josh Tiven',
'Tony Brown',
'Derrick Stafford',
'Leroy Richardson',
'Matt Boland',
'Mike Callahan',
'Tre Maddox']
star_players = ['Stephen Curry', 'Kawhi Leonard', 'Kevin Durant', 
'Russell Westbrook', 'Kyle Lowry', 'Paul George', 'Carmelo Anthony', 
'Dwyane Wade', 'LeBron James','Anthony Davis', 'James Harden', 
'Giannis Antetokounmpo', 'Kyrie Irving', 'Jimmy Butler', 'Marc Gasol',
 'Klay Thompson', 'LaMarcus Aldridge', 'Pau Gasol', 'John Wall']

def generate_ranking(filename = 'ranking.csv', num = 300):
    '''
    returns a ranking of the best referees in the NBA by ratio of 
    incorrect calls over total calls. It eliminates referees with 
    fewer than num calls on our dataset, with a preset value of
    300. At the preset value, this excludes 9 out of 70 
    referees in total. 
    Inputs:
    A filename corresponding to a file
    containing the list of all referees in the dataset,
    with the total number of calls, incorrect calls, incorrect 
    non calls, total incorrect calls, and incorrect to correct call
    ratio.
    An integer corresponding to the minimum number of calls we 
    want to have for the cutoff

    '''

    ranking = pandas.read_csv(filename)

    sorted_ranking = ranking[ranking['total']>num].sort('percentage', ascending = True)
    return sorted_ranking

def variation_coefficient(filename = 'ranking.csv', number = 300):

    '''
    Returns the standard deviation, mean and variation_coefficient
    for the incorrect calls, the error ratio for a ranking without
    cutoff, and the error ratio for a ranking with cutoff. 
    Note that only the latter two are used in the paper
    '''

    ranking = pandas.read_csv(filename)

    stdev_calls = math.sqrt(ranking['totali'].var())
    mean_calls = ranking['totali'].mean()
    calls_variation_coefficient = stdev_calls/mean_calls

    stdev_error = math.sqrt(ranking['percentage'].var())
    mean_error = ranking['percentage'].mean()
    error_variation_coefficient = stdev_error/mean_error

    sorted_ranking = generate_ranking(num = number)

    stdev_error_sort = math.sqrt(sorted_ranking['percentage'].var())
    mean_error_sort = sorted_ranking['percentage'].mean()
    error_variation_coefficient_sort = stdev_error_sort/mean_error_sort

    print('The stats for calls are', stdev_calls, mean_calls, calls_variation_coefficient)
    print('The stats for unsorted errors are', stdev_error, mean_error, error_variation_coefficient)
    print('The stats for sorted errors are', stdev_error_sort, mean_error_sort, error_variation_coefficient_sort)



 
def analysis(filename = 'proportion_shooting.csv'):
    '''
    Returns the mean and standard deviation for a certain Statistic
    for the first 10 and last 10 elements of a given csv file.
    Very often throughout the paper we try to get information for the
    same statistic for the top and bottom 10 (players, referees, etc)
    '''

    shots = pandas.read_csv(filename)
    mean_top = shots[0:10]['Ratio'].mean()
    stdev_top = math.sqrt(shots[0:10]['Ratio'].var())
    mean_acc = shots[10:]['Ratio'].mean()
    stdev_acc = math.sqrt(shots[10:]['Ratio'].var())
    return mean_top, stdev_top, mean_acc, stdev_acc

def proportion_shooting(filename = 'NBARefs.db'):
    '''
    This function computes the proportion of shooting fouls 
    over total fouls amongst the calls by a given referee in our
    top 10 by accuracy and top 10 by number of calls. It
    generates a csv file that is a suitable input for analysis()
    '''
    con = sqlite3.connect(filename)

    cur = con.cursor()

    rv = [('Name', 'Total Fouls', 'Shooting Fouls', 'Ratio')]
    for element in top_10:
        total = cur.execute('select count(*) from calls join referees\
        on calls.game_code=referees.game_code where referee_name = ?', [element])
        total_no = total.fetchall()[0][0]
        shooting = cur.execute('select count(*) from calls join referees\
        on calls.game_code=referees.game_code where call_type = ? and referee_name = ?',
        ['Foul: Shooting', element])
        shooting_no = shooting.fetchall()[0][0]
        rv.append((element, total_no, shooting_no, shooting_no/total_no))


    for element in top_refs:
        total = cur.execute('select count(*) from calls join referees\
        on calls.game_code=referees.game_code where referee_name = ?', [element])
        total_no = total.fetchall()[0][0]
        shooting = cur.execute('select count(*) from calls join referees\
        on calls.game_code=referees.game_code where call_type = ? and referee_name = ?',
        ['Foul: Shooting', element])
        shooting_no = shooting.fetchall()[0][0]
        rv.append((element, total_no, shooting_no, shooting_no/total_no))
    cur.close()
    del cur
    con.close()

    f = open("top_teams.csv","w")
    out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)
    for tup in rv:
        out.writerow(tup)
    f.close()
    return rv




def better_teams(filename = 'NBARefs.db'):

    '''
    This function returns the proportion of games by top teams 
    officiated by referees in the top and bottom 10 by accuracy 
    lists. It also generates a csv file that is a suitable input
    for the analysis() function
    '''

    con = sqlite3.connect(filename)

    cur = con.cursor()
    rv = [('Name', 'Games with Top Teams', 'Total Games with Top Teams', 'Ratio')]
    for ref in top_refs:
        ref_counter = 0
        game_counter = 0
        for team in top_teams:
            referee = cur.execute('select count(distinct game_name) from calls join referees\
            on calls.game_code=referees.game_code where referee_name = ? \
            and home_team = ? or away_team = ?', [ref, team, team])
            ref_counter += referee.fetchall()[0][0]
            total = cur.execute('select count(distinct game_name) from calls join referees\
            on calls.game_code=referees.game_code where home_team = ? or away_team = ?',
            [team, team])
            game_counter += total.fetchall()[0][0]
        rv.append((ref, ref_counter, game_counter, ref_counter/game_counter))

    for ref in bottom_refs:
        ref_counter = 0
        game_counter = 0
        for team in top_teams:
            referee = cur.execute('select count(distinct game_name) from calls join referees\
            on calls.game_code=referees.game_code where referee_name = ? \
            and home_team = ? or away_team = ?', [ref, team, team])
            ref_counter += referee.fetchall()[0][0]
            total = cur.execute('select count(distinct game_name) from calls join referees\
            on calls.game_code=referees.game_code where home_team = ? or away_team = ?',
            [team, team])
            game_counter += total.fetchall()[0][0]
        rv.append((ref, ref_counter, game_counter, ref_counter/game_counter))

    cur.close()
    del cur
    con.close()
    f = open("top_teams.csv","w")
    out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)
    for tup in rv:
        out.writerow(tup)
    f.close()
    return rv
    


def better_players(filename = 'NBARefs.db'):
    '''
    Returns the error ratios for calls involving the 
    star players
    '''

    con = sqlite3.connect(filename)

    cur = con.cursor()
    rv = [('Name', 'Total Incorrect Calls and Non-Calls', 'Total Calls', 'Ratio')]
   
    for player in star_players:
        totali = cur.execute('select count(*) from calls  where (committing_player = \
            ? or disadvantaged_player = ?) and (call_accuracy\
            = ? or call_accuracy = ?)', [player, player, 'INC', 'IC']);
        total_inc = totali.fetchall()[0][0]
        total = cur.execute('select count(*) from calls where committing_player = ?\
          or disadvantaged_player = ?', [player, player])
        total_calls = total.fetchall()[0][0]
        rv.append((player, total_inc, total_calls, total_inc/total_calls))
        


    cur.close()
    del cur
    con.close()
    f = open("star_players.csv","w")
    out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)
    for tup in rv:
        out.writerow(tup)
    f.close()
    return rv    

def analysis2(filename = 'star_players.csv'):
    '''
    This function is identical to analysis, but it 
    returns the statistics for the entire file instead of
    dividing it into two categories. 
    '''
    shots = pandas.read_csv(filename)
    mean= shots['Ratio'].mean()
    stdev = math.sqrt(shots['Ratio'].var())
    return mean, stdev