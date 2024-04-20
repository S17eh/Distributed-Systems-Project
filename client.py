import Pyro4
import time

def main():
    ns = Pyro4.locateNS()
    uri1 = ns.lookup('replica1')
    uri2 = ns.lookup('replica2')
    replica1 = Pyro4.Proxy(uri1)
    replica2 = Pyro4.Proxy(uri2)

    # Write a value
    print("Client: Sending 'write' request for key 'key1' to Replica1.")
    replica1.write('key1', 'value1')
    time.sleep(1)  
    print("Client: Sending 'write' request for key 'key2' to Replica2.")
    replica2.write('key2', 'value2')
    time.sleep(1)  

    # Read a value
    print("Client: Sending 'read' request for key 'key2' to Replica1.")
    print(replica1.read('key2'))
    time.sleep(1)  
    print("Client: Sending 'read' request for key 'key1' to Replica2.")
    print(replica2.read('key1'))
    time.sleep(1)  

    # Delete a value
    print("Client: Sending 'delete' request for key 'key1' to Replica1.")
    replica1.delete('key1')
    time.sleep(1)  
    print("Client: Sending 'read' request for key 'key1' to Replica2.")
    print(replica2.read('key1'))

if __name__=="__main__":
    main()
