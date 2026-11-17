import duckdb
from carga import BANCO

con = duckdb.connect(str(BANCO))

resultado = con.execute("""
    SELECT
        title AS jogo,
        COUNT(*) AS quantidade_registros,
        SUM(total_sales) AS vendas_somadas
    FROM prata.games
    WHERE LOWER(title) LIKE '%grand theft auto v%'
    GROUP BY title
    ORDER BY vendas_somadas DESC
""").df()

print("\nVendas somadas de GTA V:\n")
print(resultado.to_string(index=False))

con.close()