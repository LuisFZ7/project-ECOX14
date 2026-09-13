from pathlib import Path
import pandas as pd
from data_profiling import ProfileReport
from wordcloud import WordCloud

RELATORIOS = Path("relatorios")

BRONZE = Path("../dados/bronze/PopularGames")
PADRAO = "games*.csv"



def gerar(caminho):
    df = pd.read_csv(caminho)

    colunas_texto = [
      "About the game",
      "Name",
      "Header image",
      "Website",
      "Support url",
      "Support email",
      "Notes",
      "Short description",
      "Detailed description",
      "Movies",
      "Screenshots",
      "Supported languages",
      "Full audio languages",
      "Packages",
      "Developers",
      "Publishers",
      "Categories",
      "Genres",
      "Tags",
    ]

    df_analise = df.drop(
      columns=[c for c in colunas_texto if c in df.columns], errors="ignore"
    )

    perfil = ProfileReport(df_analise, title=caminho.name, minimal=True)

    RELATORIOS.mkdir(exist_ok=True)
    saida = RELATORIOS / f"{caminho.stem}.html"
    perfil.to_file(saida)
    return saida

def mais_recente():
    arquivos = sorted(BRONZE.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError("bronze vazia")
    return arquivos[-1]

def main():
    caminho = mais_recente()
    print("perfilando:", caminho.name)
    print(gerar(caminho))

if __name__ == "__main__":
    main()
