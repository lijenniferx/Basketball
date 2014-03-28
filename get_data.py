##########################################
#### Building the useful data structures from the basketball html files, and pickles them
####  player_data: dictionary of player stats per game. Keys are the names of the players
####  opponent_data: array of aggregate opponent stats per game. 
####  win_loss: list of 1s and 0s indicating sequence of wins (1) and losses (0)
####  home_away: list of 1s and 0s indicating sequence of home (1) and away (0) games
####  
#########################################
from bs4 import BeautifulSoup
import re
from numpy import *
import glob
import operator

###########################
### some tweakable parameters
no_of_top=2  ### number of top players to calculate "spread of scoring"
stat_categories=['Reb','Pts','A','Stl']


################################
#### getting the game outcomes, home/away info, player names
################################

html=open('basketball.html','r')
soup=BeautifulSoup(html.read(),'lxml')

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

### getting list of player names
players=[x.text for x in soup.body.find_all('a',{'href':re.compile('player/d*')})][4:]  

################################
#### some housekeeping: getting the list of html files for each game, and indices for the stat categories of interest
##################################

cat_soup=BeautifulSoup(open(glob.glob('./*.html')[0],'r').read(),'lxml')
categories=[x.text for x in cat_soup.body.find_all('th',{'style':lambda x: x and x.startswith('background')})][:16]
stats_index=[]
for x in stat_categories:
    if x in categories:
        stats_index.append(categories.index(x)+3)
    else:
        raise Exception('You did not enter an acceptable stat category') 


################################
##### filling in player stats and opponent stats for each game
#######################

### preallocating the arrays for player data
no_of_games=len(glob.glob('./[0-9]*.html'))
player_data=dict()
for ind in players:
    player_data[ind]=zeros((len(stat_categories),no_of_games))  ### rebounds, points, minutes played

#### preallocating the array for opponent data
opponent_data=zeros((no_of_games,len(stat_categories)))

##### preallocating the array for officials
officials=[['','',''] for x in range(no_of_games)]

### going through each html file, finding the player data for each game, as well as the aggregate data for the opponents
game_index=0

for files in glob.glob('./[0-9]*.html'):
    if len(files)==12:
        html=open(files,'r')
        soup_game=BeautifulSoup(html.read(),'lxml')
#        soup_game.find(text=re.compile('Officials'))   #### planned code for collecting officials
#
#        officials=
        which_team=0  ### default is to get the second set of aggregate data
        if soup_game.findAll('tr')[-1].td.text=='West Virginia':
            which_team=1  #### get the first set of aggregate data
       
        '''player data'''
        for possibilities in soup_game.findAll('tr'):
            if possibilities.a:  ### our player
                temp_stats=[x.text for x in possibilities.find_all('td')]
                player_data[temp_stats[1]][:,game_index]=[temp_stats[x] for x in stats_index]
            elif possibilities.td:
                if possibilities.find_all('td',limit=2)[1].text=='Totals':
                    if which_team==1:                        
                        temp_stats=[x.text for x in possibilities.find_all('td')]
                        opponent_data[game_index,:]=[temp_stats[x] for x in stats_index]
                        which_team=0                                  
                    elif which_team==0:
                        which_team=1
        
        game_index+=1    

####################
### saving files
##################

import pickle
with open('basketball.pik','wb') as f:
        pickle.dump(player_data,f,-1)
        pickle.dump(opponent_data,f,-1)
        pickle.dump(win_loss,f,-1)
        pickle.dump(home_away,f,-1)
        
f.close()


