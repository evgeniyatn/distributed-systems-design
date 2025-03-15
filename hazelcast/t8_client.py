import hazelcast

def task5():
    hz = hazelcast.HazelcastClient(cluster_name="hello-world",cluster_members=[])
    try:
        queue = hz.get_queue("bounded-queue").blocking()
        while True:
            item = queue.take()
            print(f"Read: {item}")
    finally:
        hz.shutdown()


if __name__ == "__main__":
    task5()
