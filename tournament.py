#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("DELETE from matches")    
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 
    c.execute("DELETE FROM tournament")
    db.commit()
    db.close()  


def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 
    c.execute("Select count(*) as num FROM tournament;")
    db.commit()
    counter = c.fetchone()[0]
    db.close()
    return counter


def registerPlayer(playername):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    
    create a player called First Player
    --Don't need to add id -- this is a serial & primary key"""
    
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 
    c.execute( "insert into tournament (name) values(%s)", (playername,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 
    c.execute("select * from standings;")
    db.commit
    rankings= c.fetchall()
    db.close()
    return rankings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 
    c.execute("insert into matches(winner, loser) values(%s,%s)", (winner, loser))
    db.commit()
    db.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
     
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor() 

    # Get the standings from the view standings
    c.execute("select id, name from standings;")
    standings = c.fetchall()

    # Get the number of players
    c.execute("select count(id) as totalplayers from tournament;")
    tp= c.fetchall()
    totalPlayers = tp[0][0]
    numPairs = int(totalPlayers) / 2
    
    pairs = range(numPairs)

    # Create the pairs
    for i in range(0, numPairs + 1, 4):
        pairs = [(standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1]), 
            (standings[i+2][0],standings[i+2][1],standings[i+3][0],standings[i+3][1])]

    db.close()
    return pairs


