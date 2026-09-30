import json
from datetime import datetime
from pathlib import Path
import csv

import pandas as pd

BRONZE = Path("../dados/bronze/SteamGames")
PRATA = Path("../dados/prata/SteamGames")
PADRAO = "gamessteam_*.csv"

def carregar():
    arquivos = sorted(BRONZE.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError(f"nada em {BRONZE}")

    caminho = arquivos[-1]

    df = pd.read_csv(caminho, header=None, skiprows=1)

    del df[8]

    df.columns = [
        'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU',
        'Required age', 'Price', 'DiscountDLC count', 'About the game',
        'Supported languages', 'Full audio languages', 'Reviews',
        'Header image', 'Website', 'Support url', 'Support email',
        'Windows', 'Mac', 'Linux', 'Metacritic score', 'Metacritic url',
        'User score', 'Positive', 'Negative', 'Score rank', 'Achievements',
        'Recommendations', 'Notes', 'Average playtime forever',
        'Average playtime two weeks', 'Median playtime forever',
        'Median playtime two weeks', 'Developers', 'Publishers',
        'Categories', 'Genres', 'Tags', 'Screenshots', 'Movies'
    ]

    return df, caminho

def ordenar_rating(df):
    df_ordenado = df.sort_values(by="Positive", ascending=False)
    return df_ordenado

def remove_duplicates(df):
    df_limpo = df.drop_duplicates(subset=["Name"]).copy()
    return df_limpo

def remover_nans_geral(df):
    df = df.dropna(
        subset=["Genres", "Metacritic score", "Positive", "Negative"]).copy()

    df = df[df["Metacritic score"] > 1]

    return df

def delete_unecessary_collumns(df_limpo):
    df_limpo = df_limpo.drop(columns=['AppID', 'Estimated owners', 'Peak CCU', 'Required age', 'Price', 'DiscountDLC count', 'About the game', 'Supported languages', 
                                      'Full audio languages', 'Reviews', 'Header image', 'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux',
                                      'Metacritic url', 'Achievements', 'Recommendations', 'Notes', 'Average playtime forever', 
                                      'Average playtime two weeks', 'Median playtime forever', 'Median playtime two weeks', 'Publishers', 'Categories',
                                      'Tags', 'Screenshots', 'Movies', 'Score rank', "User score"])
    return df_limpo

# percentual de relação entre notas positivas e negativas
def criar_percentual_positivo(df):
    total = df["Positive"] + df["Negative"]

    df["percentual_positivo"] = (df["Positive"] / total * 100)

    return df

# arrumar datas para ter certeza que estão no formato correto
def corrigir_datas(df):
    df["Release date"] = pd.to_datetime(df["Release date"], errors="coerce")

    return df

# ter certeza que nas colunas está sendo usado números
def corrigir_tipos(df):
    colunas_numericas = ["Metacritic score", "Positive", "Negative"]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


def main():
    df, origem = carregar()

    df = corrigir_tipos(df)
    df = remover_nans_geral(df)
    df = delete_unecessary_collumns(df)
    df = corrigir_datas(df)
    df = criar_percentual_positivo(df)
    df = ordenar_rating(df)
    df_limpo = criar_percentual_positivo(df)

    caminho_saida = PRATA / origem.name
    df_limpo.to_csv(caminho_saida, index=False)
    
    print(df_limpo.head(10))
    

if __name__ == "__main__":
    main()