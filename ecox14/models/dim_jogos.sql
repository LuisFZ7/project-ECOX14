SELECT
    normalized_title,
    AppID,
    title AS nome,
    genre AS genero,
    publisher AS publicadora,
    developer AS desenvolvedora,
    release_date AS data_lancamento,
    normalized_title AS chave_normalizada
FROM {{ source('prata', 'games') }}