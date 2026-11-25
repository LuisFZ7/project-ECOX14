
import logging
import duckdb

from config import PRATA, OURO

log = logging.getLogger(__name__)

BANCO = OURO / "projeto.duckdb"


def um_valor(con, sql):
    return con.execute(sql).fetchone()[0]


def conectar():
    BANCO.parent.mkdir(parents=True, exist_ok=True)
    log.info("banco: %s", BANCO)
    return duckdb.connect(str(BANCO))


def criar_esquemas(con):
    con.execute("CREATE SCHEMA IF NOT EXISTS prata")
    con.execute("CREATE SCHEMA IF NOT EXISTS ouro")
    log.info("esquemas prata e ouro prontos")


def carregar_prata(con):
    caminho = PRATA / "games.parquet"

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")

    con.execute(f"""
        CREATE OR REPLACE TABLE prata.games AS
        SELECT *
        FROM read_parquet('{caminho.as_posix()}')
    """)

    linhas = um_valor(
        con,
        "SELECT COUNT(*) FROM prata.games"
    )

    log.info("prata.games: %s linhas", linhas)

def main():
    con = conectar()

    try:
        criar_esquemas(con)
        carregar_prata(con)

    finally:
        con.close()

    log.info("carga concluida")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

    main()
