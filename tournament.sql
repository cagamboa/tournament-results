-- Table definitions for the tournament project.
--

--create the database called tournament
create db
	tournament;

\c tournament;

--create the table called tournament
create table tournament ( 
	id serial primary key, 
	name text);

--create the table called matches
create table matches (
	matchNumber serial primary key, 
	winner integer references tournament(id), 
	loser integer references tournament(id));

--create a view of the wins
create view wins as select id, name, count(winner) as wins 
	from tournament left join matches on tournament.id = matches.winner 
	group by id order by wins desc;

--create a view of the losses
create view losses as select id, count(loser) as losses 
	from tournament left join matches on tournament.id = matches.loser 
	group by id order by losses desc;

--create a view combining the wins and losses into one view	
create view totalMatches as select wins.id,name,wins,losses 
	from wins, losses where wins.id = losses.id;

--create a view of the player id and total matches played
create view totals as select wins.id, sum(wins + losses) as total 
	from wins, losses where wins.id = losses.id group by wins.id;

--create a view of the player standings. It will show the id, name, wins, total matches played
create view standings as select totalMatches.id,name,wins, total 
	from totalMatches left join totals on totalMatches.id = totals.id order by wins desc;
