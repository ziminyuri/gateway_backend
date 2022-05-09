from flask import Flask, request
from flask_opentracing import FlaskTracing
from jaeger_client import Config

config = Config(
    config={
        'sampler':
        {
            'type': 'const',
            'param': 1
        },
        'logging': True,
        'reporter_batch_size': 1
    },
    service_name="service"

)


def init_trace(app: Flask):
    jaeger_tracer = config.initialize_tracer()
    FlaskTracing(jaeger_tracer, True, app)

    @app.before_request
    def before_request():
        request.headers.get("X-Request-Id")

        # Необходимо для корректной работы recaptcha шаблона
        # request_id = request.headers.get("X-Request-Id")
        # if not request_id:
        #     raise RuntimeError('request id is required')
