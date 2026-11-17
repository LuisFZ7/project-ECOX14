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
FROM {{ source('prata', 'games') }}
WHERE AppID IS NOT NULL