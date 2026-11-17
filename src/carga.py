
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

    
def verificar_duplicados(con):
    duplicados = con.execute("""
        SELECT
            AppID,
            title,
            console,
            total_sales,
            normalized_title
        FROM prata.games
        WHERE AppID IN (
            SELECT AppID
            FROM prata.games
            WHERE AppID IS NOT NULL
            GROUP BY AppID
            HAVING COUNT(*) > 1
        )
        ORDER BY AppID, console
    """).df()

    if duplicados.empty:
        log.info("nenhum duplicado encontrado")
    else:
        print(duplicados.to_string(index=False))

def construir_ouro(con):
    con.execute("""
        CREATE OR REPLACE TABLE ouro.dim_jogos AS
        SELECT
            CONCAT(
                normalized_title,
                '_',
                COALESCE(console, 'sem_plataforma')
            ) AS jogo_id,
            AppID,
            title AS nome,
            console AS plataforma,
            genre AS genero,
            publisher AS publicadora,
            developer AS desenvolvedora,
            release_date AS data_lancamento,
            normalized_title AS chave_normalizada
        FROM prata.games
        WHERE AppID IS NOT NULL
    """)

    log.info(
        "ouro.dim_jogos: %s linhas",
        um_valor(con, "SELECT COUNT(*) FROM ouro.dim_jogos")
    )

    con.execute("""
        CREATE OR REPLACE TABLE ouro.fato_jogos AS
        SELECT
            CONCAT(
                normalized_title,
                '_',
                COALESCE(console, 'sem_plataforma')
            ) AS jogo_id,
            AppID,
            total_sales AS vendas_totais,
            critic_score AS nota_da_critica,
            Positive AS avaliacoes_positivas,
            Negative AS avaliacoes_negativas,
            percentual_positivo,
            quantidade_generos
        FROM prata.games
        WHERE AppID IS NOT NULL
    """)

    log.info(
        "ouro.fato_jogos: %s linhas",
        um_valor(con, "SELECT COUNT(*) FROM ouro.fato_jogos")
    )

    con.execute("""
        CREATE OR REPLACE VIEW ouro.vw_jogos AS
        SELECT
            f.*,
            d.nome,
            d.plataforma,
            d.genero,
            d.publicadora,
            d.desenvolvedora,
            d.data_lancamento
        FROM ouro.fato_jogos f
        JOIN ouro.dim_jogos d USING (jogo_id)
    """)

    log.info("ouro.vw_jogos: criada")


def conferir(con):

    duplicados_dim = um_valor(con, """
        SELECT COUNT(*) FROM (
            SELECT jogo_id
            FROM ouro.dim_jogos
            GROUP BY jogo_id
            HAVING COUNT(*) > 1
        )
    """)

    duplicados_fato = um_valor(con, """
        SELECT COUNT(*) FROM (
            SELECT jogo_id
            FROM ouro.fato_jogos
            GROUP BY jogo_id
            HAVING COUNT(*) > 1
        )
    """)

    orfaos = um_valor(con, """
        SELECT COUNT(*)
        FROM ouro.fato_jogos f
        LEFT JOIN ouro.dim_jogos d USING (jogo_id)
        WHERE d.jogo_id IS NULL
    """)

    log.info("duplicados na dimensao: %s (esperado 0)", duplicados_dim)
    log.info("duplicados na fato    : %s (esperado 0)", duplicados_fato)
    log.info("fatos sem dimensao    : %s (esperado 0)", orfaos)

    if duplicados_dim or duplicados_fato or orfaos:
        raise ValueError(
            f"modelo inconsistente: "
            f"{duplicados_dim} duplicados na dimensao, "
            f"{duplicados_fato} duplicados na fato, "
            f"{orfaos} orfaos"
        )


def main():
    con = conectar()

    try:
        criar_esquemas(con)
        carregar_prata(con)
        verificar_duplicados(con)
    #    construir_ouro(con)
    #    conferir(con)

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
