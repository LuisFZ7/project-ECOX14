SELECT
    normalized_title,
    AppID,
    total_sales AS vendas_totais,
    "Metacritic score" AS nota_da_critica,
    Positive AS avaliacoes_positivas,
    Negative AS avaliacoes_negativas,
    percentual_positivo,
    quantidade_generos
FROM {{ source('prata', 'games') }}
