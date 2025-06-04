import pandas as pd
import ast

def load_projects(filterLive=True):
    '''
    read the raw csv of projects
    without state=='live' if filterLive=True,
    prepare for the merge ('ID' renamed to 'id')
    '''
    df_projects = pd.read_csv('data/raw/ks-projects-201801.csv')
    df_projects.rename(columns={'ID':'id'}, inplace=True)
    if filterLive :
        df_projects = df_projects[df_projects['state']!='live']
        df_projects['state'] = df_projects['state'].apply(lambda x: 1 if x == 'successful' else 0)

    return df_projects

def load_commentaires():
    '''
    read the raw csv of comments
    by filtering out the empty coments
    '''
    df_comments = pd.read_csv('data/raw/comments_clean.csv')
    df_comments = df_comments[df_comments['comments']!='[]']
    # cast string as py list
    df_comments['commentaires'] = df_comments['comments'].apply(ast.literal_eval)
    df_comments.drop(columns=['comments'], inplace=True)

    return df_comments

def load_merged_data(ligne_par_ligne=True):
    '''
    merge the two df : comments and projects
    ligne par ligne si ligne_par_ligne==True,
    sinon par projet
    '''
    df_comments = load_commentaires()
    df_projects = load_projects()

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

#print(load_merged_data(ligne_par_ligne = True))
