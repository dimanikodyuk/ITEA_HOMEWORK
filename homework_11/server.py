# НА СТОРОНЕ КЛИЕНТА
import socket
import sys

from logging import getLogger, StreamHandler

logger = getLogger(__name__)
stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # семейство сокета и его тип
sock.bind(("127.0.0.1", 10002)) # max port 65335
sock.listen(socket.SOMAXCONN) # слушаем хост и порт и задаём макс. количество входящих соединений
conn, addr = sock.accept() # начинаем принимать входящее клиентское соединение

conn.settimeout(5) # таймаут в секундах

f = open("server_file.txt", "a", encoding="utf-8")

with conn, sock:
    while True:
        received_data = conn.recv(1024)
        if not received_data:
            f.close()
            break
        f.writelines(received_data.decode('utf-8'))
        logger.info(f"Сервер получил данные: {received_data.decode('utf-8')}")
