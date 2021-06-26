# НА СТОРОНЕ КЛИЕНТА
import socket
import sys
import time

from datetime import datetime
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

sock = socket.create_connection(("127.0.0.1", 10002), timeout=4) # таймаут установки соединения
sock.settimeout(2) # таймаут на работу с сокетом

with sock:
    f = open("client_file.txt", "r", encoding="utf-8")
    while True:
        line = f.readline()
        if not line:
            break
            sock.close()
        new_line = f"{datetime.now()} : {line}"
        sock.sendall(new_line.encode("utf-8"))
        logger.info(f"Отправлена строка: {new_line}")
        time.sleep(1)



