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
FROM {{ source('prata', 'games') }}
WHERE AppID IS NOT NULL