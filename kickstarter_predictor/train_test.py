from __future__ import annotations

from pathlib import Path
from typing import Tuple, Literal, Optional

import pandas as pd
from sklearn.model_selection import train_test_split

from kickstarter_predictor.params import LOCAL_DATA_PATH

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DEFAULT_OUTPUT_DIR: Path = Path(LOCAL_DATA_PATH) / "processed"
DEFAULT_BASE_FILENAME: str = "merged_data"

__all__ = [
    "split_df",
    "save_split",
    "load_or_create_split",
]

# ---------------------------------------------------------------------------
# 1) Split du DataFrame complet
# ---------------------------------------------------------------------------

def split_df(
    df: pd.DataFrame, *, test_size: float = 0.2, random_state: int = 0,
    balancing: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:

    required_cols = {"id", "X", "y"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"Le DataFrame doit contenir les colonnes {required_cols}, "
            f"colonnes présentes : {set(df.columns)}"
        )
    print('----------split_df----------')
    if balancing :
        df0= df[df['y']==0]
        df1= df[df['y']==1].sample(n=df[df['y']==0]['y'].count())

        df_all  = pd.concat([df0, df1])
    else: df_all = df


    X = df_all.drop(columns=["y"])
    y = df_all["y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    train_df = pd.concat([
        X_train.reset_index(drop=True),
        y_train.reset_index(drop=True),
    ], axis=1)[["id", "X", "y" ]]
    test_df = pd.concat([
        X_test.reset_index(drop=True),
        y_test.reset_index(drop=True),
    ], axis=1)[["id", "X", "y" ]]

    return train_df, test_df

# ---------------------------------------------------------------------------
# 2) Sauvegarde au format Parquet
# ---------------------------------------------------------------------------

def save_split(
    train_df: pd.DataFrame, test_df: pd.DataFrame, *,
    base_filename: str, output_dir: Path) -> Tuple[Path, Path]:
    """Enregistre *train_df* & *test_df* en Parquet dans *output_dir*."""
    print('----------save_split----------')
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_path = output_dir / f"{base_filename}_train.parquet"
    test_path = output_dir / f"{base_filename}_test.parquet"

    train_df.to_parquet(train_path, index=False)
    test_df.to_parquet(test_path, index=False)

    return train_path, test_path

# ---------------------------------------------------------------------------
# 3) Wrapper unique : charge ou crée à la volée
# ---------------------------------------------------------------------------

def load_or_create_split(
    *,
    file: Literal["train", "test"], df: Optional[pd.DataFrame] = None, ligne_par_commentaire: bool = True,
    balancing: bool = True,base_filename: str = DEFAULT_BASE_FILENAME,
    output_dir: Path = DEFAULT_OUTPUT_DIR, test_size: float = 0.2, random_state: int = 0) -> Tuple[pd.Series, pd.Series]:
    print('----------load_or_create_split----------')
    # Choix du sous‑dossier selon le flag
    subfolder = "par_commentaire" if ligne_par_commentaire else "par_projet"
    output_dir = Path(output_dir) / subfolder

    subset_path = output_dir / f"{base_filename}_{file}.parquet"

    if subset_path.is_file():
        subset_df = pd.read_parquet(subset_path)
    else:
        if df is None:
            raise FileNotFoundError(
                f"{subset_path} introuvable et aucun DataFrame fourni pour créer le split."
            )

        # Création du split, puis sauvegarde
        train_df, test_df = split_df(
            df,
            test_size=test_size,
            random_state=random_state,
            balancing=balancing
        )
        save_split(
            train_df, test_df,
            base_filename=base_filename,
            output_dir=output_dir
        )
        subset_df = train_df if file == "train" else test_df

    return subset_df["X"], subset_df["y"]
