from flask_opentracing import FlaskTracer
from flask import Flask, request
from jaeger_client import Config
from src.core.config import JAEGER_TYPE, JAEGER_SERVICE_NAME, JAEGER_REPORTING_HOST, JAEGER_REPORTING_PORT


def _get_jaeger_config():
    jaeger_config = {
        "sampler": {
            "type": JAEGER_TYPE,
            "param": 1,
        },
        "local_agent": {
            "reporting_host": JAEGER_REPORTING_HOST,
            "reporting_port": JAEGER_REPORTING_PORT,
        },
        "logging": True,
    }
    config = Config(
        config=jaeger_config,
        service_name=JAEGER_SERVICE_NAME,
        validate=True,
    )
    return config.initialize_tracer()


def init_trace(app: Flask):
    tracer = FlaskTracer(_get_jaeger_config, True, app=app)

    @tracer.trace()
    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        parent_span = tracer.get_span()
        parent_span.set_tag('http.request_id', request_id)
