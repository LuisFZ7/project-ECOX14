{{ config(materialized='view') }}

SELECT
    f.*,
    d.nome,
    d.plataforma,
    d.genero,
    d.publicadora,
    d.desenvolvedora,
    d.data_lancamento,
    d.chave_normalizada
FROM {{ ref('fato_jogos') }} f
JOIN {{ ref('dim_jogos') }} d
    USING (jogo_id)