##########################################
#### Building the useful data structures from the basketball html files #####
#########################################
from bs4 import BeautifulSoup
import re
from numpy import *
import glob
import operator

###########################
### some tweakable parameters
no_of_top=2  ### number of top players to calculate "spread of scoring"
stat_categories=['Reb','Pts','A']


#### getting the html for the base url
html=open('basketball.html','r')
soup=BeautifulSoup(html.read(),'lxml')


#### getting the game outcomes

rows=soup.body.find_all('tr')
win_loss=[]
home_away=[]
for x in rows:
    if len(x)==11 and x.find_all('td'):
        if x.find_all('td')[3].text in ['W','L']:  ### game information
            win_loss.append(x.find_all('td')[3].text=='W')
            home_away.append(x.find_all('td')[1].text[0]!='@')

home_away=[1 if x==True else 0 for x in home_away]  #### 1 if the game is at home
win_loss=[1 if x==True else 0 for x in win_loss]  #### 1 if the game is a win
 

################################
##### filling in player data for each game
#######################

### getting list of player names
players=[x.text for x in soup.body.find_all('a',{'href':re.compile('player/d*')})][4:]  

##### getting the stat categories (e.g., Rebounds, Points, Assists)
list_of_html_files=glob.glob('./*.html')
cat_soup=BeautifulSoup(open(list_of_html_files[0],'r').read(),'lxml')
categories=[x.text for x in cat_soup.body.find_all('th',{'style':lambda x: x and x.startswith('background')})][:16]
stats_index=[]
for x in stat_categories:
    if x in categories:
        stats_index.append(categories.index(x)+3)
    else:
        raise Exception('You did not enter an acceptable stat category') 


### preallocating the arrays for player data
player_data=dict()
for ind in players:
    player_data[ind]=zeros((3,len(game_links)))  ### rebounds, points, minutes played


### going through each html file, finding the data for each gape
game_index=0
for files in list_of_html_files:
    if len(files)==12:
        html=open(files,'r')
        soup_game=BeautifulSoup(html.read(),'lxml')
        
        
        for all_players in soup_game.findAll('tr'):
            if all_players.a:  ### our player
                temp_stats=[x.text for x in all_players.find_all('td')]
                player_data[temp_stats[1]][:,game_index]=[temp_stats[x] for x in stats_index]
        
        game_index+=1    
    

##### this function calculates total value of each stat per game                                
def events_per_game(which_stat):
    events=0
    for x in player_data:
        events=events+player_data[x][stat_categories.index(which_stat)]
    return events

##### total rebounds per game
reb_per_game=events_per_game('Reb')

##### calculate the "scoring spread" for each game (fraction of points produced by the top N scorers, specified by no_of_top)
scoring=dict()
for ind in player_data:
    scoring[ind]=sum(player_data[ind][1,:])

sorted_scoring=array(sorted(scoring.iteritems(), key=operator.itemgetter(1)))  ### sorted list of scorers
top_scorers=sorted_scoring[-no_of_top:,0]  #### list of top scorers

top_scoring=0;     #### points per game produced by the top scorers
for x in top_scorers:
    top_scoring=top_scoring+player_data[x][1]  


pts_per_game=events_per_game('Pts') ##### total points per game

scoring_spread=top_scoring/pts_per_game

    
    
