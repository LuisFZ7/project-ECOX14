from pathlib import Path
import pandas as pd
from config import PRATAFG, PRATASG

PRATAFG = Path("../dados/prata/FamousGames")
PRATASG = Path("../dados/prata/SteamGames")

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

def juntar(famous_games, steam_games):
    return famous_games.merge(
    steam_games,
    left_on="normalized_title",
    right_on="normalized_title",
    how="left",
    validate="many_to_one",
    )

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

def verificar_duplicatas(steam_games):
    duplicados = steam_games[
        steam_games.duplicated(
            subset=["normalized_title"],
            keep=False
        )
    ].sort_values("normalized_title")

    print("\nDUPLICATAS NO STEAM GAMES")
    print("Total de registros duplicados:", len(duplicados))

    print(
        duplicados[
            ["Name", "normalized_title", "AppID"]
        ].to_string(index=False)
    )

def salvar(resultado):
    destino = Path("../dados/prata/games.parquet")
    destino.parent.mkdir(parents=True, exist_ok=True)

    resultado.to_parquet(destino, index=False)

    print("Salvo em:", destino)

def main():
    famous_games, steam_games = carregar_dados()

    verificar_duplicatas(steam_games)

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