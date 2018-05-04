"""
Methods to communicate between host and clients for Dominion Game
"""
def send_message(message,connection):
    msg_length = len(message)
    new_messsage = msg_length.to_bytes(length=2,byteorder='big') + message.encode('ascii')
    connection.sendall(new_messsage)

def read_message(connection):
    msg_length = int.from_bytes(connection.recv(2),'big')
    return connection.recv(msg_length).decode('ascii')

def send_print_command(message,connection):
    send_message('0'+ message,connection)

def send_input_command(connection):
    send_message('1',connection)

def print_and_send_command(message,connection):
    send_print_command(message,connection)
    send_input_command(connection)
    return read_message(connection)

def send_kill_command(connection):
    send_message('2',connection)

def read_command(connection):
    message = read_message(connection)
    return message[0], message[1:]

