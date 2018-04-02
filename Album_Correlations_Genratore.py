import numpy as np
import pandas as pd
import csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler    
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import figure
import time






class  Correlation ():
    def __init__(self):
        albums=pd.read_csv('albums.csv')
        songs=pd.read_csv('songs.csv')
        users=pd.read_csv('users.csv')
        usersongrelationships=pd.read_csv('usersongrelationships.csv')

        df1=pd.merge(songs, albums, on="album_id") 
        df2=pd.merge(df1,usersongrelationships, on="song_id") 
        df=pd.merge(df2, users, on="user_id") 
        self.df=df


    def users(self,username):
        mat=self.df.pivot_table(index='song_title',columns='username',values='listen_count')
        user=mat[username]
        corr=pd.DataFrame(mat.corrwith(user,drop=True),columns=['Correlation'])       
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation'])


        # print("*"*35+username+'*'*30) 
        # print(corr)
        # print('*'*100)   

        plt.figure(figsize=(5, 6))
        plt.title('Correlation for User : ' + str(  username))
        sns.heatmap(corr, cmap='coolwarm', linecolor='white', annot=True)
        plt.savefig('static/analysis/users/' + str(username) + '.png')
        plt.tight_layout()
        plt.close()
    



    def songs(self,song_title):
        mat=self.df.pivot_table(index='username',columns='song_title',values='listen_count')
        song=mat[song_title]
        corr=pd.DataFrame(mat.corrwith(song,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation'])

        # print("*"*35+song_title+'*'*30) 
        # print(corr)
        # print('*'*100)      

        plt.subplots_adjust(left=.4)
        plt.figure(figsize=(20,15))
        plt.tight_layout()
        plt.title('Correlation for Song : '+str(song_title))
        sns.heatmap(corr,cmap='coolwarm',linecolor='white')
        plt.savefig('static/analysis/songs/' + str(song_title) + '.png')
        plt.close()

    def albums(self,album_title):
        mat=self.df.pivot_table(index='username',columns='album_title',values='listen_count', aggfunc='sum')
        album=mat[album_title]
        corr=pd.DataFrame(mat.corrwith(album,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation']) 


        # print("*"*35+album_title+'*'*30) 
        # print(corr)
        # print('*'*100)   

        plt.subplots_adjust(left=.4)
        plt.tight_layout()
        plt.title('Correlation for Album : '+str(album_title))
        sns.heatmap(corr,cmap='coolwarm',linecolor='white')
        plt.savefig('static/analysis/albums/' + str(album_title) + '.png')
        plt.close()

albums=pd.read_csv('albums.csv')
songs=pd.read_csv('songs.csv')
users=pd.read_csv('users.csv')
usersongrelationships=pd.read_csv('usersongrelationships.csv')

df1=pd.merge(songs, albums, on="album_id") 
df2=pd.merge(df1,usersongrelationships, on="song_id") 
df=pd.merge(df2, users, on="user_id") 

all_users=df['username'].unique() #unique users
all_songs=df['song_title'].unique() #unique songs
all_albums=df['album_title'].unique() #unique albums

print('Saving Album Correlation'+'.'*10)
for album in all_albums:
    c=Correlation()
    c.albums(album)
print('Savied Successfull'+'!'*10)





