from __future__ import annotations

from argparse import ArgumentParser
# from email.mime.text import MIMEText
from queue import Queue
import socket
from socketserver import ThreadingTCPServer, BaseRequestHandler
from threading import Thread

import tomli


def student_id() -> int:
    return 12012423 # TODO: replace with your SID


parser = ArgumentParser()
parser.add_argument('--name', '-n', type=str, required=True)
parser.add_argument('--smtp', '-s', type=int)
parser.add_argument('--pop', '-p', type=int)

args = parser.parse_args()
with open('data/config.toml', 'rb') as f:
    _config = tomli.load(f)
    SMTP_PORT = args.smtp or int(_config['server'][args.name]['smtp'])
    POP_PORT = args.pop or int(_config['server'][args.name]['pop'])
    ACCOUNTS = _config['accounts'][args.name]
    MAILBOXES = {account: [] for account in ACCOUNTS.keys()}

with open('data/fdns.toml', 'rb') as f:
    FDNS = tomli.load(f)

ThreadingTCPServer.allow_reuse_address = True


def fdns_query(domain: str, type_: str) -> str | None:
    domain = domain.rstrip('.') + '.'
    return FDNS[type_][domain]


class POP3Server(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.user = None
        self.authenticated = False
        self.deleted_emails = set()
        super().__init__(*args, **kwargs)

    def handle(self):
        conn = self.request
        conn.sendall(b'+OK POP3 server ready\r\n')

        while True:
            data = conn.recv(1024).decode().strip()
            print(data)
            if len(data) == 0:  # 如果接收到空数据，表示连接已关闭
                break

            if data.startswith('USER '):
                self.handle_user(data, conn)
            elif data.startswith('PASS '):
                self.handle_pass(data, conn)
            elif data == 'STAT':
                print(12)
                self.handle_stat(conn)
            elif data.startswith('LIST ') and data.split()[1].isdigit():
                self.handle_list1(data, conn)
            elif data == 'LIST':
                self.handle_list(conn)
            # elif data.startswith('LIST ') and data.split()[1].isdigit():
            #     self.handle_list1(data, conn)
            elif data.startswith('RETR ') and data.split()[1].isdigit():
                print(13)
                self.handle_retr(data, conn)
            elif data.startswith('DELE ') and data.split()[1].isdigit():
                self.handle_dele(data, conn)
            elif data == 'RSET':
                self.handle_rset(conn)
            elif data == 'NOOP':
                self.handle_noop(conn)
            elif data == 'QUIT':
                self.handle_quit(conn)
                break
            else:
                conn.sendall(b'-ERR Invalid command\r\n')

    def handle_user(self, command, conn):
        username = command.split()[1]
        if username in ACCOUNTS:
            self.user = username
            conn.sendall(b'+OK User accepted\r\n')
        else:
            conn.sendall(b'-ERR Invalid user\r\n')

    def handle_pass(self, command, conn):
        if self.user is None:
            conn.sendall(b'-ERR User not specified\r\n')
        elif not self.authenticated:
            password = command.split()[1]
            if ACCOUNTS[self.user] == password:
                self.authenticated = True
                conn.sendall(b'+OK User successfully authenticated\r\n')
            else:
                conn.sendall(b'-ERR Invalid password\r\n')
        else:
            conn.sendall(b'-ERR User already authenticated\r\n')

    def handle_stat(self, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            num_emails = len(MAILBOXES[self.user])
            total_bytes = sum(len(email) for email in MAILBOXES[self.user])
            conn.sendall(b'+OK %d %d\r\n' % (num_emails, total_bytes))

    def handle_list(self, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            response = b'+OK\r\n'
            for i, email in enumerate(MAILBOXES[self.user], start=1):
                if i not in self.deleted_emails:
                    response += b'%d %d\r\n' % (i, len(email))
            response += b'.\r\n'
            conn.sendall(response)

    def handle_list1(self, command,conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            email_index = int(command.split()[1])
            if email_index in self.deleted_emails:
                conn.sendall(b'-ERR Email has been marked as deleted\r\n')
            elif 1 <= email_index <= len(MAILBOXES[self.user]):
                email = MAILBOXES[self.user][email_index - 1]
                response = b'%d %d\r\n.\r\n' % (email_index, len(email))
                conn.sendall(response)
            else:
                conn.sendall(b'-ERR \r\n')


    def handle_retr(self, command, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            email_index = int(command.split()[1])
            if email_index in self.deleted_emails:
                conn.sendall(b'-ERR Email has been marked as deleted\r\n')
            elif 1 <= email_index <= len(MAILBOXES[self.user]):
                email = MAILBOXES[self.user][email_index - 1]
                print(email)
                conn.sendall(b'+OK %d %s' % (len(email), email))
            else:
                conn.sendall(b'-ERR \r\n')

    def handle_dele(self, command, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:

            email_index = int(command.split()[1])
            print( email_index)
            if email_index in self.deleted_emails or email_index <= 0 or email_index > len(MAILBOXES[self.user]):
                conn.sendall(b'-ERR \r\n')
            else:
                self.deleted_emails.add(email_index)
                conn.sendall(b'+OK \r\n')

    def handle_rset(self, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            self.deleted_emails.clear()
            conn.sendall(b'+OK reset\r\n')

    def handle_noop(self, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            conn.sendall(b'+OK\r\n')

    def handle_quit(self, conn):
        if not self.authenticated:
            conn.sendall(b'-ERR User not authenticated\r\n')
        else:
            for email_index in self.deleted_emails:
                del MAILBOXES[self.user][email_index - 1]
            conn.sendall(b'+OK Bye\r\n')


class SMTPServer(BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall(b'220 localhost Simple Mail Transfer Service Ready\r\n')
        sender = None
        receivers = []
        data = b''
        print(SMTP_PORT)
        while True:
            command = conn.recv(1024).decode().strip()
            if command.startswith('helo') or command.startswith('ehlo'):
                # Handle HELO command
                conn.sendall(b'250 \r\n')

            elif command.startswith('mail'):
                # Handle MAIL command
                sender = command.split(':')[1].strip()[1:-1]
                conn.sendall(b'250 OK\r\n')
            elif command.startswith('rcpt'):
                # Handle RCPT command
                receiver = command.split(':')[1].strip()[1:-1]
                receivers.append(receiver)
                conn.sendall(b'250 OK\r\n')

            elif command == 'data':
                # Handle DATA command
                conn.sendall(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')
                data = conn.recv(1024)
                while not data.endswith(b'\r\n.\r\n'):
                    data += conn.recv(1024)
                conn.sendall(b'250 OK\r\n')

            elif command == 'quit':
                # Handle QUIT command
                conn.sendall(b'221 Bye\r\n')
                break

        # Store the email in the correct mailbox or forward it to the recipient's server
        for receiver in receivers:
            receiver_domain = receiver.split('@')[1]
            print(receiver_domain)
            print(args.name)
            tmp = None
            if args.name == 'exmail.qq.com':
                tmp = 'mail.sustech.edu.cn'
            else:
                tmp = args.name
            if receiver_domain == tmp :
                MAILBOXES[receiver].append(data)
                print('sdfsdfsdf')
            else:
                print('ttt')
                server_ip = receiver_domain
                print("server_ip: "+server_ip)
                if(SMTP_PORT == 1125):
                    TP = 2125
                else:
                    TP = 1125
                receiver_server = ('localhost', TP)
                print(receiver_server)
                with socket.create_connection(receiver_server) as s:
                    s.sendall(b'HELO\r\n')
                    dd = s.recv(1024)
                    print(dd)
                    print(0)
                    s.sendall(b'helo\r\n')
                    dd = s.recv(1024)
                    print(dd)
                    print(1)
                    s.sendall(f'mail from:<{sender}>\r\n'.encode())
                    dd = s.recv(1024)
                    print(dd)
                    print(2)
                    s.sendall(f'rcpt to:<{receiver}>\r\n'.encode())
                    dd = s.recv(1024)
                    print(dd)
                    print(3)
                    s.sendall(b'data\r\n')
                    dd = s.recv(1024)
                    print(dd)
                    print(4)
                    s.sendall(data)
                    dd = s.recv(1024)
                    print(dd)
                    print(5)
                    s.sendall(b'quit\r\n')
                    dd = s.recv(1024)
                    print(dd)
                    print(6)
        conn.close()


if __name__ == '__main__':
    if student_id() % 10000 == 0:
        raise ValueError('Invalid student ID')

    smtp_server = ThreadingTCPServer(('', SMTP_PORT), SMTPServer)
    pop_server = ThreadingTCPServer(('', POP_PORT), POP3Server)
    Thread(target=smtp_server.serve_forever).start()
    Thread(target=pop_server.serve_forever).start()
