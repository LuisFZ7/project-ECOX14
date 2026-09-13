import json
from datetime import datetime
from pathlib import Path

import pandas as pd

BRONZE = Path("../dados/bronze/FamousGames")
PRATA = Path("../dados/prata/FamousGames")
PADRAO = "gamesfamous_*.csv"

def carregar():
    arquivos = sorted(BRONZE.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError(f"nada em {BRONZE}")
    caminho = arquivos[-1]
    df = pd.read_csv(caminho)
    #print("lido:", caminho.name, df.shape)
    #print(df.columns.tolist())
    #print(df.isna().sum())
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
    df_limpo = df.dropna().copy()
    return df_limpo

def delete_unecessary_collumns(df_limpo):
    df_limpo = df_limpo.drop(columns=['img', 'last_update', 'na_sales', 'jp_sales', 'pal_sales', 'other_sales'])
    return df_limpo

def main():
    df, origem = carregar()
    tratar_metricas_jogos(df)
    df_ordenado = ordenar_rating(df)
    df_limpo = remove_duplicates(df_ordenado)
    df_limpo = delete_unecessary_collumns(df_limpo)
    df_limpo = df_limpo.dropna(subset=["total_sales"])

    caminho_saida = PRATA / origem.name
    df_limpo.to_csv(caminho_saida, index=False)
    
    print(df_limpo.head(10))
    

if __name__ == "__main__":
    main()