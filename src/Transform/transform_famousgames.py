import json
from datetime import datetime
from pathlib import Path
import re
import unicodedata
from config import BRONZEFG, PRATAFG
import pandas as pd

PADRAO = "gamesfamous_*.csv"

def carregar():
    arquivos = sorted(BRONZEFG.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError(f"nada em {BRONZEFG}")
    caminho = arquivos[-1]
    df = pd.read_csv(caminho)
    return df, caminho

def tirar_espacos(df):
    df.columns = df.columns.str.strip()
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].str.strip()
    return df

def tratar_metricas_jogos(df):
    colunas_metricas = ["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]
    
    for coluna in colunas_metricas:
        if coluna in df.columns:
            df[coluna] = df[coluna] * 1000000

    return df

def ordenar_rating(df):
    df_ordenado = df.sort_values(by="total_sales", ascending=False)
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

def normalize_names(df):
    def normalizar(nome):
        nome = str(nome)

        nome = re.sub(r"[®™©]", "", nome)

        nome = unicodedata.normalize("NFKD", nome)
        nome = "".join(
            c for c in nome
            if not unicodedata.combining(c)
        )

        nome = nome.lower()
        nome = re.sub(r"[^a-z0-9]+", "_", nome)

        return nome.strip("_")

    df["normalized_title"] = df["title"].apply(normalizar)
    return df


def salvar(df, origem):
    PRATAFG.mkdir(parents=True, exist_ok=True)
    destino = PRATAFG / origem.with_suffix(".parquet").name
    df.to_parquet(destino, index=False)
    print("salvo em:", destino, df.shape)
    return destino

def main():
    df, origem = carregar()
    tratar_metricas_jogos(df)
    df_ordenado = ordenar_rating(df)
    df_limpo = delete_unecessary_collumns(df_ordenado)
    df_limpo = normalize_names(df_limpo)
    df_limpo = df_limpo.dropna(subset=["total_sales"])
    destino = salvar(df_limpo, origem)

#   print(df_limpo.head(10))
    

if __name__ == "__main__":
    main()