from pathlib import Path
import logging

RAIZ = Path(__file__).resolve().parent.parent

DADOS = RAIZ / "dados"

BRONZE = DADOS / "bronze"
BRONZEFG = BRONZE / "FamousGames"
BRONZESG = BRONZE / "SteamGames"

PRATA = DADOS / "prata"
PRATAFG = PRATA / "FamousGames"
PRATASG = PRATA / "SteamGames"


OURO = DADOS / "ouro"

def configurar_log():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(RAIZ / "pipeline.log"),
            logging.StreamHandler(),
        ],
    )


# nos outros arquivos
#from config import BRONZE, PRATA