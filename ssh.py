import json
import socket

from ssh2.session import Session                   # pylint: disable=no-name-in-module
from ssh2.error_codes import LIBSSH2_ERROR_EAGAIN  # pylint: disable=no-name-in-module
from ssh2.utils import wait_socket                 # pylint: disable=no-name-in-module


def open_session(session):
    channel = LIBSSH2_ERROR_EAGAIN
    while channel == LIBSSH2_ERROR_EAGAIN:
        channel = session.open_session()
    return channel

def get_data(channel):
    size = 1024
    chunk = []
    while size > 0:
        size, data = channel.read()
        part = data.decode()
        if part:
            chunk.append(part)
    result = ''.join(chunk)
    print(result, end='')
    return result

def wait_complete(sock, session, channel):
    data = ''
    while not is_complete(data):
        wait_socket(sock, session)
        data = get_data(channel)

def is_complete(data):
    if not data:
        return False

    data = data.replace('][', ',')
    try:
        chunk = json.loads(data)
    except json.decoder.JSONDecodeError:
        return True

    for message in chunk:
        if message['type'] == 'success' \
        or message['type'] == 'error' \
        or message['type'] == 'canceled' \
        or message['type'] == 'question':
            return True
    return False

def main():
    user = ''
    password = ''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1543))

    session = Session()
    session.handshake(sock)
    session.userauth_password(user, password)
    session.set_blocking(False)

    channel = open_session(session)
    channel.shell()

    channel.write('options set --output-format=json --show-prompt=no --notify-progress=yes\n')
    wait_complete(sock, session, channel)

    channel.write('common connect-ib\n')
    wait_complete(sock, session, channel)

    channel.write('config dump-config-to-files --dir=xml\n')
    wait_complete(sock, session, channel)

    channel.write('config dump-cfg --file=1cv8.cf\n')
    wait_complete(sock, session, channel)

    channel.write('infobase-tools dump-ib --file=1cv8.dt\n')
    wait_complete(sock, session, channel)

    channel.write('common disconnect-ib\n')
    wait_complete(sock, session, channel)

    channel.write('common shutdown\n')
    wait_complete(sock, session, channel)

    channel.send_eof()
    channel.close()
    session.disconnect()

    exit(0)

if __name__ == "__main__":
    main()