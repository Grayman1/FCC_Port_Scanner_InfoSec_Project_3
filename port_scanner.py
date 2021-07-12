import socket
import threading
from queue import Queue
from common_ports import ports_and_services
# import common_ports

# Scan Ports
def portscan(target, port):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)      
    sock.connect((target, port))
    sock.close()
    return True
  except:
    return False
  sock.close()

# Function if verbose is True
def verboseResponse(target, ports=[]):
  try:
    hostByAddr = socket.gethostbyaddr(target)
  except:
    hostByAddr = None

  hostByName = target 
#  print("hostByAddr: ", hostByAddr, "hostByName: ", hostByName)
  
  if hostByAddr:
    header1 = "Open Ports for {} ({})".format(hostByAddr, hostByName)
  else:
    header1 = "Open Ports for {}".format(hostByName)

  header2 = f"PORT     SERVICE\n"
  for index, port in enumerate(ports):
    serviceRef = ports_and_services[port]
    header2 += str(port).ljust(4) + "     " + serviceRef
    if len(ports) != 1 and len(ports) != index + 1 : header2 += "\n"

  return f"{header1}\n{header2}"


def get_open_ports(target, port_range, verbose=False):
  queue = Queue()
  open_ports = []
  start= port_range[0]
  stop = port_range[1]
  port_list = range(start, stop)
#  print('target:', target, "start_port", start, "stop_port:", stop)

#  start, stop = port_range

  # ******  Check For Valid target   ******
  try:
    socket.getaddrinfo(target, port_range[0])
  except:
    if target[0].isdigit() and target[1].isdigit():
      return 'Error: Invalid IP address'
    else: 
      return 'Error: Invalid hostname'

  #Get Hostname or address
  if target[0].isdigit() and target[1].isdigit():
    hostByAddr = target

  stop = stop + 1
  for port in range(start, stop):
    port = int(port)
    result = portscan(target, port)
    if result:
        open_ports.append(port)
        print("Port {} is Open".format(port))
  
  if verbose: return verboseResponse(target, open_ports)

#  print(type(open_ports))
  return(open_ports)

"""
  def fill_queue(port_list):
    for port in port_list:
      queue.put(port)
  
  def worker():
    while not queue.empty():
      port = queue.get()
      if portscan(port):
#        print("Port {} is Open!".format(port))
        open_ports.append(port)

  fill_queue(port_list)  
  thread_list = []

  for t in range(100):
    thread = threading.Thread(target = worker)
    thread_list.append(thread)

  for thread in thread_list:
    thread.start()

  for thread in thread_list:
    thread.join()
"""
#  print("Open ports are: ", open_ports)



  


"""
def get_open_ports(target, port_range, verbose=False):
  open_ports = []
  queue = Queue()
  start, stop = port_range

  def portscan(port):
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((target, port))
      return True
    except:
      return False

  def fill_queue(port_list):
    for port in port_list:
      queue.put(port)

  def worker():
    while not queue.empty():
      port = queue.get()
      if portscan(port):
        print("Port {} is Open!".format(port))
        open_ports.append(port)
  
  port_list = range(start, stop)
  fill_queue(port_list)

  thread_list = []

  for t in range(100):
    thread = threading.Thread(target = worker)
    thread_list.append(thread)

  for thread in thread_list:
    thread.start()

  for thread in thread_list:
    thread.join()

  print("Open ports are: ", open_ports)


  print(type(open_ports[0]))
  return(open_ports)
"""

"""
KPWorthi
port_dict = common_ports.ports_and_services

def get_open_ports(target, port_range, verb = False):
    open_ports = []
    port_string, hostByAddr, hostByName = ("", "", "")
    start, stop = port_range

    #checking validity of 'target' with first port in range
    try: socket.getaddrinfo(target, port_range[0])
    except:
      if target[0].isdigit() and target[1].isdigit(): return 'Error: Invalid IP address'
      else: return 'Error: Invalid hostname'

    #getting host name/address for verbose
    if target[0].isdigit() and target[1].isdigit() and verb:
      hostByAddr = target
      try: hostByName = socket.gethostbyaddr(target)[0]
      except: hostByName = None
    elif verb:
      hostByAddr = socket.gethostbyname(target)
      hostByName = target    

    def portCheck(host, port):
      testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      testSocket.settimeout(0.2)
      if testSocket.connect_ex((target, port)):
        #print('Port', port, 'closed.')
        testSocket.close()
        return False
      else:
        #print('Port', port, 'open.')
        testSocket.close()
        return True


    for port in range(start,stop+1):
      if portCheck(target, port):
        open_ports.append(port)

    if verb:
      if hostByName is not None: port_string = 'Open ports for ' + hostByName + ' (' + hostByAddr + ')\n'
      else: port_string = 'Open ports for ' + hostByAddr + "\n"
      port_string += 'PORT     SERVICE'
      for port in open_ports:
        #add spaces to end of port as string due
        #to format the supplied testing expects
        port = str(port)
        while len(port) < 4: port += " "
        port_string += "\n" + port + "     " + port_dict[int(port)]
      return port_string

    else: return open_ports
"""