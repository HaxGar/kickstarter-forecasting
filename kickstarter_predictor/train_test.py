from __future__ import annotations

from pathlib import Path
from typing import Tuple, Literal, Optional

import pandas as pd
from sklearn.model_selection import train_test_split

from kickstarter_predictor.params import LOCAL_DATA_PATH

# Constantes

DEFAULT_OUTPUT_DIR: Path = Path(LOCAL_DATA_PATH) / "processed"
DEFAULT_BASE_FILENAME: str = "merged_data"

__all__ = ["split_df", "save_split", "load_or_create_split"]

def split_df(df: pd.DataFrame,*, test_size: float = 0.2, random_state: int = 0, balancing: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Répartit df en train/test et équilibre le train si demandé."""
    print('---------split_split---------')
    # Vérification colonnes
    required = {"id", "X", "y"}
    if not required.issubset(df.columns):
        raise ValueError(
            f"Le DataFrame doit contenir {required}, colonnes présentes: {set(df.columns)}"
        )

    # Split pur avec stratification sur y
    X = df.drop(columns=["y"])
    y = df["y"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    train_df = pd.concat([X_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)[["id", "X", "y"]]
    test_df = pd.concat([X_test.reset_index(drop=True), y_test.reset_index(drop=True)], axis=1)[["id", "X", "y"]]

    # Équilibrage sur le train uniquement
    if balancing:
        print('----balancing----')
        df0 = train_df[train_df.y == 0]
        df1 = train_df[train_df.y == 1]
        # sur-échantillonner la minorité
        df1_up = df1.sample(n=len(df0), replace=True, random_state=random_state)
        train_df = pd.concat([df0, df1_up], axis=0)
        # shuffle
        train_df = train_df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    print('ALL')
    print(X.shape)
    print('TRAIN')
    print(train_df['y'].value_counts(normalize=True))
    print(train_df.shape)
    print('TEST')
    print(test_df['y'].value_counts(normalize=True))
    print(test_df.shape)
    return train_df, test_df

def save_split(train_df: pd.DataFrame, test_df: pd.DataFrame, *, base_filename: str, output_dir: Path) -> Tuple[Path, Path]:
    """Enregistre train_df & test_df en Parquet dans output_dir."""
    print('---------save_split---------')
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    train_path = folder / f"{base_filename}_train.parquet"
    test_path = folder / f"{base_filename}_test.parquet"

    train_df.to_parquet(train_path, index=False)
    test_df.to_parquet(test_path, index=False)

    return train_path, test_path

def load_or_create_split(*, file: Literal["train", "test"], df: Optional[pd.DataFrame] = None,
    ligne_par_commentaire: bool = True, balancing: bool = True,
    base_filename: str = DEFAULT_BASE_FILENAME, output_dir: Path = DEFAULT_OUTPUT_DIR,
    test_size: float = 0.2, random_state: int = 0) -> Tuple[pd.Series, pd.Series]:
    """Renvoie X, y du subset demandé, avec balancing du train si nécessaire."""
    print('---------départ---------')
    sub = "par_commentaire" if ligne_par_commentaire else "par_projet"
    folder = Path(output_dir) / sub
    subset_path = folder / f"{base_filename}_{file}.parquet"

    if subset_path.is_file():
        df_subset = pd.read_parquet(subset_path)
    else:
        if df is None:
            raise FileNotFoundError(
                f"{subset_path} introuvable et aucun DataFrame fourni."
            )
        train_df, test_df = split_df(
            df,
            test_size=test_size,
            random_state=random_state,
            balancing=balancing,
        )
        save_split(train_df, test_df, base_filename=base_filename, output_dir=folder)
        df_subset = train_df if file == "train" else test_df
    return df_subset["X"], df_subset["y"]
