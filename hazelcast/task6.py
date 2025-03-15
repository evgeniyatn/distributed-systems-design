from hazelcast import HazelcastClient
import concurrent.futures
import time

def optimistic_lock(client, key):
    map = client.get_map("d-map2").blocking()
    if not map.contains_key(key):
        map.put(key, 0)

    for _ in range(10000):
        while True:
            value = map.get(key)
            new_value = value + 1
            if map.replace_if_same(key, value, new_value):
                break

def task():
    client1 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client2 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client3 = HazelcastClient(cluster_name="hello-world", cluster_members=[])

    key = "key"

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        futures.append(executor.submit(optimistic_lock, client1, key))
        futures.append(executor.submit(optimistic_lock, client2, key))
        futures.append(executor.submit(optimistic_lock, client3, key))
        concurrent.futures.wait(futures)

    end_time = time.time()

    map = client1.get_map("d-map2").blocking()
    print(f"Final value: {map.get(key)}")
    print(f"Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    task()
