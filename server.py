import Pyro4

@Pyro4.expose
class Replica(object):
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.vector_clock = 0
        self.other_replicas = []

    def add_replica(self, replica):
        self.other_replicas.append(replica)

    def write(self, key, value, clock=None, propagate=True):
        if clock is None or clock > self.vector_clock:
            self.vector_clock = max(self.vector_clock, clock or 0) + 1
            self.data[key] = (value, self.vector_clock)
            print(f"Replica '{self.name}': Key '{key}' added.")
            if propagate:
                for replica in self.other_replicas:
                    replica.write(key, value, self.vector_clock, False)
        else:
            print(f"Replica '{self.name}': Write operation for key '{key}' ignored due to stale clock.")

    def delete(self, key, clock=None, propagate=True):
        if key in self.data and (clock is None or clock > self.vector_clock):
            del self.data[key]
            self.vector_clock = max(self.vector_clock, clock or 0) + 1
            print(f"Replica '{self.name}': Key '{key}' deleted.")
            if propagate:
                for replica in self.other_replicas:
                    replica.delete(key, self.vector_clock, False)
        else:
            print(f"Replica '{self.name}': Delete operation for key '{key}' ignored due to stale clock.")

    def read(self, key):
        value, clock = self.data.get(key, (None, -1))
        if value is None:
            print(f"Replica '{self.name}': Key '{key}' not found.")
        else:
            print(f"Replica '{self.name}': Key '{key}' found.")
        return value, clock


def main():
    replica1 = Replica('Replica1')
    replica2 = Replica('Replica2')
    replica1.add_replica(replica2)
    replica2.add_replica(replica1)

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri1 = daemon.register(replica1)
    uri2 = daemon.register(replica2)
    ns.register("replica1", uri1)
    ns.register("replica2", uri2)
    print("Replicas are running...")
    daemon.requestLoop()

if __name__=="__main__":
    main()

