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

        print("*"*35+"User Correlation "+'*'*30) 
        print(corr)
        print('*'*100)

        #Plots
        # plt.title('Song User matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        # plt.title('Correlation for User : '+username)
        # sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        # plt.show()
        
        return corr   


    def songs(self,song_title):
        mat=self.df.pivot_table(index='username',columns='song_title',values='listen_count')
        song=mat[song_title]
        corr=pd.DataFrame(mat.corrwith(song,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation'])

        print("*"*35+"Songs Correlation "+'*'*30) 
        print(corr)
        print('*'*100)      

        #Plots
        # plt.title('User Song matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        plt.title('Correlation for Song : '+song_title)
        sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        plt.show()
        
        return corr   


    def albums(self,album_title):
        mat=self.df.pivot_table(index='username',columns='album_title',values='listen_count', aggfunc='sum')
        album=mat[album_title]
        corr=pd.DataFrame(mat.corrwith(album,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation']) 

        print("*"*35+"Albums Correlation "+'*'*30) 
        print(corr)
        print('*'*100)      

        # # Plots
        # plt.title('User Album matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        # plt.title('Correlation for Album : '+album_title)
        # sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        plt.show()

        return corr    


class Clustering():
    def __init__(self,username):
        albums=pd.read_csv('albums.csv')
        songs=pd.read_csv('songs.csv')
        users=pd.read_csv('users.csv')
        usersongrelationships=pd.read_csv('usersongrelationships.csv')

        df1=pd.merge(songs, albums, on="album_id") 
        df2=pd.merge(df1,usersongrelationships, on="song_id") 
        df=pd.merge(df2, users, on="user_id") 


        self.df=df
        self.username=username  
        self.all_users=self.df['username'].unique() #unique users
        self.all_songs=self.df['song_title'].unique() #unique songs
        self.all_albums=self.df['album_title'].unique() #unique albums
        self.user_songs= self.df[(self.df['listen_count']>0) & (self.df['username']==self.username)]['song_title'].unique()
        self.non_user_songs=self.df[(self.df['listen_count']==0) & (self.df['username']==self.username)]['song_title'].unique()
        self.user_albums= self.df[(self.df['listen_count']>0) & (self.df['username']==self.username)]['album_title'].unique()
        self.non_user_albums= []
        for album in self.all_albums:
            if album  not in self.user_albums:
                self.non_user_albums.append(album)

    def song_year(self,song_title):
        x=str(self.df[self.df['song_title']==song_title]['pub_year'].unique())
        x=x.split('-')[0]
        return int(x[1:-1])

    def album_year(self,album_title):
        x=str(self.df[self.df['album_title']==album_title]['pub_year'].unique())
        x=x.split('-')[0]
        return int(x[1:-1]) 

    def genre(self,song_title):
        x=str(self.df[self.df['song_title']==song_title]['genre'].unique())
        return x[2:-2]  

    #gives simialr songs correspoding to given song using Clustering method
    def similar_song(self,song_title):
        u=self.df[['username','gender','album_title','date_of_birth','song_title','artist','listen_count','is_favorite','is_added_to_playlist']]
        u=u.groupby('song_title').sum()
        x=pd.DataFrame(u.index)
        x.reset_index()
        y=x['song_title'].apply(self.song_year)
        g=x['song_title'].apply(self.genre)
        u['genre']=[g[i] for i in range(0,len(g))]
        u['pub_year']=[y[i] for i in range(0,len(y))]

        # print(u)
        X = u.iloc[:, :].values

        # Encoding categorical data
        from sklearn.preprocessing import LabelEncoder, OneHotEncoder
        labelencoder_X = LabelEncoder()
        X[:, -2] = labelencoder_X.fit_transform(X[:, -2])

        onehotencoder = OneHotEncoder(categorical_features = [-2])
        X = onehotencoder.fit_transform(X).toarray()


        # Feature Scaling
        sc_X = StandardScaler()
        SX = sc_X.fit_transform(X)


        # Fitting K-Means to the dataset
        kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 0)
        y_sc_kmeans = kmeans.fit_predict(SX)

        su=pd.DataFrame(u.index)
        su['cluster']=y_sc_kmeans
        su.set_index('song_title',inplace=True)


        RX=sc_X.inverse_transform(SX)
        su['Bollywood']=RX[:,0:1]
        su['Hip-Hop']=RX[:,1:2]
        su['Punjabi']=RX[:,2:3]
        su['Remix']=RX[:,3:4]
        su['Rock']=RX[:,4:5]
        su['Soundtrack']=RX[:,5:6]
        su['listen_count']=RX[:,6:7]
        su['is_favorite']=RX[:,7:8]
        su['is_added_to_playlist']=RX[:,8:9]
        su['genre']=[g[i] for i in range(0,len(g))]
        su['pub_year']=RX[:,-1]
        su['cluster']=y_sc_kmeans
        # su.set_index('song_title',inplace=True)   
        print(su)
        sns.jointplot(x='listen_count',y='cluster',kind='scatter',data=su)        
        plt.show()
        similar_songs=pd.DataFrame(su[su['cluster']==su[su.index==song_title]['cluster'][0]].index)
        similar_songs.set_index(np.arange( 1, len(similar_songs)+1 ),inplace=True)

        #removing items which are already listened by user
        for s in self.user_songs:
          try:
              similar_songs.drop(similar_songs[similar_songs['song_title']==s].index[0],axis=0,inplace=True)

          except:
              pass

        #removing the current song from similar item
        try:
            similar_songs.drop(similar_songs[similar_songs['song_title']==song_title].index[0],axis=0,inplace=True) 
        except:
            pass


        similar_songs.set_index(np.arange( 1, len(similar_songs)+1 ),inplace=True)  

        print("*"*35+" Similar Songs Based on Clustering"+'*'*30)
        print('Cluster  : '+str(su[su.index==song_title]['cluster'][0]))
        print(similar_songs)
        print('*'*100)  
        return similar_songs

    #gives simialr songs correspoding to given song using Clustering method
    def similar_album(self,album_title):
        u=self.df[['username','gender','album_title','date_of_birth','song_title','artist','listen_count','is_favorite','is_added_to_playlist']]
        u=u.groupby('album_title').sum()
        x=pd.DataFrame(u.index)
        x.reset_index()
        y=x['album_title'].apply(self.album_year)
        u['pub_year']=[y[i] for i in range(0,len(y))]
        X = u.iloc[:, :].values


        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc_X = StandardScaler()
        SX = sc_X.fit_transform(X)


        # Fitting K-Means to the dataset
        kmeans = KMeans(n_clusters = 3, init = 'k-means++', random_state = 0)
        y_kmeans = kmeans.fit_predict(SX)
        u['cluster']=y_kmeans

        similar_albums=pd.DataFrame(u[u['cluster']==u[u.index==album_title]['cluster'][0]].index)
        similar_albums.set_index(np.arange( 1, len(similar_albums)+1 ),inplace=True)

        #removing items which are already listened by user
        for s in self.user_albums:
          try:
            similar_albums.drop(similar_albums[similar_albums['album_title']==s].index[0],axis=0,inplace=True) 
          except:
              pass
        #removing the current album from similar item 
        try:
            similar_albums.drop(similar_albums[similar_albums['album_title']==album_title].index[0],axis=0,inplace=True)        
        except:
            pass    


        similar_albums.set_index(np.arange( 1, len(similar_albums)+1),inplace=True) 
        print("*"*35+" Similar Albums Based on Clustering "+'*'*30)
        print('Cluster  : '+str(u[u.index==album_title]['cluster'][0]))     
        print(similar_albums)
        print('*'*100)      
        return similar_albums   



















# help(pd.DataFrame.pivot_table)
c=Clustering('vishal')
c.similar_song('Game of Thrones')
