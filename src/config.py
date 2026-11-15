from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

DADOS = RAIZ / "dados"
BRONZE = DADOS / "bronze"
BRONZEFG = BRONZE / "FamousGames"
BRONZESG = BRONZE / "SteamGames"
PRATA = DADOS / "prata"


# nos outros arquivos
#from config import BRONZE, PRATA