import pandas as pd
import ast

from pathlib import Path

from attila.params import *

## row data, private funcions :
def load_raw_projects(filterLive=True):
    '''
    read the raw csv of projects
    without state=='live' if filterLive=True,
    prepare for the merge ('ID' renamed to 'id')
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "ks-projects-201801.csv")
    df_projects = pd.read_csv(path)
    df_projects.rename(columns={'ID':'id'}, inplace=True)
    if filterLive :
        df_projects = df_projects[df_projects['state']!='live']
        df_projects['state'] = df_projects['state'].apply(lambda x: 1 if x == 'successful' else 0)

    return df_projects

def load_raw_commentaires():
    '''
    read the raw csv of comments
    by filtering out the empty coments
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "comments_clean.csv")
    df_comments = pd.read_csv(path)
    df_comments = df_comments[df_comments['comments']!='[]']
    # cast string as py list
    df_comments['commentaires'] = df_comments['comments'].apply(ast.literal_eval)
    df_comments.drop(columns=['comments'], inplace=True)

    return df_comments

def load_merged_raw_data(ligne_par_ligne=True):
    '''
    merge the two df : comments and projects
    ligne par ligne si ligne_par_ligne==True,
    sinon par projet
    '''
    df_comments = load_raw_commentaires()
    df_projects = load_raw_projects()

    df_merged = (
        df_comments.merge(
            df_projects[['id', 'state']]
        )
        #.drop(columns=['id'])
    )

    if ligne_par_ligne :
        df_merged = df_merged.explode('commentaires').reset_index(drop=True)
    else :
        df_merged['commentaires'] = df_merged['commentaires'].apply(
            lambda x: '; '.join(x)
        )

    return df_merged.rename(columns={"commentaires": "X", 'state':'y'})

## callable functions
def load_data(
    data_type='merged',
    cached_version=True
    ):
    '''
        data_type : merged ou cleaned
        cached_version : charge directement la version sauvegardé si ça existe
    '''
    cache_path = Path(LOCAL_DATA_PATH).joinpath('processed', f"{data_type}_data.csv")

    if cached_version and cache_path.is_file():
        df = pd.read_csv(cache_path)
    else :
        df = load_merged_raw_data()
        df.to_csv(cache_path)

    return df
