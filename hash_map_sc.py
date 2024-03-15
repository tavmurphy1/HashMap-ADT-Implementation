
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in the hash map,
        its associated value must be replaced with the new value. If the given key is not in the hash map,
        a new key/value pair must be added.

        When put() is called, if the current load factor of the table is greater than or equal to 1.0, the table must
        be resized to double its current capacity.

        It has O(1) time complexity.
        """
        # 1 - If the current load factor of the table is greater than or equal to 1.0, the table must be resized to
        # double its current capacity
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # 2 - The element is hashed and the remainder taken after dividing by the table size
        table = self._buckets

        table_index = self._hash_function(key) % self._capacity

        # 3 - Linked list located in the hash table at the table index is examined.
        node = table[table_index].contains(key)

        # 3a - if the given key is not located in the hash table,
        # insert a new SL node with the given value to the linked list
        if node is None:
            table[table_index].insert(key, value)

            # Increase the size by one
            self._size += 1

        # 3b - otherwise if the given key
        # is already in the map, we replace its value with the new value
        else:
            node.value = value

        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs must be put into the new table,
        meaning the hash table links are rehashed into the new table using the put method.
        """
        # 1 - First check that new_capacity is not less than 1, if so return and do nothing. If not, change it to the
        # next highest prime number. (using is_prime and next_prime).
        if new_capacity < 1:
            return
        elif new_capacity == 2:
            new_capacity = 2
        elif not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # 2 - Initialize the new table and fill it with linked list buckets
        new_table = DynamicArray()

        for _ in range(new_capacity):
            new_table.append(LinkedList())

        # 2 - Iterate through each bucket of the old table, and initialize capacity and size for the new DA
        arr = self._buckets

        self._buckets = new_table
        self._size = 0

        old_capacity = self._capacity
        self._capacity = new_capacity

        for index in range(old_capacity):

            # 2a - if the bucket is not empty, iterate through the linked list
            if arr[index].length() > 0:

                # 2a1 - For each node extract the key and value
                for node in arr[index]:
                    key_value = node.key
                    value = node.value

                    # 2a2 - Call the put method to put the key_value into the newly sized table.
                    self.put(key_value, value)

        return

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        # Load factor (𝝺) is defined as the number of elements divided by the size of the hash table.
        # aka 𝝺 = n/m
        # 𝝺 is the load factor
        # n is the total number of elements stored in the table (size)
        # m is the number of buckets (capacity)

        # So we have 'load factor == size / capacity'

        size = self._size
        ht_capacity = self._capacity

        load_factor = float(size / ht_capacity)

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        array = self._buckets
        ht_capacity = self._capacity

        empty_count = 0

        # Iterate through each bucket in the Dynamic Array and iterate count if the bucket is empty
        for index in range(ht_capacity):
            if array[index].length() == 0:
                empty_count += 1

        return empty_count

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash map, the method returns None.

        It has O(1) time complexity.
        """

        # 1 - The element is hashed and the remainder taken after dividing by the table size
        table = self._buckets

        table_index = self._hash_function(key) % self._capacity

        # 2 - Linked list located in the hash table at the table index is examined.
        node = table[table_index].contains(key)

        # 3 - If the target bucket is empty or does not contain the given key return None.
        if node is None:
            return None

        # 4 - Else if the target bucket contains the given key, return its associated value
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hashmap, otherwise it returns False. An empty hash map does not contain
        any keys.

        It has O(1) time complexity.
        """

        size = self._size
        ht_capacity = self._capacity
        hash_function = self._hash_function
        table = self._buckets

        # 1 - If the hash map is empty, return False
        if size == 0:
            return False

        # 2 - the input key is hashed and the remainder taken after dividing by the table size
        table_index = hash_function(key) % ht_capacity

        # 2 - Return True if the key is found in its correct bucket using the contains() method
        if table[table_index].contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, it does
        nothing (no exception needs to be raised).

        It has O(1) time complexity
        """

        size = self._size
        ht_capacity = self._capacity
        table = self._buckets
        hash_function = self._hash_function

        # 1 - If the hash map is empty, return
        if size == 0:
            return

        # 2 - the input key is hashed and the remainder taken after dividing by the table size
        table_index = hash_function(key) % ht_capacity

        # 3 - Remove the key from its associated index and decrement size
        if not table[table_index].contains(key):
            return
        else:
            table[table_index].remove(key)
            self._size -= 1
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order
        of the keys in the dynamic array does not matter.
        """
        # 1 - Initialize a Dynamic Array object
        arr = DynamicArray()

        # 2 - Iterate through the hash map, appending each key value pair as a tuple in the Dynamic Array.
        ht_capacity = self._capacity
        buckets = self._buckets

        for index in range(ht_capacity):

            if buckets[index].length() > 0:

                for node in buckets[index]:
                    arr.append((node.key, node.value))

        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """

        # 1 - Create a new Dynamic Array at self._buckets
        self._buckets = DynamicArray()

        # 2 - Append LinkedList objects equal to the current capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # reset size to 0
        self._size = 0

        return


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a Dynamic Array, which is not guaranteed to be sorted. Returns a tuple containing, in the following order,
    a dynamic array comprising the mode value(s) of the given array, and an integer representing the
    highest frequency of occurrence for the mode value(s).

    If there is more than one value with the highest frequency, all values at that frequency should be included in the
    Dynamic Array object being returned (the order does not matter). If there is only one mode, the dynamic array will
    only contain that value.

    We assume that the input array contains at least one element, and that all values stored in the array will be
    strings. There are no checks for these two conditions.

    The function has O(N) time complexity, made possible with the separate chaining hash map.
    """

    map = HashMap()

    highest_frequency = 1

    mode_da = DynamicArray()

    # 1 - We iterate through the input array hashing each element O(N). Key is element, value is # of repetitions
    for index in range(da.length()):

        current_frequency = map.get(da[index])

        if current_frequency is None:
            current_frequency = 1
        else:
            current_frequency += 1

        # 2 - If the current frequency beats the highest, make a new mode array and append the current value
        if current_frequency > highest_frequency:

            mode_val = da[index]

            highest_frequency = current_frequency

            mode_da = DynamicArray()
            mode_da.append(mode_val)

        # 3 - If the current frequency ties the highest, append the current value to the existing mode array
        elif current_frequency == highest_frequency:

            mode_da.append(da[index])

        # If the current frequency is less than the highest, don't do anything else

        # 4 - 'Put' the element into the hash table along with current frequency (minimum of 1)
        map.put(da[index], current_frequency)

    return mode_da, highest_frequency
