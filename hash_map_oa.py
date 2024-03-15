
from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated
        value is replaced with the new value. If the given key is not in the hash map, a new key/value pair is added.

        When put() is called, if the current load factor of the table is greater than or equal to 0.5, the table must
        be resized to double its current capacity using resize_table.

        It has O(1) time complexity.
        """

        # 1 - If the current load factor of the table is greater than or equal to 0.5, the table must be resized to
        # double its current capacity
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # 2 - The element is hashed and the remainder taken after dividing by the table size
        ht_capacity = self._capacity
        hash_function = self._hash_function
        table = self._buckets

        table_index = hash_function(key) % ht_capacity

        # 3 - If the hash table located at the initial index is empty, insert the element there and stop
        # Otherwise compute the next index using quadratic probing
        if table[table_index] is None:
            table[table_index] = HashEntry(key, value)
            self._size += 1
            return

        # 3a - If indexed bucket is a tombstone, overwrite w/ HashEntry containing key/value at the indexed bucket and
        # increment size
        elif table[table_index].is_tombstone is True:
            table[table_index] = HashEntry(key, value)
            self._size += 1
            return

        # 3b - If indexed bucket holds matching key and is not a tombstone, overwrite its value and return
        elif table[table_index].key == key and table[table_index].is_tombstone is False:
            table[table_index].value = value
            return

        # 4 - Otherwise quadratic probe until finding a tombstone bucket, empty space, or matching key/non-tombstone
        else:
            j_val = 0
            base_index = table_index
            while True:

                j_val += 1

                table_index = (base_index + j_val ** 2) % ht_capacity

                # 4a - If the indexed bucket holds None, Insert HashEntry containing the key/value at the indexed bucket
                # and decrement size
                if table[table_index] is None:
                    table[table_index] = HashEntry(key, value)
                    self._size += 1
                    return

                # 4b - If indexed bucket is a tombstone, Insert HashEntry containing key/value at the indexed bucket i
                # and increment size
                if table[table_index].is_tombstone:
                    table[table_index] = HashEntry(key, value)
                    self._size += 1
                    return

                # 4c - If indexed bucket holds matching key and not a tombstone, update value of HashEntry and return
                elif table[table_index].key == key and table[table_index].is_tombstone is False:
                    table[table_index].value = value
                    return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs must be put into the new table,
        meaning all non-tombstone hash table links must be rehashed. Another hash map method will help with this.
        """

        # 1 - First check that new_capacity is not less than the current number of elements in the table, if so return
        # and do nothing. If not, change it to the next highest prime number. (using is_prime and next_prime).
        if new_capacity < self._size:
            return
        elif new_capacity == 2:
            new_capacity = 2
        elif not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # 2 - Initialize the new table and fill it with 'None'
        new_table = DynamicArray()

        for _ in range(new_capacity):
            new_table.append(None)

        # 2 - Iterate through each bucket of the old table, and initialize capacity and size for the new DA
        arr = self._buckets

        self._buckets = new_table
        self._size = 0

        old_capacity = self._capacity
        self._capacity = new_capacity

        for index in range(old_capacity):

            # 2a - if the index is not empty and is not a tombstone, extract the key and value
            if arr[index] is not None:

                if arr[index].is_tombstone is False:
                    key_value = arr[index].key
                    value = arr[index].value

                    # 2a2 - Call the put method to put the key_value into the newly sized table.
                    self.put(key_value, value)

        return

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        It has O(1) time complexity.
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

        arr = self._buckets
        ht_capacity = self._capacity

        empty_count = 0

        # Iterate through each bucket in the Dynamic Array and iterate count if the bucket is empty
        for index in range(ht_capacity):
            if arr[index] is None:
                empty_count += 1

        return empty_count

    def get(self, key: str) -> object:
        """
        Receives a key and returns the value associated with that key. If the key is not in the hash map the method
        returns None.

        It has O(1) time complexity.
        """

        # 1 - The element is hashed and the remainder taken after dividing by the table size
        ht_capacity = self._capacity
        table = self._buckets
        hash_function = self._hash_function

        table_index = hash_function(key) % ht_capacity

        # 2 - If the bucket located at the initial index is empty, the key is not in the table. Return None
        if table[table_index] is None:
            return None

        # 2a - if the key is a match, and it is not a tombstone, return the associated value
        elif table[table_index].key == key and table[table_index].is_tombstone is False:
            return table[table_index].value

        # Otherwise we compute the next index using quadratic probing
        else:
            j_val = 0
            base_index = table_index
            while True:
                j_val += 1

                table_index = (base_index + j_val ** 2) % ht_capacity

                # if the probe finds None, return none because it means key is not in the hash map
                if table[table_index] is None:
                    return None

                # 3a - If the loop exited due to finding a matching key, return the value in its associated HashEntry
                if table[table_index].key == key and table[table_index].is_tombstone is False:
                    return table[table_index].value

    def contains_key(self, key: str) -> bool:
        """
        Receives a key and returns true if the given key is in the hash map, otherwise it returns False. An empty hash
        map does not contain any keys.

        It has O(1) Time Complexity.
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

        # 2a - If the bucket located at the initial index is empty return False
        if table[table_index] is None:
            return False

        # 2a - if the initial index has a key match, and it is not a tombstone, return the associated value
        elif table[table_index].key == key and table[table_index].is_tombstone is False:
            return True

        # Otherwise we compute the next index using quadratic probing
        else:
            j_val = 0
            base_index = table_index
            while True:
                j_val += 1

                table_index = (base_index + j_val ** 2) % ht_capacity

                if table[table_index] is None:
                    return False

                if table[table_index].key == key and table[table_index].is_tombstone is False:
                    return True

    def remove(self, key: str) -> None:
        """
        Receives a key and removes it and its associated value from the hash map. If the key is not in the hash map the
        method does nothing (no exception is raised.)

        It has O(1) time complexity.
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

        # 2a - If the bucket located at the initial index is empty return
        if table[table_index] is None:
            return

        # 2b - if the initial index has a key match, and it is not a tombstone, make it a tombstone and decrement size
        if table[table_index].key == key and table[table_index].is_tombstone is False:
            table[table_index].is_tombstone = True
            self._size -= 1
            return

        # 3 - Otherwise Quadratic probe until finding a table_index that is either none or has a matching key
        else:
            j_val = 0
            base_index = table_index
            while True:
                j_val += 1
                table_index = (base_index + j_val ** 2) % ht_capacity

                # 3a - If the table index holds nothing, the value is not in the hash table and we return.
                if table[table_index] is None:
                    return

                # 3b - if the probed index has a key match, and is not a tombstone, make it a tombstone, decrement size
                if table[table_index].key == key and table[table_index].is_tombstone is False:
                    table[table_index].is_tombstone = True
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
        for active_element in self:
            arr.append((active_element.key, active_element.value))

        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """

        # 1 - Create a new Dynamic Array at self._buckets
        self._buckets = DynamicArray()

        # 2 - Append 'None'
        for _ in range(self._capacity):
            self._buckets.append(None)

        # reset size to 0
        self._size = 0

        return

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself. Uses a variable to track the iterators
        progress through the hash map's contents.
        """

        self._index = 0

        return self

    def __next__(self):
        """
        This method returns the next item in the hash map, based on the current location of the iterator. It only
        iterates over active items.
        """

        index = self._index
        da = self._buckets

        try:
            value = da[index]
        except DynamicArrayException:
            raise StopIteration

        while value is None or value.is_tombstone is True:
            self._index += 1
            try:
                value = da[self._index]
            except DynamicArrayException:
                raise StopIteration

        self._index += 1

        return value
