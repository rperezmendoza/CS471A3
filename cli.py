from socket import *
from helper_funcs import *
from functions import *
import sys


# ================== CHECK VALID FUNCTION ARGS ================= #

if len(sys.argv) < 3:
  print "USAGE python cli.py ", sys.argv[0], " <server machine> <server port>"
  sys.exit()

server_name = sys.argv[1]
try:
  server_port = int(sys.argv[2])
except:
  print "Error: please enter a valid server port number"
  sys.exit()

# ==========  OPEN CONTROL CONNECTION WITH SERVER ============= #

try:
  control_connection = socket(AF_INET, SOCK_STREAM)
  control_connection.connect((server_name, server_port))
except Exception as e:
  print "Could not connect to the specified server"
  print "Error: ", e
  sys.exit()

print 'Established control connection with server:', (server_name, server_port)

command = ""

while command != "quit":

  # ==================== SEND COMMAND ==================== #
  command = raw_input('ftp> ')
  command_type = get_cmd_type(command)

  if invalid_cmd( command_type ):
    print "'", command_type, "' : command not found"
    continue

  send_msg_size(control_connection, command)
  send_msg(control_connection, command)

  # ================ OPEN DATA CONNECTION ================ #
  
  data_port = recv_port(control_connection)
  try:
    data_connection = socket(AF_INET, SOCK_STREAM)
    data_connection.connect((server_name, data_port))
  except Exception as e:
    print 'Could not establish data connection with server'
    print 'Error:', e
    sys.exit()

  # ==================== DO FUNCTION ===================== #
 
  # --- GET --- #
  if command_type == 'get':
    file_size = recv_msg_size(data_connection)

    if getFile(data_connection, file_size):
      print '   > File sucessfully copied'


  # --- PUT --- #
  elif command_type == 'put':
    file_name = command.split()[1]
    file_size = get_file_size(file_name)
    send_msg_size(data_connection, file_size)

    if putFile(data_connection, file_name):
      print '   > File successfully sent to server'


  # --- LS --- #
  elif command_type == 'ls':
    msg_size = recv_msg_size(data_connection)
    file_list = recv_msg(data_connection, msg_size)
    print file_list


  # --- LLS --- #
  elif command_type == 'lls':
    print get_local_files()


  # --- QUIT --- #
  elif command_type == 'quit':
    pass


  # =============== CLOSE DATA CONNECTION =============== #

  data_connection.close()

# ============== CLOSE CONTROL CONNECTION =============== #

control_connection.close()
print 'Control connection with', (server_name, server_port), 'closed'
