# NBARefs
A repository with our CS122 Project about NBA refereeing

The compressed file NBA.tar.gz contains the large folder that configures the website. I was able to unzip the file on my VM to get the folder so hopefully that shouldn't be a problem. There is another README in that folder to explain how to get to the website.

When using the exported VM, please use the cs122-project directory for the website configuration.

Contents:
A database of NBA .. .docx - Word document containing the original proposal of our project
NBA.tar.gz - Compressed folder containing the website configuration. See the introduction of this file for more info
NBARefs.db - The final database used for statistical analysis
NBAStat_Final.xlsx - The cleaned up version of the PDFs using Adobe Acrobat
Output.csv - The file mapping each referee to the game codes of the games they officiated. It is the csv version of the referees table in the final database
NBAStat.txt - A tab delimited txt file containing the same data as NBAStat_Final.xlsx
Referees.py - A file containing the functions that generate Output.csv
Sorted300, Sorted400 - The lists of referees sorted by accuracy with cutoffs at 300 and 400 respectively
create-db.sql - The sql query that generates NBARefs.db
data_dict.csv - The output of parser.py. It is the csv version of the calls table in the final database
parser.py - The code that generates data_dict.csv
proportion_shooting.csv - The list of referees by proportion of shooting fouls over total fouls
ranking.csv - The list of all referees in the dataset, with incorrect calls, incorrect non calls, total incorrect calls, total calls and error ratio
ranking.sql - The sql query that generates ranking.csv
star_players.csv - A csv file containing the error ratios for star players in our dataset.
statistical_analysis.py - The code that generates all of the stats that we used in our paper
top_teams.csv - A file containing the ratio of games including top teams officiated by the top and bottom 10 referees by accuracy
util.py - A function containing auxiliary methods used to generate Output.csv. It is the same file that was provided to us in PA2
