from prometheus_client import Counter, Histogram, Gauge

# Golden Signals for order-service
REQUEST_COUNT = Counter(
    'order_service_requests_total',
    'Total number of requests to order service',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'order_service_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'order_service_errors_total',
    'Total number of errors',
    ['type']
)

# Downstream dependency metrics
DOWNSTREAM_CALLS = Counter(
    'order_service_downstream_calls_total',
    'Calls made to other services',
    ['target_service', 'status']
)

DOWNSTREAM_LATENCY = Histogram(
    'order_service_downstream_latency_seconds',
    'Latency of calls to downstream services',
    ['target_service']
)

CPU_USAGE = Gauge('order_service_cpu_usage_percent', 'Simulated CPU usage')
MEMORY_USAGE = Gauge('order_service_memory_usage_bytes', 'Simulated memory usage')
