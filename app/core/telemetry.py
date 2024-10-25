import psutil
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
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


    # Create Meter
    # meter = metrics.get_meter(__name__)
    #
    # # Function to collect memory metrics
    # def get_memory_metrics(observer):
    #     memory = psutil.virtual_memory()
    #     observer.observe(memory.total, {"type": "total"})
    #     observer.observe(memory.available, {"type": "available"})
    #     observer.observe(memory.used, {"type": "used"})
    #     observer.observe(memory.free, {"type": "free"})
    #     observer.observe(memory.percent, {"type": "percent"})
    #
    # def get_cpu_metrics(observer):
    #     cpu_percent = psutil.cpu_percent(interval=1)
    #     observer.observe(cpu_percent, {"type": "usage"})
    #
    # # Create observable gauges
    # memory_gauge = meter.create_observable_gauge(
    #     name="system_memory",
    #     description="System memory usage metrics",
    #     unit="bytes",
    #     callbacks=[get_memory_metrics]
    # )
    #
    # cpu_gauge = meter.create_observable_gauge(
    #     name="system_cpu",
    #     description="System CPU usage metrics",
    #     unit="percent",
    #     callbacks=[get_cpu_metrics]
    # )

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
        service="suwung-database",
    )

    return trace_provider, metric_provider