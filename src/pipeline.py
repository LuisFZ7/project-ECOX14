
import logging
import sys
import config

log = logging.getLogger(__name__)

def etapa_ingestao():
    import Ingestao.ingerir_famousgames as ingerir_famousgames
    import Ingestao.ingerir_steamgames as ingerir_steamgames

    ingerir_famousgames.main()
    ingerir_steamgames.main()


def etapa_transform():
    import Transform.transform_famousgames as transform_famousgames
    import Transform.transform_steamgames as transform_steamgames
    
    transform_famousgames.main()
    transform_steamgames.main()

def etapa_enriquecer():
    import enriquecer
    
    enriquecer.main()

def etapa_carga():
    import carga
    carga.main()

def etapa_modelagem():
    import subprocess
    subprocess.run(
        ["dbt", "run"], 
        cwd=config.RAIZ / "ecox14",
        check=True)

ETAPAS = [
    ("ingestao", etapa_ingestao),
    ("transform", etapa_transform),
    ("enriquecer", etapa_enriquecer),
    ("carga", etapa_carga),
    ("modelagem", etapa_modelagem),
]

def executar(nome, funcao):
    log.info("etapa %s: inicio", nome)

    try:
        funcao()
    except Exception:
        log.exception("etapa %s falhou", nome)
        raise

    log.info("etapa %s: fim", nome)


def main(a_partir_de=None):
    config.configurar_log()

    nomes = [nome for nome, _ in ETAPAS]
    if a_partir_de and a_partir_de not in nomes:
        log.error("etapa desconhecida: %s", a_partir_de)
        log.error("etapas validas: %s", ", ".join(nomes))
        return 1
    comecou = a_partir_de is None

    for nome, funcao in ETAPAS:
        if nome == a_partir_de:
            comecou = True
        if not comecou:
            log.info("etapa %s: pulada", nome)
            continue
        if funcao is None:
            log.warning("etapa %s: ainda nao implementada", nome)
            continue
        executar(nome, funcao)
    log.info("pipeline concluido")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
