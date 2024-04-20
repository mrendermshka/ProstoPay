"""
General Implementation notes:
    1) I created two hashmaps classes one works via linked links and notes, another one simplier because was not sure what
    type of development used inside company's products.
    2) for both you can choose capacity of hashmap, it will auto increase if it'll filled up to 70% of capacity.
    3) List was filled with None values, it's gets less memory at the start compare to lists. It decrease
    speed, the reason of it checking if item is filled.
    4) Added testing both of created classes, in console logged if test passed
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMapLinkedList:
    def __init__(self, capacity=10, load_factor=0.7):
        """
        HashMap implemented using linked lists for collision resolution.

        Args:
            capacity (int): Initial capacity of the hash map.
            load_factor (float): Threshold for resizing the hash map.

        Notes:
            - This implementation uses linked lists to handle collisions.
            - The load factor determines when the hash map should resize.
            - Capacity is initially set to 10, but can be adjusted by the user.
        """
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        for bucket in self.buckets:
            current = bucket
            while current:
                index = self._hash(current.key) % new_capacity
                if not new_buckets[index]:
                    new_buckets[index] = Node(current.key, current.value)
                else:
                    node = new_buckets[index]
                    while node.next:
                        node = node.next
                    node.next = Node(current.key, current.value)
                current = current.next
        self.buckets = new_buckets
        self.capacity = new_capacity

    def put(self, key, value):
        index = self._hash(key)
        if not self.buckets[index]:
            self.buckets[index] = Node(key, value)
        else:
            node = self.buckets[index]
            while node:
                if node.key == key:
                    node.value = value
                    return
                if not node.next:
                    break
                node = node.next
            node.next = Node(key, value)
        self.size += 1
        if self.size >= self.load_factor * self.capacity:
            self._resize()

    def get(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        index = self._hash(key)
        prev = None
        node = self.buckets[index]
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return
            prev = node
            node = node.next


class BasicHashMap:
    def __init__(self, capacity=10, load_factor=0.7):
        """
        Basic HashMap implementation using list of lists for collision resolution.

        Args:
            capacity (int): Initial capacity of the hash map.
            load_factor (float): Threshold for resizing the hash map.

        Notes:
            - This implementation uses a list of lists to handle collisions.
            - The load factor determines when the hash map should resize.
            - Capacity is initially set to 10, but can be adjusted by the user.
        """
        self.capacity = capacity
        self.load_factor = load_factor
        self.buckets = [None] * self.capacity
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        for bucket in self.buckets:
            if bucket is not None:
                for key, value in bucket:
                    index = hash(key) % new_capacity
                    if new_buckets[index] is None:
                        new_buckets[index] = []
                    new_buckets[index].append((key, value))

        self.capacity = new_capacity
        self.buckets = new_buckets
        self.load_factor = int(self.capacity * self.load_factor)

    def get(self, key):
        index = self._hash(key)
        if self.buckets[index] is None:
            return None
        bucket = self.buckets[index]
        for current_key, value in bucket:
            if current_key == key:
                return value
        return None

    def put(self, key, value):
        if self.size >= self.load_factor * self.capacity:
            self._resize()
        index = self._hash(key)
        if not self.buckets[index]:
            self.buckets[index] = []
        bucket = self.buckets[index]
        for i, (current_key, current_value) in enumerate(bucket):
            if current_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        if bucket is None:
            return
        for i, (current_key, _) in enumerate(bucket):
            if current_key == key:
                del bucket[i]
                self.size -= 1
                return


def test_hash_maps():
    # Test HashMapLinkedList
    print("Testing LinkedList hash map")
    hashmap_linkedlist = HashMapLinkedList()
    # Test putting data
    hashmap_linkedlist.put("name", "John")
    print("Test 1. Put data 'name' element ---- OK")
    hashmap_linkedlist.put("age", 30)
    print("Test 2. Put data 'age' element ---- OK")
    hashmap_linkedlist.put("city", "New York")
    print("Test 3. Put data 'city' element ---- OK")

    # Test getting data
    assert hashmap_linkedlist.get("name") == "John"
    print("Test 4. Get data 'name' element ---- OK")
    assert hashmap_linkedlist.get("age") == 30
    print("Test 5. Get data 'age' element ---- OK")
    assert hashmap_linkedlist.get("city") == "New York"
    print("Test 6. Get data 'city' element ---- OK")
    assert hashmap_linkedlist.get("country") is None
    print("Test 7. Get non-existent data 'country' element ---- OK")

    # Test deleting data
    hashmap_linkedlist.delete("city")
    print("Test 8. Delete data 'city' element ---- OK")
    assert hashmap_linkedlist.get("city") is None
    print("Test 9. Get deleted data 'city' element ---- OK")

    # Test BasicHashMap
    print("Testing basic hash map")
    basic_hashmap = BasicHashMap()
    # Test putting data
    basic_hashmap.put("name", "Alice")
    print("Test 10. Put data 'name' element ---- OK")
    basic_hashmap.put("age", 25)
    print("Test 11. Put data 'age' element ---- OK")
    basic_hashmap.put("city", "London")
    print("Test 12. Put data 'city' element ---- OK")

    # Test getting data
    assert basic_hashmap.get("name") == "Alice"
    print("Test 13. Get data 'name' element ---- OK")
    assert basic_hashmap.get("age") == 25
    print("Test 14. Get data 'age' element ---- OK")
    assert basic_hashmap.get("city") == "London"
    print("Test 15. Get data 'city' element ---- OK")
    assert basic_hashmap.get("country") is None
    print("Test 16. Get non-existent data 'country' element ---- OK")

    # Test deleting data
    basic_hashmap.delete("city")
    print("Test 8. Delete data 'city' element ---- OK")
    assert basic_hashmap.get("city") is None
    print("Test 9. Get deleted data 'city' element ---- OK")


if __name__ == "__main__":
    test_hash_maps()
