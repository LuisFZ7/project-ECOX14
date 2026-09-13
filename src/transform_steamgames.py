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

def tirar_espacos(df):
    df.columns = df.columns.str.strip()
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].str.strip()
    return df

def conferir_chave(df, chave="title"):
    repetidas = df[chave].duplicated().sum()
    print("chaves repetidas:", repetidas)
    if repetidas:
        print(df[df[chave].duplicated(keep=False)])
    return df.drop_duplicates(subset=chave)

def transformK_number(valor):
    if pd.isna(valor):
        return valor
    
def tratar_metricas_jogos(df):
    colunas_metricas = ["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]
    
    for coluna in colunas_metricas:
        if coluna in df.columns:
            df[coluna] = df[coluna] * 1000000

    return df

def ordenar_rating(df):
    df_ordenado = df.sort_values(by="critic_score", ascending=False)
    return df_ordenado

def remove_duplicates(df):
    df_limpo = df.drop_duplicates(subset=["title"]).copy()
    return df_limpo

def remover_nans_geral(df):
    df = df.dropna(subset=["Genres", "Metacritic score", "User score"]).copy()
    df = df[df["Metacritic score"] > 1]
    return df

def delete_unecessary_collumns(df_limpo):
    df_limpo = df_limpo.drop(columns=['AppID', 'Estimated owners', 'Peak CCU', 'Required age', 'Price', 'DiscountDLC count', 'About the game', 'Supported languages', 
                                      'Full audio languages', 'Reviews', 'Header image', 'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux',
                                      'Metacritic url', 'Positive', 'Negative', 'Achievements', 'Recommendations', 'Notes', 'Average playtime forever', 
                                      'Average playtime two weeks', 'Median playtime forever', 'Median playtime two weeks', 'Publishers', 'Categories',
                                      'Tags', 'Screenshots', 'Movies', 'Score rank'])
    return df_limpo

def main():
    df, origem = carregar()

    df = remover_nans_geral(df)
    df_limpo = delete_unecessary_collumns(df)
    #df_limpo = remove_duplicates(df_ordenado)

    caminho_saida = PRATA / origem.name
    df_limpo.to_csv(caminho_saida, index=False)
    
    print(df_limpo.head(10))
    

if __name__ == "__main__":
    main()