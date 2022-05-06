from flask_opentracing import FlaskTracer
from flask import Flask
from jaeger_client import Config


def _get_jaeger_config():
    jaeger_config = {
        "sampler": {
            "type": settings.JAEGER.JAEGER_TYPE,
            "param": 1,
        },
        "local_agent": {
            "reporting_host": settings.JAEGER.REPORTING_HOST,
            "reporting_port": settings.JAEGER.REPORTING_PORT,
        },
        "logging": True,
    }
    config = Config(
        config=jaeger_config,
        service_name=settings.JAEGER.SERVICE_NAME,
        validate=True,
    )


def init_trace(app: Flask):
    tracer = FlaskTracer(_get_jaeger_config, True, app=app)