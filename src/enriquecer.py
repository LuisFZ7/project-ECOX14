from pathlib import Path
import pandas as pd
from config import *

def carregar_dados():
    arquivo_famous = max(
        PRATAFG.glob("gamesfamous_*.parquet"),
        key=lambda x: x.name
    )

    arquivo_steam = max(
        PRATASG.glob("gamessteam_*.parquet"),
        key=lambda x: x.name
    )

    famous_games = pd.read_parquet(arquivo_famous)
    steam_games = pd.read_parquet(arquivo_steam)

    return famous_games, steam_games

#agrupar os jogos de diferentes plataformas em um unico jogo para visualizar as vendas
def agrupar_famous(famous_games):
    agrupado = (
        famous_games
        .groupby("normalized_title", as_index=False)
        .agg({
            "title": "first",
            "total_sales": "sum",
            "genre": "first",
            "publisher": "first",
            "developer": "first",
            "release_date": "first",
        })
    )

    return agrupado

def remover_duplicatas_normalizadas(df):
    df = df.drop_duplicates(
        subset=["normalized_title"],
        keep=False
    ).copy()

    return df


def juntar(famous_games, steam_games):
    resultado = famous_games.merge(
    steam_games,
    left_on="normalized_title",
    right_on="normalized_title",
    how="left",
    validate="many_to_one",
    )
    return resultado

def validar(famous_games, resultado):
    sem_par = resultado["AppID"].isna()

    print("famous_games :", len(famous_games))
    print("resultado:", len(resultado))
    print("sem par :", int(sem_par.sum()))

    if len(resultado) != len(famous_games):
        print("ATENCAO: o numero de linhas mudou.")

    return resultado[sem_par]

def estatisticas(famous_games, steam_games):
    esq = set(steam_games["normalized_title"])
    dir_ = set(famous_games["normalized_title"])

    print("\nNomes Correspondentes")
    print("Steam Games:", len(esq - dir_))
    print("Famous Games:", len(dir_ - esq))
    print("Ambos:", len(esq & dir_))

def salvar(resultado):
    destino = PRATA / "games.parquet"
    destino.parent.mkdir(parents=True, exist_ok=True)

    resultado.to_parquet(destino, index=False)

    print("Salvo em:", destino)

def main():
    famous_games, steam_games = carregar_dados()

    steam_games = remover_duplicatas_normalizadas(steam_games)
    famous_games = agrupar_famous(famous_games)

    resultado = juntar(famous_games, steam_games)

    salvar(resultado)

    sem_correspondencia = validar(
        famous_games,
        resultado
    )
    print(resultado.columns.tolist())

    estatisticas(famous_games, steam_games)

if __name__ == "__main__":
    main()


