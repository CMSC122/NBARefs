CREATE TABLE referees
  (game_code varchar(12),
   referee_name varchar(50));

.import Output.csv referees


CREATE TABLE calls
  (game_name varchar(50),
   away_team varchar(50),
   home_team varchar(50),
   time varchar(10),
   period varchar(5),
   call_type varchar(50),
   committing_player varchar(50),
   offending_team varchar(50),
   disadvantaged_player varchar(50),
   defending_team varchar(50),
   call_accuracy varchar(10),
   comment varchar(300)
   game_code varchar(12));

.import data_dict.csv calls