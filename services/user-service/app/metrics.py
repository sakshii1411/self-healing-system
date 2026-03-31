from prometheus_client import Counter, Histogram, Gauge
import time

# Golden Signals Metrics
REQUEST_COUNT = Counter(
    'user_service_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'user_service_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'user_service_errors_total',
    'Total number of errors',
    ['type']
)

# Simulated resource metrics
CPU_USAGE = Gauge('user_service_cpu_usage_percent', 'Simulated CPU usage')
MEMORY_USAGE = Gauge('user_service_memory_usage_bytes', 'Simulated memory usage')
