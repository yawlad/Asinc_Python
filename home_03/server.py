from socket import *
import sys

from common.constants import *
from common.utils import *


def process_client_request(request):

    if ACTION in request and request[ACTION] == PRESENCE and TIME in request and USER in request and request[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200,
                ALERT: 'Connected'}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise Exception
    except IndexError:
        print('Enter the value of port (-p) in range from 1024 to 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except Exception:
        print('Enter the value of adress (-a)')
        sys.exit(1)

    socket_ = socket(AF_INET, SOCK_STREAM)
    socket_.bind((listen_address, listen_port))

    socket_.listen(MAX_CONNECTIONS)
    
    while True:
        client, client_address = socket_.accept()
        try:
            request_from_client = get_message(client)
            print(
                f'Connected: {client_address} as {request_from_client[USER][ACCOUNT_NAME]}')
            response = process_client_request(request_from_client)
            send_message(client, response)
            client.close()
        except Exception as error:
            print(f'Bad request --- {error}')
            client.close()


if __name__ == '__main__':
    main()
