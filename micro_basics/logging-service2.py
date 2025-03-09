import grpc
from concurrent import futures
import logging_pb2
import logging_pb2_grpc

logs = {}

# Реалізація сервісу LoggingService
class LoggingService(logging_pb2_grpc.LoggingServiceServicer):
    def LogMessage(self, request, context):
        if request.id in logs:
            return logging_pb2.LogResponse(status="Duplicate message ignored")
        
        logs[request.id] = request.msg
        print(f"Message logged: {request.msg}")
        return logging_pb2.LogResponse(status="Logged")

    def GetLogs(self, request, context):
        return logging_pb2.LogList(logs=list(logs.values()))

# Функція запуску GRPC-сервера
def serv():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logging_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    print("Logging service is running on port 5001...")
    server.wait_for_termination()

if __name__ == '__main__':
    serv()
