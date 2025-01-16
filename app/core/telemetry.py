import psutil
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import Observation
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from fastapi import FastAPI

from app.core import logger
from app.db.session import engine


def init_telemetry(app: FastAPI, service_name: str = "suwung-service"):
    # Create resource
    resource = Resource.create({
        "service.name": service_name,
        "environment": "production"  # Can be configured from env vars
    })

    # Initialize tracing
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4317",
        insecure=True
    )
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    trace.set_tracer_provider(trace_provider)

    # Initialize metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint="http://localhost:4317",
            insecure=True
        )
    )
    metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(metric_provider)

    meter = metrics.get_meter(service_name)

    # Fungsi untuk mengumpulkan metrik memori
    def get_memory_metrics(options):  # Terima satu argumen (tidak digunakan)
        memory = psutil.virtual_memory()
        return [
            Observation(memory.total, {"type": "total"}),
            Observation(memory.available, {"type": "available"}),
            Observation(memory.used, {"type": "used"}),
            Observation(memory.free, {"type": "free"}),
            Observation(memory.percent, {"type": "percent"}),
        ]

    # Fungsi untuk mengumpulkan metrik CPU
    def get_cpu_metrics(options):  # Terima satu argumen (tidak digunakan)
        cpu_usage = psutil.cpu_percent(interval=1)
        return [Observation(cpu_usage, {"type": "usage"})]

    # Register observable gauges
    meter.create_observable_gauge(
        name="system_memory",
        description="Metrics untuk penggunaan memori sistem",
        unit="bytes",
        callbacks=[get_memory_metrics]
    )

    meter.create_observable_gauge(
        name="system_cpu",
        description="Metrics untuk penggunaan CPU sistem",
        unit="percent",
        callbacks=[get_cpu_metrics]
    )

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
        service="suwung-database",
    )

    return trace_provider, metric_provider