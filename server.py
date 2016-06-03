import Queue
import threading

import sys

import tcp

port = 2000
addr_to_id = {('52.37.112.251', port): 0, ('52.40.128.229', port): 1, ('52.41.5.151', port): 2}
id_to_addr = {0: ('52.37.112.251', port), 1: ('52.40.128.229', port), 2: ('52.41.5.151', port)}
host_to_id = {'52.37.112.251': 0, '52.40.128.229': 1, '52.41.5.151': 2}
id_to_host = {0: '52.37.112.251', 1: '52.40.128.229', 2: '52.41.5.151'}



def start_server(port=80, id=None):
    queue = Queue.Queue()
    server = Server(queue, port, id)
    server.start()
    return queue


def addr_to_tuple(addr):
    tuple = (addr, port)
    return tuple


class Server(threading.Thread):

    def __init__(self, queue, port, id):
        self.port = port
        self.id = id
        self.queue = queue
        self.role = 'follower'
        self.channel = tcp.Network(port, id)
        self.channel.start()
        self.leader = None
        self.connected_peers = []
        threading.Thread.__init__(self)

    def run(self):

        self.running = True
        while self.running:
            for peer in list(addr_to_id.keys()):
                # if peer not in self.connected_peers and not addr_to_id[peer] == id:
                if peer not in self.channel and not host_to_id[peer[0]] == id:
                    connected = self.channel.connect(peer)
                    if connected:
                        print str("Server: Connected to "+peer[0])
                        self.connected_peers.append(peer)
                    # print "Connected: ", connected
                message = self.channel.receive(4.0)
                if message:
                    for addr, msg in message:
                        self.process_msg(addr, msg)
                else:
                    msg = 'hearbeat from' + str(id)
                    for peer in self.connected_peers:
                        self.channel.send(msg, id=host_to_id[peer[0]])
                        print "sent msg to", peer[0]

    def process_msg(self, addr, msg):
        print "MSG: ", msg

id = int(sys.argv[1])
start_server(port=2000, id=id)




