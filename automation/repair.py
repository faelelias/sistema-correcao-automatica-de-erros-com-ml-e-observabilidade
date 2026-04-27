import joblib
import os
import logging
import subprocess
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar modelo
try:
    model = joblib.load("ml/error_model.pkl")
    vectorizer = joblib.load("ml/vectorizer.pkl")
    logger.info("Modelo de ML carregado com sucesso")
except FileNotFoundError as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    sys.exit(1)

def reparar(log):
    """
    Analisa um log e executa reparo automático se erro detectado
    
    Args:
        log (str): Mensagem de log para análise
    """
    try:
        X = vectorizer.transform([log])
        prediction = model.predict(X)[0]

        if prediction == "error":
            logger.warning(f"ALERTA - Erro detectado: {log}")
            logger.info("Iniciando procedimento de reparo automático...")
            
            # Tenta reiniciar container da app
            try:
                result = subprocess.run(
                    ["docker", "restart", "code-app-1"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    logger.info("Container reiniciado com sucesso")
                else:
                    logger.warning(f"Erro ao reiniciar container: {result.stderr}")
            except FileNotFoundError:
                logger.error("Docker não encontrado no sistema")
            except subprocess.TimeoutExpired:
                logger.error("Timeout ao reiniciar container")
        else:
            logger.info(f"Log normal, sem ação necessária: {log}")
            
    except Exception as e:
        logger.error(f"Erro ao processar log: {e}", exc_info=True)

# Teste
if __name__ == "__main__":
    logger.info("=== Sistema de Reparo Automático Iniciado ===")
    
    # Testes
    test_logs = [
        "500 Internal Server Error",
        "200 OK - Requisição bem-sucedida",
        "Connection timeout",
        "Database OK"
    ]
    
    for test_log in test_logs:
        logger.info(f"Testando: {test_log}")
        reparar(test_log)
        logger.info("-" * 50)
