import socket
import threading
from queue import Queue
from common_ports import ports_and_services


# GENERAL PORT SCAN FUNCTION
def portscan(target, port):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)      
    sock.connect((target, port))
    sock.close()
    return True
  except:
    sock.close()
    return False
  

# FUNCTION IF VERBOSE IS SET TO 'TRUE'
def verboseResponse(hostAddr, hostName, ports=[]):  
  
  # CONFIGURE HEADER BASED ON PRESENCE OF VALID HOST NAME
  if hostName:
    header1 = "Open ports for {} ({})".format(hostName[0], hostAddr)
  else:
    header1 = "Open ports for {}".format(hostAddr)

  header2 = f"PORT     SERVICE\n"
  for index, port in enumerate(ports):
    serviceRef = ports_and_services[port]
    header2 += str(port).ljust(4) + "     " + serviceRef
    if len(ports) != 1 and len(ports) != index + 1 : header2 += "\n"

  return f"{header1}\n{header2}"


# MULTI-THREAD FUNCTION TO REDUCE RUN-TIME
def multiThreadPortScan(target, port_list, threads):
  queue = Queue()
  open_ports = []
#  print("M/T port list: ", port_list)

  def fill_queue(port_list):
    for port in port_list:
      queue.put(port)

  def worker():
#    print("Filled queue: ", queue.qsize())
    while not queue.empty():
      port = queue.get()
      if portscan(target, port):
      #  print("Port {} is Open!".format(port))
        open_ports.append(port)
      #  print("Worker open_ports:", open_ports)
        
  fill_queue(port_list)

  thread_list = []

  for t in range(threads):
      thread = threading.Thread(target=worker)
      thread_list.append(thread)

  for thread in thread_list:
      thread.start()

  for thread in thread_list:
      thread.join()
  
#  print("Function final open_ports:", open_ports)

  return open_ports


# MAIN FUNCTION - 'GET_OPEN_PORTS'
def get_open_ports(target, port_range, verbose=False):
#  queue = Queue()
  open_ports = []
  start= port_range[0]
  stop = port_range[1] + 1
  port_list = range(start, stop)
#  print('target:', target, "start_port", start, "stop_port:", stop)

  # ******  Check For Valid target   ******
  try:
    hostAddr = socket.gethostbyname(target)
  #  print("target ip_addr: ", hostAddr)
  except:
    if target[0].isdigit() and target[1].isdigit():
      return 'Error: Invalid IP address'
    else: 
      return 'Error: Invalid hostname'

  try:
    hostName = socket.gethostbyaddr(target)    
  except:
    hostName = None    

  """
#  hostByName = target 
  if hostName:
    print("host URL Name: ", hostName[0],"\n", "host address: ", hostAddr)
  else:
    print("host URL Name: ", hostName,"\n", "host address: ", hostAddr)
  """

# ****  SET # THREADS, CALL MULTI-THREAD FUNCTION  *****
  threads = 10
  open_ports = multiThreadPortScan(target, port_list, threads)
  

#  print("Call M/T function:", multiThreadPortScan(target, port_list))
#  print("M/T function return: ", open_ports)


  if verbose: return verboseResponse(hostAddr, hostName, open_ports)
#  print("Get function final: ", open_ports)

  return(open_ports)

"""
 ***** ORIGINAL UNTHREADED PORT SCANNER CODE -- WORKS   *****
 RUN TIME = 92.7 secs.

  stop = stop + 1
  for port in range(start, stop):
    port = int(port)
    result = portscan(target, port)
    if result:
        open_ports.append(port)
        print("Port {} is Open".format(port))
"""

"""
  ***** MULTI-THREADING TEST CODE   *****

    # THREADS       RUN TIME 
                    (secs.)
        2             51.48
        3             39.3
        5             24.37
        8             24.20
        9             24.11, 24.1
        10            18.3, 18.6   
        30            18.2
        50            18.1
        100           18.2
        200           18.2
        500           18.3
        900           18.3



"""

  

  
