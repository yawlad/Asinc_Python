from socket import *
from datetime import datetime
import sys
import argparse
import threading
import time

from common.constants import *
from common.utils import *
from Exeptions import *

from decorators import log

import logs.client_log_config
CLIENT_LOGGER = logging.getLogger('client')


class Client():

    def __init__(self, server_address = DEFAULT_IP_ADDRESS, server_port = DEFAULT_PORT, logger = CLIENT_LOGGER, name = None):
        self.logger = logger
        
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-n', '--name', default=None, nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        self.server_address = namespace.addr
        self.server_port = namespace.port
        self.client_name = namespace.name
        
        if not 1023 < server_port < 65536:
            self.critical(f'Undefined port (must be in range from 1024 to 65535): {self.server_port}.')
            sys.exit(1) 

    @log
    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.client_name
        }


    @log
    def make_presense(self):

        self.logger.debug(f'Created {PRESENCE}-message for {self.client_name}')

        return {
            ACTION: PRESENCE,
            TIME: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: self.client_name,
                STATUS: HERE
            }
        }

    @log
    def create_message(self):
        to_user = input('Enter the destination: ')
        message = input('Enter your message: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        self.logger.debug(f'Created message-dict: {message_dict}')
        try:
            send_message(self.socket, message_dict)
            self.logger.info(f'Your message has been sent {to_user}')
        except:
            self.logger.critical('Connection lost.')
            sys.exit(1)
    
    @log
    def message_from_server(self):
        while True:
            try:
                message = get_message(self.socket)
                if ACTION in message and message[ACTION] == MESSAGE and  SENDER in message and DESTINATION in message and MESSAGE_TEXT in message and message[DESTINATION] == self.client_name:
                    print(f'\nGet message from {message[SENDER]}: \n{message[MESSAGE_TEXT]}')
                    self.logger.info(f'Get message from {message[SENDER]}: \n{message[MESSAGE_TEXT]}')
                else:
                    self.logger.error(f'Get bad message from server: {message}')
            except IncorrectDataRecivedError:
                self.logger.error(f'Cannnot decode the message')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                self.logger.critical(f'Connection lost.')
                break
    
    @log
    def process_ans(self, response):

        self.logger.debug(f'Processing response from server: {response}')

        if RESPONSE in response:
            if response[RESPONSE] == 200:
                return f'Response code: {response[RESPONSE]}\nAlert: {response[ALERT]}'
            return f'Response code: {response[RESPONSE]}\nError: {response[ERROR]}'
        raise Exception

    @log
    def user_interactive(self):
        while True:
            command = input('Input command: ')
            if command == 'message':
                self.create_message()
            elif command == 'exit':
                send_message(socket, self.create_exit_message(self.client_name))
                print('Disconnecting...')
                self.logger.info('Disconnected.')
                time.sleep(1)
                break
            else:
                print('Bad Command')
        
    def connect(self):   
        
        print('CLIENT STARTING...')

        if not self.client_name:
            self.client_name = input('Enter your nickname: ')

        self.logger.info(
            f'Client started: server adress: {self.server_address}, '
            f'port: {self.server_port}, client name: {self.client_name}')
        
         
        try:
            
            self.logger.info(
                f'Trying to connect to {self.server_address}:{self.server_port}.')
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.server_address, self.server_port))
            self.logger.info(
                f'Successfully connected to {self.server_address}:{self.server_port}.')
            request_to_server = self.make_presense()
            send_message(self.socket, request_to_server)
        except ConnectionRefusedError:
            self.logger.error(
                f'Connection refused: {self.server_address}:{self.server_port}')
            sys.exit(1)
        except Exception as error:
            self.logger.error(f'Connection error: {error}:{self.server_port}')
            sys.exit(1)
            
        else: 
            receiver = threading.Thread(target=self.message_from_server)
            receiver.daemon = True
            receiver.start()

            user_interface = threading.Thread(target=self.user_interactive)
            user_interface.daemon = True
            user_interface.start()
            self.logger.debug('Procceses started')

            while True:
                time.sleep(1)
                if receiver.is_alive() and user_interface.is_alive():
                    continue
                break



if __name__ == '__main__':
    cl = Client()
    cl.connect()
