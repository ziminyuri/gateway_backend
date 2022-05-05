import asyncio
from concurrent import futures

import grpc

from src.app import main
from src.grpc_server.stubs import auth_pb2_grpc
from src.services.auth_grpc import AuthServicer


async def start_server():
    app = main()
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(app), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(start_server())
