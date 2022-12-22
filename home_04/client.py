from socket import *
from datetime import datetime
import sys

from common.constants import *
from common.utils import *


def make_presense(account_name='Guest'):
    return {
        ACTION: PRESENCE,
        TIME: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        TYPE: STATUS,
        USER: {
            ACCOUNT_NAME: account_name,
            STATUS: HERE
        }
    }

def process_ans(response):
    
    if RESPONSE in response:
        if response[RESPONSE] == 200:
            return f'Response code: {response[RESPONSE]}\nAlert: {response[ALERT]}'
        return f'Response code: {response[RESPONSE]}\nError: {response[ERROR]}'
    raise Exception

def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Enter the value of port (-p) in range from 1024 to 65535')
        sys.exit(1)
        
    socket_ = socket(AF_INET, SOCK_STREAM)
    socket_.connect((server_address, server_port))
    request_to_server = make_presense()
    send_message(socket_, request_to_server)
    try:
        responce = process_ans(get_message(socket_))
        print(responce)
    except Exception as error:
        print(f'Decoding error --- {error}')


if __name__ == '__main__':
    main()
