#!/usr/bin/env -S python3 -u

import argparse, socket, time, json, select, struct, sys, math

class Table_entry:
    ASPath = []

    def __init__(self, AS, ASPath, localpref, selfOrigin, origin):
        self.ASPath = [AS] + ASPath
        self.localpref = localpref
        self.selfOrigin = selfOrigin
        self.origin = origin

class Router:

    relations = {}
    sockets = {}
    ports = {}
    update_record = []
    withdraw_record = []

    def __init__(self, asn, connections):
        print("Router at AS %s starting up" % asn)
        self.asn = asn
        for relationship in connections:
            port, neighbor, relation = relationship.split("-")

            self.sockets[neighbor] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sockets[neighbor].bind(('localhost', 0)) #Port 0 triggers OS to automatically return a suitable available port
            self.ports[neighbor] = int(port)
            self.relations[neighbor] = relation
            self.send(neighbor, json.dumps({ "type": "handshake", "src": self.our_addr(neighbor), "dst": neighbor, "msg": {}  }))

    def our_addr(self, dst):
        quads = list(int(qdn) for qdn in dst.split('.'))
        quads[3] = 1
        return "%d.%d.%d.%d" % (quads[0], quads[1], quads[2], quads[3])

    def send(self, network, message):
        self.sockets[network].sendto(message.encode('utf-8'), ('localhost', self.ports[network]))

    def run(self):
        while True:
            socks = select.select(self.sockets.values(), [], [], 0.1)[0]
            for conn in socks:
                k, addr = conn.recvfrom(65535)
                print("k: %s, addr: %s" % (k, addr))
                srcif = None
                for sock in self.sockets:
                    if self.sockets[sock] == conn:
                        srcif = sock
                        break
                msg = k.decode('utf-8')

                print("Received message '%s' from %s" % (msg, srcif))
                
                self.parse_json(self, msg)
        return

    def hardcode_temp(self):
        self.send()

    def parse_json(self, msg):
        payload_dict = json.loads(msg)

        if payload_dict['type'] == 'update':
            self.handle_update(self, payload_dict)
        if payload_dict['type'] == 'handshake':
            self.handle_handshake(self, payload_dict)
        if payload_dict['type'] == 'withdraw':
            self.handle_withdraw(self, payload_dict)
        else:
            raise Exception("Message type %s is not handled" % payload_dict['type'])

    def handle_update(self, payload_dict):
        self.update_record.append(payload_dict)
        src_ip = payload_dict['src']
        dst_ip = payload_dict['dst']
        msg_dict = json.loads(payload_dict['msg'])

        
    
    def broadcast(self, src_ip, payload_dict):
        #Build 
        announcement_dict = {}
        announcement_dict['type'] = 'update'
        announcement_dict['src'] = payload_dict['src']
        announcement_dict['']

        #Broadcast update to others
        if self.relations[src_ip] == 'cust':
            print("do cust")
        elif self.relations[src_ip] == 'peer' or self.relations[src_ip] == 'prov':
            print('do rest')
        else:
            raise Exception("Could not match ip to relation")
        print("todo")

    def handle_handshake(self, json_payload):
        print("TO DO HANDSHAKE")

    def handle_withdraw(self, json_payload):
        payload = json.loads(json_payload)
        self.withdraw_record.append(payload)

    # Takes in a network ip and a net_mask and returns a masked network ip
    def mask(self, network, net_mask) -> str:
        network_quads = list(int(qdn) for qdn in network.split('.'))
        net_mask_quads = list(int(qdn) for qdn in net_mask.split('.'))
        
        masked_quads = []
        for i in range(len(network_quads)):
            masked_binary_quad = network_quads[i] & net_mask_quads[i]
            masked_quads.insert(i, masked_binary_quad)
        return "%d.%d.%d.%d" % (masked_quads[0], masked_quads[1], masked_quads[2], masked_quads[3]) 
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='route packets')
    parser.add_argument('asn', type=int, help="AS number of this router")
    parser.add_argument('connections', metavar='connections', type=str, nargs='+', help="connections")
    args = parser.parse_args()
    router = Router(args.asn, args.connections)
    router.run()
