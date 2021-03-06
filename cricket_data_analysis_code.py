# -*- coding: utf-8 -*-
"""Cricket Data Analysis Code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RGqkcyda4vZHq9IiYJqDc-jqa-LiBHCv
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
# %matplotlib inline
import random

from sklearn import metrics
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

custom_colors = ["#023e8a", "#0096c7","#90e0ef","#ff5400","#ffbd00"]
customPalette = sns.set_palette(sns.color_palette(custom_colors))

players = pd.read_csv(r'Batsmen.csv', )
players.drop(players[players['Runs'] == '-'].index, inplace=True)
players.drop(players[players['Ave'] == '-'].index, inplace=True)
players.drop_duplicates(subset=['Player'], inplace=True)
players['Mat'] = players['Mat'].astype(int)
players['Inns'] = players['Inns'].astype(int)
players['NO'] = players['NO'].astype(int)
players['Runs'] = players['Runs'].astype(int)
players['BF'] = players['BF'].astype(int)
players['4s'] = players['4s'].astype(int)
players['6s'] = players['6s'].astype(int)

players.drop(players[players['Runs'] < 50].index, inplace=True)

players

batsmen = pd.DataFrame({"Player_Id": players["Player ID"]})

batsmen["Innings"] = players["Inns"]
batsmen["Runs"] = players["Runs"]
batsmen["Balls_played"] = players["BF"]
batsmen["4s and 6s"] = players["4s"] + players["6s"]
batsmen["Average"] = (players["Runs"] / (players["Inns"] - players["NO"])).round(2)
batsmen['Hitting Ability'] = batsmen["4s and 6s"] / players["BF"]


batsmen["Strike_Rate"] = (batsmen["Runs"] * 100 / batsmen["Balls_played"]).round(2)

print(batsmen)

def triple_plot(x, title,c):
    fig, ax = plt.subplots(3,1,figsize=(20,12),sharex=True)
    sns.distplot(x, ax=ax[0],color=c)
    ax[0].set(xlabel=None)
    ax[0].set_title('Histogram + KDE')
    sns.boxplot(x, ax=ax[1],color=c)
    ax[1].set(xlabel=None)
    ax[1].set_title('Boxplot')
    sns.violinplot(x, ax=ax[2],color=c)
    ax[2].set(xlabel=None)
    ax[2].set_title('Violin plot')
    fig.suptitle(title, fontsize=25)
    plt.tight_layout(pad=3.0)
    plt.show()

triple_plot(batsmen["Strike_Rate"],'Distribution of Strike Rate',custom_colors[0])

batsmen = batsmen[batsmen["Strike_Rate"] > 110]
triple_plot(batsmen["Strike_Rate"],'Distribution of Strike Rate',custom_colors[1])

def scatter_plot(data,title,c,col1,col2):
    fig = plt.figure(figsize=(12,6))
    sns.scatterplot(x=col1, y=col2, data=data,color=c)
    plt.title(title)
    plt.show()

def elbow_method(X):
    distortions = [] 
    inertias = [] 
    mapping1 = {} 
    mapping2 = {} 
    K = range(2,10) 

    for k in K:  
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)     

        distortions.append(sum(np.min(cdist(X, kmeans.cluster_centers_, 
                          'euclidean'),axis=1)) / X.shape[0]) 
        inertias.append(kmeans.inertia_) 

        mapping1[k] = sum(np.min(cdist(X, kmeans.cluster_centers_, 
                     'euclidean'),axis=1)) / X.shape[0] 
        mapping2[k] = kmeans.inertia_ 

    print("Distortion")
    for key,val in mapping1.items(): 
        print(str(key)+' : '+str(val)) 

    print("Inertia")
    for key,val in mapping2.items(): 
        print(str(key)+' : '+str(val)) 

    plt.plot(K, distortions, 'bx-',color=custom_colors[random.randint(0,5)]) 
    plt.xlabel('Values of K') 
    plt.ylabel('Distortion') 
    plt.xticks(K)
    plt.title('Elbow Method') 
    plt.show()

elbow_method(batsmen[["Average" , "Strike_Rate"]])

elbow_method(batsmen[["Average", "Hitting Ability"]])

elbow_method(batsmen[["Strike_Rate", "Hitting Ability"]])

def scores(X):
    K = range(3,8) 

    for k in K:  
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X) 
        y_hat = kmeans.predict(X)
        labels = kmeans.labels_
        
        a = metrics.silhouette_score(X, labels, metric = 'euclidean')
        b = metrics.calinski_harabasz_score(X, labels)
        
        print("k={0}, Silhouette score={1}, Calinski harabasz score={2}".format(k,a, b))

kmeans = KMeans(n_clusters=5)
kmeans.fit(batsmen[["Average" , "Strike_Rate"]])
batsmen["cluster1"] = kmeans.labels_

fig = plt.figure(figsize=(12,6))

colors = custom_colors

plt.scatter(batsmen["Average"], batsmen["Strike_Rate"], c=batsmen["cluster1"],  cmap='rainbow')
    
plt.title("IPL Batsmen")
plt.xlabel("Average of the Batsmen")
plt.ylabel("Strike Rate of the Batsmen")
plt.show()

kmeans = KMeans(n_clusters=5)
kmeans.fit(batsmen[["Average", "Hitting Ability"]])
batsmen["cluster2"] = kmeans.labels_

fig = plt.figure(figsize=(12,6))

colors = custom_colors


plt.scatter(batsmen["Average"], batsmen["Hitting Ability"], c=batsmen["cluster2"], cmap='rainbow')
    
plt.title("IPL Batsmen")
plt.xlabel("Average of the Batsmen")
plt.ylabel("Hitting Abilty of the Batsmen")
plt.show()

kmeans = KMeans(n_clusters=5)
kmeans.fit(batsmen[["Strike_Rate", "Hitting Ability"]])
batsmen["cluster3"] = kmeans.labels_

fig = plt.figure(figsize=(12,6))

colors = custom_colors

plt.scatter(batsmen["Strike_Rate"], batsmen["Hitting Ability"], c=batsmen["cluster3"],  cmap='rainbow')
    
plt.title("IPL Batsmen")
plt.xlabel("Strike Rate of the Batsmen")
plt.ylabel("Hitting Abilty of the Batsmen")
plt.show()

from sklearn.cluster import AgglomerativeClustering

clustering = AgglomerativeClustering(n_clusters=10,affinity='euclidean',linkage='complete').fit(batsmen[["Hitting Ability", "Innings"]])
plt.scatter(batsmen["Hitting Ability"],batsmen["Innings"], c=clustering.labels_, cmap='rainbow')

from mpl_toolkits.mplot3d import Axes3D
from google.colab import widgets

kmeans = KMeans(n_clusters=5)
kmeans.fit_predict(batsmen[["Average", "Hitting Ability", "Strike_Rate"]])
batsmen["cluster4"] = kmeans.labels_

fig = plt.figure(figsize=(26,6))
ax = fig.add_subplot(131, projection='3d')
ax.scatter( batsmen["Average"], batsmen["Hitting Ability"], batsmen["Strike_Rate"], c=batsmen["cluster4"], s=15)
ax.set_xlabel('Hitting Ability')
ax.set_ylabel('Average')
ax.set_zlabel('Strike_Rate')
plt.show()

!pip install chart_studio
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots
import plotly.offline as py

Scene = dict(xaxis = dict(title  = 'Hitting Ability'),yaxis = dict(title  = 'Average'),zaxis = dict(title  = 'Strike_Rate'))
labels = batsmen["cluster4"]
trace = go.Scatter3d(x = batsmen["Average"], y = batsmen["Hitting Ability"], z = batsmen["Strike_Rate"], mode='markers',marker=dict(color = labels, size= 10, line=dict(color= 'black',width = 10)))
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)
fig.show()