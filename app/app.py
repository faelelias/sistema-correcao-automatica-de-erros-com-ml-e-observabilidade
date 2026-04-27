from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import logging
import sys
from datetime import datetime
import time

app = Flask(__name__)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Métricas Prometheus
request_count = Counter('app_requests_total', 'Total de requisições', ['method', 'endpoint', 'status'])
request_duration = Histogram('app_request_duration_seconds', 'Duração das requisições em segundos', ['endpoint'])
errors_total = Counter('app_errors_total', 'Total de erros', ['endpoint'])
app_health = Gauge('app_health_status', 'Status da aplicação (1=saudável, 0=erro)')

# Middleware para registrar métricas
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        request_count.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        request_duration.labels(endpoint=request.path).observe(duration)
    return response

@app.route("/")
def home():
    logger.info("Requisição recebida na rota /")
    return jsonify({
        "status": "success",
        "message": "Aplicação rodando com observabilidade!",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/health")
def health():
    logger.info("Health check executado")
    app_health.set(1)
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics")
def metrics():
    logger.debug("Métricas Prometheus solicitadas")
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/error")
def error():
    logger.error("Erro simulado para testes!")
    errors_total.labels(endpoint="/error").inc()
    app_health.set(0)
    raise Exception("Erro simulado para testes!")

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Exceção capturada: {str(error)}", exc_info=True)
    errors_total.labels(endpoint="unknown").inc()
    app_health.set(0)
    return jsonify({
        "status": "error",
        "message": str(error),
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == "__main__":
    logger.info("Iniciando aplicação...")
    app_health.set(1)
    app.run(host="0.0.0.0", port=8080, debug=False)

