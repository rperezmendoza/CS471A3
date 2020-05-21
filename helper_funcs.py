import sys

'''
  Given a complete command, return the function portion of the command
  e.g if command = "get data.txt" return "get"
'''
def get_cmd_type(input):
  return input.split()[0]

'''
  Determine if the given command is defined
'''
def invalid_cmd(input):
  all_cmds = ['get', 'put', 'ls', 'lls', 'quit']
  return input not in all_cmds

'''
  Tell receiver the size of the message I am about to send
  Send a 10 byte string containing the size of the message in bytes
'''
def send_msg_size(socket, msg):
  size_str = ''
  if type(msg) is str:
    size = len(msg)
    size_str = str(size).zfill(10)
  elif type(msg) is int:
    size_str = str(msg).zfill(10)

  bytes_sent = 0
  while bytes_sent != 10:
    bytes_sent += socket.send(size_str[bytes_sent:])

'''
  Send the port number to the receiver
  Send as a 10 byte string
'''
def send_port(socket, port):
  port_str = str(port).zfill(10)
  bytes_sent = 0
  while bytes_sent != 10:
    bytes_sent += socket.send(port_str)

'''
  Receive information about the size of the message the sender is about to send
  Receive a 10 byte string with the size of the message, and return the size
  as an int
'''
def recv_msg_size(socket):
  size_str = ''
  while len(size_str) != 10:
    buff = socket.recv(10)
    if not buff:
      print 'Connection closed unexpectedy when waiting for message size'
      sys.exit()
    size_str += buff
  size = int(size_str)
  return size

'''
  Receive a port number from the sender
  Receive a 10 byte string and return as an int
'''
def recv_port(socket):
  port_str = ''
  while len(port_str) != 10:
    buff = socket.recv(10)
    if not buff:
      print 'Connection closed unexpectedy when waiting for port number'
      sys.exit()
    port_str += buff
  port = int(port_str)
  return port

'''
  Send all the bytes in a string to the receiver
'''
def send_msg(socket, msg):
  bytes_sent = 0
  while bytes_sent != len(msg):
    bytes_sent += socket.send( msg[bytes_sent:] )


'''
  Receive a message with the specified byte size
  Return the message as a string
'''
def recv_msg(socket, size):
  msg = ''
  while len(msg) != size:
    buff = socket.recv(size)
    if not buff:
      print 'Connection closed unexpectedly when waiting for message'
      sys.exit()
    msg += buff
  
  return msg

