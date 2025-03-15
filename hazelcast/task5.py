from hazelcast import HazelcastClient
import concurrent.futures
import time

def with_lock(client, key):
    map = client.get_map("d-map1").blocking()
    if not map.contains_key(key):
        map.put(key, 0)
    for _ in range(10000):
        map.lock(key)  
        try:
            value = map.get(key)
            value += 1
            map.put(key, value)
        finally:
            map.unlock(key)  

def task():
    client1 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client2 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client3 = HazelcastClient(cluster_name="hello-world", cluster_members=[])

    key = "key"
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        futures.append(executor.submit(with_lock, client1, key))
        futures.append(executor.submit(with_lock, client2, key))
        futures.append(executor.submit(with_lock, client3, key))
        concurrent.futures.wait(futures)

    end_time = time.time()
    map = client1.get_map("d-map1").blocking()
    print(f"Final value: {map.get(key)}")
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    task()
