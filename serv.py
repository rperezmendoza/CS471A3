from socket import *
from helper_funcs import *
from functions import *
import sys


# ================ CHECK VALID FUNCTION ARGS ================ #
if len(sys.argv) < 2:
  print "USAGE python ", sys.argv[0], " <PORT NUMBER>"
  sys.exit()

try:
  port = int(sys.argv[1])
except:
  print "Error: please enter a valid port number"
  sys.exit()

# ==================== CREATE SERVER SOCKET ================= #

server_socket = socket(AF_INET, SOCK_STREAM)
try:
  server_socket.bind(('', port))
except Exception as e:
  print "Could not bind the server socket to the specified port number"
  print "Error: ", e
  sys.exit()
  
server_socket.listen(100)

while 1:
  
  # ========== OPEN CONTROL CONNECTION WITH CLIENT ========== #
  
  control_connection, client_address = server_socket.accept()
  print 'Control connection established with client:', client_address
  command = ""

  # ================ LISTEN FOR A NEW COMMAND =============== #

  while command != "quit":

    command = ""

    command_len = recv_msg_size(control_connection)
    command = recv_msg(control_connection, command_len)
    command_type = get_cmd_type(command)
  
    # ================ OPEN DATA CONNECTION ================= #

    data_socket = socket(AF_INET, SOCK_STREAM)
    try:
      data_socket.bind(('', 0))
    except Exception as e:
      print 'Failed to create a socket with ephemeral port'
      print 'Error:', e
      sys.exit()

    data_port = data_socket.getsockname()[1]
    send_port(control_connection, data_port)

    data_socket.listen(1)

    data_connection, data_address = data_socket.accept()

    # ==================== DO FUNCTION ====================== #
    

    # --- GET --- #
    if command_type == 'get':
      file_name = command.split()[1]
      file_size = get_file_size(file_name)
      send_msg_size(data_connection, file_size)

      if putFile(data_connection, file_name):
        print 'Sent file "', file_name, '" to client'
      

    # --- PUT --- #
    elif command_type == 'put':
      file_size = recv_msg_size(data_connection)

      if getFile(data_connection, file_size):
        print 'File received'


    # --- LS --- #
    elif command_type == 'ls':
      file_list = get_local_files()
      send_msg_size(data_connection, file_list)
      send_msg(data_connection, file_list)


    # --- LLS --- #
    elif command_type == 'lls':
      pass
      # No data transfer necessary


    # --- QUIT --- #
    elif command_type == 'quit':
      pass
      # No data transfer necessary

    # ================ CLOSE DATA CONNECTION ================ #   

    data_connection.close()

  # ================ CLOSE CONTROL CONNECTION =============== #

  control_connection.close()
  print 'Closed connection with client', client_address
  


