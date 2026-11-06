# ip_hash_cracker
IP Address MD5 Hash Cracker

A brute-force tool that recovers an IPv4 address from its MD5 hash.
Since MD5 is a one-way function, the only way to reverse it for an IP
address is to hash every possible IPv4 address (0.0.0.0 – 255.255.255.255)
and compare the result against the target hash.

How it works:
  - Treats every IPv4 address as an integer (0 to 2^32 − 1)
  - Converts each integer to dotted-decimal notation using bit shifting
  - Computes the MD5 hash of that string and compares it to the target
  - Splits the search space evenly across all available CPU cores
    using Python's multiprocessing module
  - Terminates all worker processes as soon as a match is found

Usage:
  1. Set TARGET_HASH to the MD5 hash you want to crack.
  2. Run:  python3 ip_hash_cracker.py

Performance:
  Typical runtime is under 60 seconds on a modern machine (2–4 cores).
  More cores = proportionally faster.

Requirements:
  Python 3.6+  |  No third-party libraries required
