from pathlib import Path
import duckdb

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "dados" / "ouro" / "projeto.duckdb"

con = duckdb.connect(str(BANCO), read_only=True)

try:
    consultas = {
        "DIMENSAO": """
            SELECT jogo_id, nome, plataforma, AppID
            FROM ouro.dim_jogos
            WHERE nome ILIKE '%Grand Theft Auto V%'
        """,

        "FATO": """
            SELECT f.*
            FROM ouro.fato_jogos f
            JOIN ouro.dim_jogos d USING (jogo_id)
            WHERE d.nome ILIKE '%Grand Theft Auto V%'
        """,

        "VIEW": """
            SELECT nome, plataforma, AppID, vendas_totais
            FROM ouro.vw_jogos
            WHERE nome ILIKE '%Grand Theft Auto V%'
        """
    }

    for nome, sql in consultas.items():
        print(f"\n===== {nome} =====")

        resultado = con.execute(sql).df()

        if resultado.empty:
            print("Nenhum registro encontrado.")
        else:
            print(resultado.to_string(index=False))

finally:
    con.close()