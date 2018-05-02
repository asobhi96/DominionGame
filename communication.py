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

def read_ack(connection):
    ack = read_message(connection)
    if ack == 'ack':
        return True
    return False
def send_ack(connection):
    send_message('ack',connection)
