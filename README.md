## Fontes de dados
| Fonte | Formato | Acesso | Extraido | Link |
|---|---|---|---|---|
| Steam Games Dataset | CSV | token | 30/09/2026 | kaggle.com/datasets/fronkongames/steam-games-dataset |
| Famous Video Games | CSV | token | 30/09/2026 | kaggle.com/datasets/ujjwalaggarwal402/video-games-dataset |

## Juncao
FamousGames juntado ao SteamGames por normalized_title, utilizando how=left.

- Linhas em Steam Games: 3458
- Linhas em Famous Games: 12191
- Correspondências: 723
- Sem correspondências: 11468

## Limitações dos dados
Foram encontradas limitações nas quantidades de jogos vendidos, devido ao fato que muitos jogos são multi-plataforma e os datasets utilizados não possuem todas as plataformas, isso deve afetar análises.