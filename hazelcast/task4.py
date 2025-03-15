from hazelcast import HazelcastClient
import concurrent.futures

def increment_value(client, key):
    map = client.get_map("d-map").blocking()
    if not map.contains_key(key):
        map.put(key, 0)

    for _ in range(10000):
        value = map.get(key)
        value += 1
        map.put(key, value)

def task():
    client1 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client2 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    client3 = HazelcastClient(cluster_name="hello-world", cluster_members=[])
    key = "key"

    # Для запуску функцій одночасно
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        futures.append(executor.submit(increment_value, client1, key))
        futures.append(executor.submit(increment_value, client2, key))
        futures.append(executor.submit(increment_value, client3, key))
        concurrent.futures.wait(futures)

    map = client1.get_map("d-map").blocking()
    print(f"Final value for key: {map.get(key)}")

if __name__ == "__main__":
    task()
