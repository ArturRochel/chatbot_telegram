import sys
from loguru import logger

def setup_logging():
    logger.remove()

    # Adicionamos apenas o console com um formato focado em Rota e Erro
    logger.add(
        sys.stdout,
        colorize=True,
        diagnose=False,
        format=(
            "<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level="DEBUG",
        enqueue=True
    )

# Executa a configuração ao importar o módulo
setup_logging()