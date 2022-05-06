import asyncio
from concurrent import futures

import grpc

from src.app import main
from src.grpc_server.stubs import auth_pb2_grpc
from src.grpc_server.utils import get_credentials
from src.services.auth_grpc import AuthServicer


async def start_server():
    app = main()
    server_key, server_cert, ca_cert = get_credentials()
    server_creds = grpc.ssl_server_credentials([(server_key, server_cert)],
                                               root_certificates=ca_cert,
                                               require_client_auth=True)
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(app), server)
    server.add_secure_port('[::]:50051', server_creds)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(start_server())
