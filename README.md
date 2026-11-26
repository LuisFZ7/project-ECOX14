## Fontes de dados
| Fonte | Formato | Acesso | Extraido | Link |
|---|---|---|---|---|
| Steam Games Dataset | CSV | token | 25/11/2026 | kaggle.com/datasets/fronkongames/steam-games-dataset |
| Famous Video Games | CSV | token | 25/11/2026 | kaggle.com/datasets/ujjwalaggarwal402/video-games-dataset |

## Juncao
FamousGames juntado ao SteamGames por normalized_title, utilizando how=left.

- Linhas em Steam Games: 3458
- Linhas em Famous Games: 12191
- Correspondências: 723
- Sem correspondências: 11468

## Limitações dos dados
Foram encontradas limitações nas quantidades de jogos vendidos, devido ao fato que muitos jogos são multi-plataforma e os datasets utilizados não possuem todas as plataformas, isso deve afetar análises.

## Ordem de execução do projeto

**Clonagem:**

```
git clone https://github.com/LuisFZ7/project-ECOX14.git
cd project-ECOX14
```

**Criação do ambiente virtual:**
```
python -m venv .venv
```
**Ativar no windows:**
```
.venv\Scripts\activate
```
**Instalar dependências:**
```
pip install -r requirements.txt
```
**Execução do Pipeline:**
```
python src/pipeline.py
```
**Executar a modelagem com dbt:**
```
cd ecox14
dbt run
```
**Iniciar dashboard do streamlit**
```
cd ..
streamlit run dashboard/painel.py
```