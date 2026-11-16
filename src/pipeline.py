
import logging
import sys
from config import configurar_log
from config import RAIZ

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

ETAPAS = [
    ("ingestao", etapa_ingestao),
    ("transform", etapa_transform),
    ("enriquecer", etapa_enriquecer),
    ("carga", etapa_carga),
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
    configurar_log()

    nomes_etapas = [nome for nome, _ in ETAPAS]

    if a_partir_de is not None and a_partir_de not in nomes_etapas:
        raise ValueError(f"Etapa desconhecida: {a_partir_de}")

    comecou = a_partir_de is None

    for nome, funcao in ETAPAS:

        if nome == a_partir_de:
            comecou = True

        if not comecou or funcao is None:
            log.info("etapa %s: pulada", nome)
            continue

        executar(nome, funcao)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
