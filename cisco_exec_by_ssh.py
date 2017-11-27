import paramiko
import sys
import os
import time
import re


class CiscoExecBySSH:
    def __init__(self):
        self.input_file = self.get_input_file()
        self.login_params = {'host': '', 'user': '', 'password': '', 'port': 22}
        self.get_login_info()
        self.client = self.login()

    def get_login_info(self):
        host, user, password = self.input_file.readline().strip().split(',')
        self.login_params['host'] = host
        self.login_params['user'] = user
        self.login_params['password'] = password

    def login(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.login_params['host'], username=self.login_params['user'],
                       password=self.login_params['password'], port=self.login_params['port'],
                       look_for_keys=False, allow_agent=False)
        return client

    def exec_commands(self):
        buffer = 2048
        delay = 1
        channel = self.client.invoke_shell()
        self._print_channel_output(channel.recv(buffer))
        channel.send(self.login_params['user'] + '\n')
        channel.send(self.login_params['password'] + '\n')
        self._print_channel_output(channel.recv(buffer))
        for command in self.input_file:
            channel.send(command)
            time.sleep(delay)
            output = channel.recv(buffer)
            if re.search('\(y/n\)', output.decode(), re.IGNORECASE):
                channel.send('y')
                time.sleep(delay)
                self._print_channel_output(output)
                output = channel.recv(buffer)
            self._print_channel_output(output)
        time.sleep(delay)
        channel.close()
        self.client.close()

    @staticmethod
    def _print_channel_output(output):
        print(output.decode(), end='')

    @staticmethod
    def get_input_file():
        try:
            input_file_path = sys.argv[1]
            if not os.path.isfile(input_file_path):
                print('No such file {}'.format(input_file_path))
                sys.exit(1)
            return open(input_file_path)
        except IndexError:
            print('Please enter input file')
            print('python3 <scrip name>.py <input file>')
            sys.exit(1)


CiscoExecBySSH().exec_commands()
