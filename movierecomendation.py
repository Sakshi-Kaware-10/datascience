#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


movies=pd.read_csv(r"C:\Users\aishw\Downloads\ml-25m\ml-25m\movies.csv")


# In[3]:


print(movies)


# In[4]:


movies


# In[5]:


import re

def clean_title(title):
    return re.sub("[^a-zA-Z0-9]","",title)


# In[6]:


movies["clean_title"]=movies["title"].apply(clean_title)


# In[7]:


movies


# In[8]:


from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer=TfidfVectorizer(ngram_range=(1,2))

tfidf=vectorizer.fit_transform(movies["clean_title"])


# In[9]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    
    return results


# In[10]:


import ipywidgets as widgets
from IPython.display import display

movie_input = widgets.Text(
    value='Toy Story',
    description='Movie Title:',
    disabled=False
)
movie_list = widgets.Output()

def on_type(data):
    with movie_list:
        movie_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            display(search(title))

movie_input.observe(on_type, names='value')


display(movie_input, movie_list)


# In[11]:


movie_id = 89745

#def find_similar_movies(movie_id):
movie = movies[movies["movieId"] == movie_id]


# In[12]:


ratings = pd.read_csv(r"C:\Users\aishw\Downloads\ml-25m\ml-25m\ratings.csv")


# In[13]:


ratings.dtypes


# In[14]:


similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()


# In[15]:


similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]


# In[16]:


similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

similar_user_recs = similar_user_recs[similar_user_recs > .10]


# In[17]:


all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]


# In[18]:


all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())


# In[19]:


rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
rec_percentages.columns = ["similar", "all"]


# In[20]:


rec_percentages


# In[21]:


rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]


# In[22]:


rec_percentages = rec_percentages.sort_values("score", ascending=False)


# In[23]:


rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")


# In[24]:


def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]


# In[25]:


import ipywidgets as widgets
from IPython.display import display

movie_name_input = widgets.Text(
    value='Toy Story',
    description='Movie Title:',
    disabled=False
)
recommendation_list = widgets.Output()

def on_type(data):
    with recommendation_list:
        recommendation_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            results = search(title)
            movie_id = results.iloc[0]["movieId"]
            display(find_similar_movies(movie_id))

movie_name_input.observe(on_type, names='value')

display(movie_name_input, recommendation_list)


# In[ ]:





# In[ ]:




