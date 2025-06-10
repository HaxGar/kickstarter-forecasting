import pandas as pd
import ast

from pathlib import Path
from kickstarter_predictor.params import *
from kickstarter_predictor.preprocess_ML import *

def load_raw_projects(filterLive)->pd.DataFrame:
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

def load_merged_raw_data(filterLive:bool=True)->pd.DataFrame:
    '''
    merge the two df : comments and projects
        -   ligne par ligne si ligne_par_ligne==True,
        -   sinon par projet
    '''
    df_comments = load_raw_commentaires()
    df_projects = load_raw_projects(filterLive)
    df_merged = (
        df_comments.merge(
            df_projects[['id', 'state', 'name']]
        )
    )
    print(f"✅ {len(df_merged)} projets merged avec ses commentaires dans load_merged_raw_data")
    return df_merged

def load_data(ligne_par_commentaire=False, **kwargs)->pd.DataFrame:
    '''
    Load merged data from cache ou de raw selon 2 scénarios possible :
        - une ligne par chaque commentaire si ligne_par_ligne==True
        - une ligne par projet avec les commentaires regroupés si ligne_par_ligne==False,
    Il renvoi ensuite le DataFrame nettoyé
    '''

    # Load cleaned data from cache ou de raw
    cleaned_path = Path(LOCAL_DATA_PATH).joinpath(
        'processed',
        'cleaned_commentaires.parquet')
    if cleaned_path.is_file():
        df = pd.read_parquet(cleaned_path)
    else :
        df = load_merged_raw_data()
        # -------> !!!!! Le temps de débogage pour charger plus vite :
        # df = df.head(50)

        # explode les commentaires pour pouvoir les nettoyer
        df = df.explode('commentaires').reset_index(drop=True)
        df = preprocess(df)
        df.rename(columns={'state':'y'}, inplace=True)

        df.to_parquet(cleaned_path,index=False)
        print(f"✅ Parquet avec {len(df)} commentaires nettoyés sauvegardé : {cleaned_path}")

    # Return data selon le format choisi
    if not ligne_par_commentaire :
        # nous regroupons par projets
        df = (
            df
            .groupby(['id', 'y', 'name'])
            .agg({
                'X': lambda s: '; '.join(map(str, s)),
                'commentaires': list
            })
            .reset_index()
        )

    # drop duplicates, nan selon
    _test = len(df)
    df = df.dropna(subset=['X'])
    print(f"❌ {_test - len(df)} nan dropped ")
    _test = len(df)
    df = df.drop_duplicates(subset=['X'])
    print(f"❌ {_test - len(df)} duplicates dropped ")

    print(f"✅ load_data retourne {len(df)} lignes")

    return df


def load_live_projects_comments(ligne_par_commentaire=True) :
    '''
    tout est dans son nom :)
    charge les commentaires (unitaires ou regroupés) des projets live pour test
    '''
    print("--------🔄 Entrée dans la fonction load_live_projects_comments--------")

    cache_path = get_cache_path(ligne_par_commentaire, 'live_data')

    if cache_path.is_file():
        df = pd.read_parquet(cache_path)
    else :
        df = load_merged_raw_data(
            ligne_par_commentaire=ligne_par_commentaire,
            filterLive=False
        )
        # uniquement les project live :
        df = df[df['y']=='live']

        # on garde le commentaire original aussi
        df['commentaire'] = df['X']
        # cleaning :
        df['X'] = df['X'].apply(cleaning_sentence)

        before_nan = len(df)
        df = df.dropna(subset=['X_cleaned'])
        print(f"{before_nan - len(df)} commentaires supprimés car possède nan")
        before_duplicate = len(df)
        df = df.drop_duplicates(subset=['X_cleaned'])
        print(f"{before_duplicate - len(df)} commentaires supprimés car possède dupplicate")
        df.reset_index(inplace=True)
        df.to_parquet(cache_path,index=False)

    print(f"✅ Sortie de la fonction load_live_projects_comments - df.length : {len(df)}")
    return df

def get_cache_path(ligne_par_commentaire, filename):
    scenario = 'par_commentaire' if ligne_par_commentaire else 'par_projet'
    return Path(LOCAL_DATA_PATH).joinpath(
        'processed',
        scenario,
        f'{filename}.parquet'
    )



if __name__=='__main__':
    load_data(False)
