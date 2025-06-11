import pandas as pd
import ast

from pathlib import Path
from kickstarter_predictor.params import *
from kickstarter_predictor.preprocess_ML import *

def load_raw_projects(live)->pd.DataFrame:
    '''
    read the raw csv of projects
    state=='live' if live=True,
    sinon, seulement les projets live
    prepare for the merge ('ID' renamed to 'id')
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "ks-projects-201801.csv")
    df_projects = pd.read_csv(path)
    df_projects.rename(columns={'ID':'id'}, inplace=True)
    if live :
        df_projects = df_projects[df_projects['state']=='live']
    else :
        df_projects = df_projects[df_projects['state']!='live']
        df_projects['state'] = df_projects['state'].apply(lambda x: 1 if x == 'successful' else 0)
    print(f"✅ {len(df_projects)} projects loaded dans load_raw_projects")
    return df_projects

def load_raw_commentaires()->pd.DataFrame:
    '''
    read the raw csv of comments by filtering out the empty coments
    '''
    path = Path(LOCAL_DATA_PATH).joinpath('raw', "comments_clean.csv")
    df_comments = pd.read_csv(path)
    df_comments = df_comments[df_comments['comments']!='[]']
    # cast string as py list
    df_comments['commentaires'] = df_comments['comments'].apply(ast.literal_eval)
    df_comments.drop(columns=['comments'], inplace=True)
    print(f"✅ {len(df_comments)} commentaires loaded dans load_raw_commentaires")
    return df_comments

def load_merged_raw_data(live:bool=False)->pd.DataFrame:
    '''
    merge the two df : comments and projects
        -   ligne par ligne si ligne_par_ligne==True,
        -   sinon par projet
    '''
    df_comments = load_raw_commentaires()
    df_projects = load_raw_projects(live)
    df_merged = (
        df_comments.merge(
            df_projects[['id', 'state', 'name']]
        )
    )
    print(f"✅ {len(df_merged)} projets merged avec ses commentaires dans load_merged_raw_data")
    return df_merged

def load_data(ligne_par_commentaire=False, live=False, **kwargs)->pd.DataFrame:
    '''
    Load merged data from cache ou de raw selon 2 scénarios possible :
        - une ligne par chaque commentaire si ligne_par_ligne==True
        - une ligne par projet avec les commentaires regroupés si ligne_par_ligne==False,
    Il renvoi ensuite le DataFrame nettoyé
    '''
    filename = 'live_commentaires' if live else 'cleaned_commentaires'
    # Load data from cache ou de raw
    cleaned_path = Path(LOCAL_DATA_PATH).joinpath(
        'processed',
        f'{filename}.parquet')
    if cleaned_path.is_file():
        df = pd.read_parquet(cleaned_path)
    else :
        df = load_merged_raw_data(live)
        # -------> !!!!! Le temps de débogage pour charger plus vite :
        # df = df.head(50)

        # explode les commentaires
        df = df.explode('commentaires').reset_index(drop=True)

        if not live :
            df = preprocess(df)
            df.rename(columns={'state':'y'}, inplace=True)

        df.to_parquet(cleaned_path,index=False)
        print(f"✅ Parquet avec {len(df)} commentaires sauvegardé : {cleaned_path}")

    # Return data selon le format choisi
    if not ligne_par_commentaire :
        # nous regroupons par projets
        if not live :
            df = (
                df
                .groupby(['id', 'y', 'name'])
                .agg({
                    'X': lambda s: '; '.join(map(str, s)),
                    'commentaires': list
                })
                .reset_index()
            )
        else :
            df = (
                df
                .groupby(['id', 'name'])['commentaires']
                .apply(list)
                .reset_index()
            )

    _col_name = 'commentaires' if live else 'X'
    # drop duplicates, nan selon
    _test = len(df)
    df = df.dropna(subset=[_col_name])
    print(f"❌ {_test - len(df)} nan dropped ")
    _test = len(df)
    df = df.drop_duplicates(subset=[_col_name])
    print(f"❌ {_test - len(df)} duplicates dropped ")
    print(f"✅ load_data return {len(df)} lignes")
    return df

def get_cache_path(ligne_par_commentaire, filename):
    scenario = 'par_commentaire' if ligne_par_commentaire else 'par_projet'
    return Path(LOCAL_DATA_PATH).joinpath(
        'processed',
        scenario,
        f'{filename}.parquet'
    )
def load_data_by_project_title(titre_du_projet) :
    df = load_data(ligne_par_commentaire=False, live=True)
    projet = df[df['name'] == titre_du_projet]
    return preprocess_projet(projet)

def load_data_by_project_id(id_projet) :
    df = load_data(ligne_par_commentaire=False, live=True)
    projet = df[df['id'] == id_projet]
    return preprocess_projet(projet)


if __name__=='__main__':
    load_data()
    load_data(live=True)
