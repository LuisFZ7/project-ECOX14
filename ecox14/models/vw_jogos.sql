{{ config(materialized='view') }}
SELECT
    f.*,
    d.nome,
    d.genero,
    d.publicadora,
    d.desenvolvedora,
    d.data_lancamento
FROM {{ ref('fato_jogos') }} f
JOIN {{ ref('dim_jogos') }} d
    USING (normalized_title)

