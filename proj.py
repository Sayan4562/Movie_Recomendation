import streamlit as st
import pickle
import pandas as pd 
import requests

st.set_page_config(page_title="Recommender System ", page_icon="images.jpeg")
def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=4ef57d55653f9485b70cfa0da35b2b33&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']
#### many link are not working ######
# def fetch_video(movie_id):
#     response=requests.get("https://api.themoviedb.org/3/movie/{}/videos?api_key=4ef57d55653f9485b70cfa0da35b2b33&language=en-US".format(movie_id))
#     data = response.json()
#     return data.get('homepage')
def recommend(movie):
    movie_index=moives[moives["title"]==movie].index[0]
    distences=similarity[movie_index]
    movies_list=sorted(list(enumerate(distences)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies=[]
    recommend_movies_posters=[]
    recommend_movies_overview=[]
    recommend_movies_director=[]
    recommend_movies_actors=[]
    for i in movies_list:
        recommend_movies.append(moives.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(moives.iloc[i[0]].movie_id))
        recommend_movies_overview.append(moives.iloc[i[0]].overview)
        recommend_movies_director.append(moives.iloc[i[0]].crew)
        recommend_movies_actors.append(moives.iloc[i[0]].cast)
    return recommend_movies,recommend_movies_posters,recommend_movies_overview,recommend_movies_director,recommend_movies_actors
moive_dict= pickle.load(open("movie_dict.pkl","rb"))
moives=pd.DataFrame(moive_dict)
similarity=pickle.load(open("similarity.pkl","rb"))
st.title("Movie recomender system")
st.write("")
st.subheader("How would like to")
selected_movie_name=st.selectbox(
    label="",
    options=moives["title"].values,
    index=None,
    placeholder="Select movie name...")
if st.button("Recommend",use_container_width=True):
    name,posters,view,director,actors=recommend(selected_movie_name)

    i = 1
    while (i < 6):
        direct = ", ".join(map(str, director[i]))
        actor = ", ".join(map(str, actors[i]))

        st.markdown("""
            <style>
                .container {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                }
                .card {
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    overflow: hidden;
                    margin: 10px;
                    width: 300px;
                }
                .car-d {
                    background-color: #ffffff;
                    border-radius: 10px;
                   
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    overflow: hidden;
                    margin: 5px;
                    width: 300px;
                } 
                .card img {
                    width: 100%;
                    height: auto;
                }
                .card-body {
                    padding: 15px;
                }
                .car-d-body {
                 border-color: #888888;
                border-top-style: solid; 
                    padding: 5px;
                } 
                .card-title {
                    font-size: 2em;
                    color: #888888; 
                    margin: 0;
                }
                .card-text {
                    color: #888888;
                    margin-bottom: 15px;
                }
                h3 {
                color:#888887;
                }                
            </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="card">
            <h1 class="card-title">{}</h5> 
            <img src="{}" alt="Snowboarding Gear">
             
            <div class="card-body">                    
                <h3>Overview</h3>
                <p class="card-text">{}</p>
            </div>
            </div>
        """.format(name[i],posters[i],view[i]), unsafe_allow_html=True)
        st.markdown("""
                    <div class="car-d">
                    <h3>Director</h3> 
                    <p class="card-text">{}</p>
                     
                    <div class="car-d-body">                    
                        <h3>Lead Actor</h3>
                        <p class="card-text">{}</p>
                    </div>
                    </div>
                """.format(direct,actor), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        i+=1