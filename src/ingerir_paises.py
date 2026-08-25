import requests
from pathlib import Path
import kagglehub
from datetime import date
import shutil
import json
from datetime import datetime
import pandas as pd

URL = "https://api.worldbank.org/v2/country"
BRONZE = Path("dados/bronze/banco_mundial")

def buscar():
    r = requests.get(URL, params={
        "format": "json", "per_page": 300}, timeout=30)
    r.raise_for_status()
    return r.json()

def conferir(dados):
    meta = dados[0]
    print("registros:", meta["total"])
    print("paginas :", meta["pages"])
    if meta["pages"] > 1:
        print("ATENCAO: falta paginar")
    return meta

def salvar(dados):
    BRONZE.mkdir(parents=True, exist_ok=True)
    paises = pd.json_normalize(dados[1])
    hoje = date.today().strftime("%Y%m%d")
    destino = BRONZE / f"paises_{hoje}.csv"
    paises.to_csv(destino, index=False)
    print(paises["region.value"].unique())
    return destino

def registrar(destino, meta):
    info = {
        "fonte": URL,
        "arquivo_bronze": destino.name,
        "registros": meta["total"],
        "extraido_em": datetime.now().isoformat(),
    }
    (BRONZE / "proveniencia.json").write_text(
    json.dumps(info, indent=2))

def main():
    dados = buscar()
    meta = conferir(dados)
    registrar(salvar(dados), meta)
  
if __name__ == "__main__":
    main()