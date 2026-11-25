from pathlib import Path
import duckdb

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "dados" / "ouro" / "projeto.duckdb"


def _consultar(sql, parametros=None):
    con = duckdb.connect(str(BANCO), read_only=True)
    try:
        return con.execute(sql, parametros or []).df()
    finally:
        con.close()


def generos():
    """Retorna a lista de generos disponíveis."""
    return _consultar(
        """
        SELECT DISTINCT genero
        FROM ouro.dim_jogos
        WHERE genero IS NOT NULL
        ORDER BY genero
        """
    )

def names():
    """Retorna a lista de jogos disponíveis."""
    return _consultar(
        """
        SELECT DISTINCT nome
        FROM ouro.vw_jogos
        WHERE nome IS NOT NULL
        ORDER BY vendas_totais DESC
        """
    )

def todos_jogos():
    """Retorna todos os jogos da camada ouro."""
    return _consultar(
        """
        SELECT *
        FROM ouro.vw_jogos
        ORDER BY nome DESC
        """
    )

def top10_generos():
    """Retorna top 10 generos."""
    return _consultar(
        """
        SELECT
            genero,
            SUM (vendas_totais) AS total_vendas
        FROM ouro.vw_jogos
        WHERE genero IS NOT NULL
        GROUP BY genero
        ORDER BY total_vendas DESC
        LIMIT 10
        """
    )

def jogos_por_genero(genero):
    """Indicadores dos jogos de um determinado genero."""
    return _consultar(
        """
        SELECT
            nome,
            genero,
            vendas_totais,
            nota_da_critica,
            percentual_positivo
            avaliacoes_positivas,
            avaliacoes_negativas
        FROM ouro.vw_jogos
        WHERE genero ILIKE ?
        ORDER BY vendas_totais DESC
        """,
        [f"%{genero}%"],
    )