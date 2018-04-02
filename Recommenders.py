import numpy as np
import pandas as pd
import csv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler    
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import time
localtime = time.localtime(time.time())


#Class for Popularity based Recommender System model
class Popularity():
    def __init__(self):
        albums=pd.read_csv('albums.csv')
        songs=pd.read_csv('songs.csv')
        users=pd.read_csv('users.csv')
        usersongrelationships=pd.read_csv('usersongrelationships.csv')

        df1=pd.merge(songs, albums, on="album_id") 
        df2=pd.merge(df1,usersongrelationships, on="song_id") 
        df=pd.merge(df2, users, on="user_id") 
        self.df=df

    def song_age(self,song_title):
        x=str(self.df[self.df['song_title']==song_title]['pub_year'].unique())
        x=x.split('-')[0]
        time=localtime[0]-int(x[1:-1])
        if time==0:
            return 0.5
        else:   
            return time 

    def album_age(self,album_title):
        x=str(self.df[self.df['album_title']==album_title]['pub_year'].unique())
        x=x.split('-')[0]
        time=localtime[0]-int(x[1:-1])
        if time==0:
            return 0.5
        else:   
            return time 


    #Showing the most popular songs in the dataset  
    def recommend_song(self):
        unique_users_weight=1
        non_unique_users_weight=.25

        #df contains songs with atleat one listen_count
        df=self.df[self.df['listen_count']>0]
        grouped_data = self.df.groupby(['song_title']).sum()
        songs=grouped_data.index

        ###############################
        #Listen Count history is Empty
        ###############################
        if not len(df):
            print("*"*35+"Popular Songs"+'*'*50)
            print('\tListen Count history is Empty')
            print('\tDisplying random songs as popular songs')
            print("*"*100)
            return self.df
        
        # unique users for the given songs list
        u=[]
        for i in songs:
            u.append(df[df['song_title']==i]['username'].nunique())

        recommendations=grouped_data    
        recommendations['unique_users']=u

        x=pd.DataFrame(recommendations.index)
        x.reset_index()
        y=x['song_title'].apply(self.song_age)
        recommendations['song_age']=[y[i] for i in range(0,len(y))]


        recommendations['score']=((recommendations['listen_count']-(recommendations['unique_users']))*non_unique_users_weight+recommendations['unique_users']*unique_users_weight)/recommendations['song_age']

        #sort the recommendations based upon score
        recommendations=recommendations.sort_values(by='score')[::-1]
        
        #removing Nan which may occures if unique users for song is 0
        recommendations=recommendations.dropna()
        recommendations=recommendations[['listen_count','unique_users','song_age','score']]
        recommendations.reset_index(inplace=True)
        recommendations.index.name='Rank'
        #removing the items whoes corelation is less than 0  
        recommendations=recommendations[recommendations['score']>0]


        print("*"*35+"Popular Songs"+'*'*50)
        print('Scoring Formula  : \n ([non_unique_user_listen_count X non_unique_users_weight]+[unique_user_listen_count X unique_users_weight])/song_age')
        print('unique_users_weight : '+str(unique_users_weight)+'     non_unique_users_weight : '+str(non_unique_users_weight))
        print()
        print(recommendations)
        print("*"*100)
        return recommendations

    #Showing the most popular albums in the dataset 
    def recommend_album(self):
        unique_users_weight=1   
        non_unique_users_weight=.25

        #df contains albums with atleat one listen_count
        df=self.df[self.df['listen_count']>0]
        grouped_data = self.df.groupby(['album_title']).sum()
        albums=grouped_data.index
        
        ###############################
        #Listen Count history is Empty
        ###############################
        if not len(df):
            print("*"*35+"Popular Albums"+'*'*50)
            print('\tListen Count history is Empty')
            print('\tDisplying random albums as popular albums')
            print("*"*100)
            #returning random unique albums
            df=pd.DataFrame(self.df['album_title'].unique() )
            df.columns=['album_title']
            return df


        # unique songs for the given album
        s=[]
        for i in albums:
            s.append(df[df['album_title']==i]['song_title'].nunique())

        # unique users for the given songs list
        u=[]
        for i in albums:
            u.append(df[df['album_title']==i]['username'].nunique())

            
        recommendations =grouped_data   
        recommendations['no_of_songs']=s
        recommendations['unique_users']=u

        x=pd.DataFrame(recommendations.index)
        x.reset_index()
        y=x['album_title'].apply(self.album_age)
        recommendations['album_age']=[y[i] for i in range(0,len(y))]


        recommendations['score']=((recommendations['listen_count']-recommendations['unique_users'])*non_unique_users_weight+recommendations['unique_users']*unique_users_weight)/(recommendations['no_of_songs']*recommendations['album_age'])
        
        #sort the recommendations based upon score
        recommendations=recommendations.sort_values(by='score')[::-1]
        
        #removing Nan which may occures if unique users for song is 0
        recommendations=recommendations.dropna()
        recommendations=recommendations[['listen_count','no_of_songs','unique_users','album_age','score']]
        recommendations.reset_index(inplace=True)
        recommendations.index.name='Rank'
        #removing the items whoes corelation is less than 0  
        recommendations=recommendations[recommendations['score']>0]

        print("*"*35+"Popular Albums"+'*'*50)
        print('Scoring Formula: \n ([non_unique_user_listen_count X non_unique_users_weight]+[unique_user_listen_count X unique_users_weight])/(no_of_songs_per_album X album_age)')
        print('unique_users_weight : '+str(unique_users_weight)+'     non_unique_users_weight : '+str(non_unique_users_weight))
        print()
        print(recommendations)
        print("*"*100)
        return recommendations


class  Collaborative_Filtering (object):
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


        # print(self.user_albums[:])
        # print(self.non_user_albums[:])
        
    #returning the (no. of user listen both song i and j)/(no. of user listen either song i or j)
    def songs_commmon_listen_count(self,i,j):
        c=0
        d=0
        for u in self.all_users:
            if (u !=self.username ):
                a=np.array(self.df[(self.df['listen_count']>0) & (self.df['username']==u)]['song_title'])
                if i in a and j in a:
                    c=c+1
                if i in a or j in a:
                    d=d+1
                    # d=0
        # for normalization     
        if d:
            return c/d      
        else:
            return c

    def construct_song_cooccurence_matrix(self):
        ###############################################
        #Construct cooccurence matrix dataframe of size
        #len(user_songs) X len(non_user_songs)
        ############################################### 
        self.song_cooccurence_matrix=pd.DataFrame(np.matrix(np.zeros(shape=(len(self.user_songs), len(self.non_user_songs))), float) ,self.user_songs,self.non_user_songs)
        
        # for s in self.non_user_songs:
        #   self.song_cooccurence_matrix.drop(s,axis=0,inplace=True)

        for i in self.user_songs:
            for j in self.non_user_songs:               
                self.song_cooccurence_matrix.loc[i,j]=self.songs_commmon_listen_count(i,j)
                
        self.song_cooccurence_matrix.dropna(inplace=True)
        

        # print(self.song_cooccurence_matrix)
        recommendations=pd.DataFrame(self.song_cooccurence_matrix.sum().sort_values()[::-1])
        
        self.s_song_cooccurence_matrix=pd.DataFrame(self.song_cooccurence_matrix.sum())
        self.s_song_cooccurence_matrix.columns=['Summation']
        


        # #removing items which are already listened by user
        # for s in self.user_songs:
        #     try:
        #         recommendations.drop(s,axis=0,inplace=True)
        #     except:
        #         pass   
        #removing the items whoes corelation is less than 0  
        recommendations=recommendations[recommendations[0]>0]
        self.n_song_cooccurence_matrix=recommendations
        self.n_song_cooccurence_matrix.columns=['Summation'] 

        recommendations=recommendations.reset_index()
        recommendations.index.name='Rank'
        recommendations.columns=['song_title','score']  
 

        self.song_recommendations=recommendations 


    #Recommends songs to login user 
    def recommend_song(self):
        ###############################
        #User history is not present 
        ###############################
        if len(self.user_songs)==0:
            temp=pd.DataFrame(self.df['song_title'].unique())
            temp.columns=['song_title']
            self.song_recommendations =temp
            print("*"*35+" Collaborative Filtering Recommended Songs "+'*'*40)
            print('\tUser history is not present ')
            print('\tCollaborative Filtering not possible ')
            print('\tRecommending random songs ')           
            print('*'*100)
            return self.song_recommendations

        self.construct_song_cooccurence_matrix()
        if  len(self.song_recommendations)!=0:  
            # print(self.song_cooccurence_matrix)
            print("*"*35+" Collaborative Filtering Recommended Songs "+'*'*50)
            print(self.song_recommendations)
            print('*'*100)
            return self.song_recommendations
        
        #Collaborative Filtering Fails because songs by listened user is not listened by any of other users
        #so we use clusternig on the songs listened by user
        else:
            #selecting the song which is listened by user maximum times
            i=0
            max=0
            for s in self.user_songs:
                c=int(self.df[(self.df['song_title']==s) & (self.df['username']==self.username)]['listen_count'].values)
                if(max<c):
                    max=c
                    index=i 
                i+=1    
            # creating Clustering object
            print("*"*15+" Collaborative Filtering Fails because songs by listened user is not listened by any of other users"+'*'*20)
            print("*"*15+" Clusternig is apllied on the song listened by user maximum no of times "+'*'*30)            
            cl_obj = Clustering(self.username)
            cl=cl_obj.similar_song(self.user_songs[index])
            return cl



    #returning (the no. of user listen both album i and j)/(no. of user listen either album i or j)
    def albums_commmon_listen_count(self,i,j):
        c=0
        d=0
        for u in self.all_users:
            if (u !=self.username ) :
                a=np.array(self.df[(self.df['listen_count']>0) & (self.df['username']==u)]['album_title'].unique())
                # print(a)
                if i in a and j in a:
                    c=c+1
                if i in a or j in a:
                    d=d+1
                    # d=0
        # for normalization     
        if d:
            return c/d      
        else:
            return c


    def construct_album_cooccurence_matrix(self):
        ###############################################
        #Construct cooccurence matrix dataframe of size
        #len(user_albums) X len(non_user_albums)
        ############################################### 
        self.album_cooccurence_matrix=pd.DataFrame(np.matrix(np.zeros(shape=(len(self.user_albums), len(self.non_user_albums))), float) ,self.user_albums,self.non_user_albums)



        for i in self.user_albums:
            for j in self.non_user_albums:              
                self.album_cooccurence_matrix.loc[i,j]=self.albums_commmon_listen_count(i,j)
                
        self.album_cooccurence_matrix.dropna(inplace=True)
        # print(self.album_cooccurence_matrix)

        recommendations=pd.DataFrame(self.album_cooccurence_matrix.sum().sort_values()[::-1])

        self.s_album_cooccurence_matrix=pd.DataFrame(self.album_cooccurence_matrix.sum())
        self.s_album_cooccurence_matrix.columns=['Summation'] 
        
        # #removing items which are already listened by user
        # for s in self.user_albums:
        #     try:
        #         recommendations.drop(s,axis=0,inplace=True)
        #     except:
        #         pass    
        #removing the items whoes corelation is less than 0  
        recommendations=recommendations[recommendations[0]>0]
        self.n_album_cooccurence_matrix=recommendations
        self.n_album_cooccurence_matrix.columns=['Summation'] 
        
        recommendations=recommendations.reset_index()
        recommendations.index.name='Rank'
        recommendations.columns=['album_title','score'] 
        #removing the items whoes corelation is less than 0  	
        self.album_recommendations=recommendations









    #Recommends albums to login user
    def recommend_album(self):
        if len(self.user_albums)==0:
            print("*"*35+" Collaborative Filtering Recommended Albums "+'*'*40)
            print('\tUser history is not present ')
            print('\tCollaborative Filtering not possible ')
            print('\tRecommending random albums ')  
            print('*'*100)
            temp=pd.DataFrame(self.df['album_title'].unique())
            temp.columns=['album_title']
            self.album_recommendations =temp
            return self.album_recommendations
        self.construct_album_cooccurence_matrix()
        if len(self.album_recommendations)!=0 :               
            # print(self.album_cooccurence_matrix)
            print("*"*35+" Collaborative Filtering Recommended Albums "+'*'*50)
            print(self.album_recommendations)
            print('*'*100)
            return self.album_recommendations
        
        #Collaborative Filtering Fails because albums by listened user is not listened by any of other users
        #so we use clusternig on the albums listened by user
        else:
            #selecting the album which is listened by user maximum times
            i=0
            max=0
            for s in self.user_albums:
                c=int(self.df[(self.df['album_title']==s) & (self.df['username']==self.username)]['listen_count'].values)
                if(max<c):
                    max=c
                    index=i 
                i+=1    
            # creating Clustering object
            print("*"*15+" Collaborative Filtering Fails because albums by listened user is not listened by any of other users"+'*'*20)
            print("*"*15+" Clusternig is apllied on the album listened by user maximum no of times "+'*'*30)            
            cl_obj = Clustering(self.username)
            cl=cl_obj.similar_album(self.user_albums[index])
            return cl       


        
    #gives simmialr songs correspoding to givrn song using  cooccurence_matrix(Collaborative Filtering) method
    def similar_song(self,song_title):
        ###############################################
        #Construct cooccurence matrix dataframe of size
        #1 X len(non_user_songs)
        ###############################################
        song=self.df[(self.df['listen_count']>0) & (self.df['song_title']==song_title)]
        song=song['song_title'].unique()

        self.similar_song_cooccurence_matrix=pd.DataFrame(np.array(np.zeros(shape=(len(song), len(self.non_user_songs))), float) ,song,self.non_user_songs)
        

        for j in self.non_user_songs:               
            self.similar_song_cooccurence_matrix.loc[song_title,j]=self.songs_commmon_listen_count(song_title,j)
                
        self.similar_song_cooccurence_matrix.dropna(inplace=True)

        # print(similar_song_cooccurence_matrix)

  
        similar_songs=pd.DataFrame(self.similar_song_cooccurence_matrix.sum().sort_values()[::-1])

        
        # #removing items which are already listened by user
        # for s in self.user_songs:
        #     try:
        #         similar_songs.drop(s,axis=0,inplace=True)
        #     except:
        #         pass

        #removing the current song from similar item  (it may be present if user not listen that song  already)
        try:
            similar_songs.drop(song_title,axis=0,inplace=True)      
        except:
            pass        
                
        similar_songs.columns=[song_title] 

        #removing the items whoes corelation is less than 0           
        similar_songs=similar_songs[similar_songs[song_title]>0]        
        self.n_similar_song_cooccurence_matrix=similar_songs

        similar_songs=similar_songs.reset_index()
        similar_songs.index.name='Rank'
        similar_songs.columns=['song_title','score']     

        # print(self.song_cooccurence_matrix)
        print("*"*35+" Similar Songs Based on Collaborative Filtering"+'*'*20)
        print(similar_songs)
        print('*'*100)  
        return similar_songs



    #gives simmialer albums correspoding to given album using  cooccurence_matrix(Collaborative Filtering) method
    def similar_album(self,album_title):
        ###############################################
        #Construct cooccurence matrix dataframe of size
        #1 X len(non_user_albums)
        ###############################################
        album=self.df[(self.df['listen_count']>0) & (self.df['album_title']==album_title)]
        album=album['album_title'].unique()


        self.similar_album_cooccurence_matrix=pd.DataFrame(np.array(np.zeros(shape=(len(album), len(self.non_user_albums))), float) ,album,self.non_user_albums)
        

        for j in self.non_user_albums:              
            self.similar_album_cooccurence_matrix.loc[album_title,j]=self.albums_commmon_listen_count(album_title,j)
                
        self.similar_album_cooccurence_matrix.dropna(inplace=True)

        # print(similar_album_cooccurence_matrix)

        similar_albums=pd.DataFrame(self.similar_album_cooccurence_matrix.sum().sort_values()[::-1])

        
        # #removing items which are already listened by user
        # for s in self.user_albums:
        #     try:
        #         similar_albums.drop(s,axis=0,inplace=True)
        #     except:
        #         pass

        #removing the current album from simmilar item  (it may be present if user  not listen that album  already)
        try:
            similar_albums.drop(album_title,axis=0,inplace=True)        
        except:
            pass 

        similar_albums.columns=[album_title] 

        #removing the items whoes corelation is less than 0           
        similar_albums=similar_albums[similar_albums[album_title]>0] 

        self.n_similar_album_cooccurence_matrix=similar_albums
        similar_albums=similar_albums.reset_index()
        similar_albums.index.name='Rank'
        similar_albums.columns=['album_title','score'] 


        print("*"*35+" Similar Albums Based on Collaborative Filtering"+'*'*20)
        print(similar_albums)
        print('*'*100)  
        return similar_albums



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
        u=self.df[['song_title','listen_count','is_favorite','is_added_to_playlist']]
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
        kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 0)
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


class  Correlation ():
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


    def users(self):
        mat=self.df.pivot_table(index='song_title',columns='username',values='listen_count')
        user=mat[self.username]
        corr=pd.DataFrame(mat.corrwith(user,drop=True),columns=['Correlation'])       
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation'])

        print("*"*35+"User Correlation "+'*'*30) 
        print(corr)
        print('*'*100)

        #Plots
        # plt.title('Song User matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        # plt.title('Correlation for User : '+self.username)
        # sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        # plt.savefig('static/Analysis/'+self.username+'.png')
        # plt.show()
            
        return corr   


    def songs(self,song_title):
        mat=self.df.pivot_table(index='username',columns='song_title',values='listen_count')
        song=mat[song_title]
        corr=pd.DataFrame(mat.corrwith(song,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation'])

        # #removing items which are already listened by user
        for s in self.user_songs:
            try:
                corr.drop(s,axis=0,inplace=True)
            except:
                pass                 


        #removing the current song from similar item 
        try:
            corr.drop(song_title,axis=0,inplace=True)        
        except:
            pass  

        #removing the items whoes corelation is less than 0    
        corr=corr[corr['Correlation']>0]

        print("*"*35+"Songs Correlation "+'*'*30) 
        print(corr)
        print('*'*100)

        #Plots
        # plt.title('User Song matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        # plt.subplots_adjust(left=.3)
        # plt.title('Correlation for Song : '+song_title)
        # sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        # plt.savefig('stat.png')
        # plt.show()
        
        return corr   


    def albums(self,album_title):
        mat=self.df.pivot_table(index='username',columns='album_title',values='listen_count', aggfunc='sum')
        album=mat[album_title]
        corr=pd.DataFrame(mat.corrwith(album,drop=True),columns=['Correlation'])     
        corr.fillna(0,inplace=True)  
        corr=pd.DataFrame(corr['Correlation'].sort_values()[::-1],columns=['Correlation']) 

        # #removing items which are already listened by user
        for a in self.user_albums:
            try:
                corr.drop(a,axis=0,inplace=True)
            except:
                pass                 


        #removing the current song from similar item 
        try:
            corr.drop(album_title,axis=0,inplace=True)        
        except:
            pass

        #removing the items whoes corelation is less than 0 
        corr=corr[corr['Correlation']>0]

        print("*"*35+"Albums Correlation "+'*'*30) 
        print(corr)
        print('*'*100)      

        # # Plots
        # plt.title('User Album matrix')        
        # sns.heatmap(mat,cmap='coolwarm',linecolor='white',linewidth=1,annot=True) 
        # plt.title('Correlation for Album : '+album_title)
        # sns.heatmap(corr,cmap='coolwarm',linecolor='white',annot=True)
        # plt.show()

        return corr    






# p=Popularity()
# p.recommend_song()

# p.recommend_album()



# c=Collaborative_Filtering('vivek')
# c.similar_song('Set Fire To The Rain')
# c.similar_album('Recovery')
# c.recommend_song()
# c.recommend_album()

# c=Correlation('vishal')
# c.users()
# c.songs('Ae Dil Hai Mushkil')
# c.albums('Recovery')