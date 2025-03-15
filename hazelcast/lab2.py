import hazelcast
import time


def task3():
    hz = hazelcast.HazelcastClient(cluster_name="hello-world",cluster_members=[])
    try:
        key = 0
        counter = 0
        map = hz.get_map("distributed-map2").blocking()
        for _ in range(1000):
            key+=1
            counter+=1
            map.put(key, counter)
            print(f"Sent: {counter}")
    finally:
        hz.shutdown()
        
def task5():
    hz = hazelcast.HazelcastClient(cluster_name="hello-world",cluster_members=[])

    try:
        queue = hz.get_queue("bounded-queue").blocking()
        for i in range(1, 101):
            queue.put(i)
            print(f"Sent: {i}")
            time.sleep(0.1)
    finally:
        hz.shutdown()
   
        
        
if __name__ == "__main__":
    task5()
