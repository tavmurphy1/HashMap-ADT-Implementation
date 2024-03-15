# Hashmap ADT Project Description

This project represents an implementation two forms of Hashmap ADT utilizing Separate Chaining and Open Addressing collision handling.

This project does not utilize any pre-built Python data structures such as lists or dictionaries.

Hash Map: An efficient data structure for fast lookups, insertions, and deletions based on keys.

This implementation supports both:

Separate Chaining (SC): Handles collisions by using linked lists at each hash table index.

Open Addressing (OA): Handles collisions by probing for an empty slot in the hash table.

# Key Features

Separate Chaining (SC) Hashmap:

put(key, value): Inserts or updates a key-value pair.

get(key): Retrieves the value associated with a key.

contains_key(key): Checks if a key exists in the hash map.

remove(key): Removes a key-value pair.

get_keys_and_values(): Returns a list of key-value tuples.

table_load(): Calculates the hash table's load factor.

Open Addressing (OA) Hashmap:

(Same methods as Separate Chaining)

# Usage Example

** Create hash maps (adjust capacity as needed):**
sc_hashmap = HashMap(capacity=5, function=hash_function_1)  # Separate chaining
oa_hashmap = HashMap(capacity=5, function=hash_function_2)  # Open Addressing

**Add key-value pairs:**
sc_hashmap.put("name", "Alice")
oa_hashmap.put("email", "alice@email.com")

**Retrieve a value**
name = sc_hashmap.get("name") 

**Check for a key**
if oa_hashmap.contains_key("age"):
    print("Age key exists")

**Find elements with the most occurrences in a dynamic array**
mode, frequency = find_mode(da)

# Installation

No installation is required since this is a collection of classes and functions. Copy the code into a Python file and start using it.

# Dependencies

None, this project is self-contained.

# Implementation Notes

The DynamicArray class provides an interface similar to the standard Python list but with efficient resizing.
HashEntry and SLNode are helper classes used to implement the hash map's internal structure.
The HashMap class offers the core hash map functionality.
The find_mode function demonstrates one use case of a hash map to quickly and efficiently locate the most frequent elements in an unsorted array.

# Testing

While no automated test suite is included, you can manually test the code's functionality with examples like those in the "Usage Example" section.

