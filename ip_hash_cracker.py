import hashlib
import multiprocessing
import time

TARGET_HASH = ""  # Replace with the target MD5 hash you want to find

TOTAL_IPS = 256 ** 4

def search_chunk(start, end, result_queue):
    for i in range(start, end):
        ip = f"{(i >> 24) & 0xFF}.{(i >> 16) & 0xFF}.{(i >> 8) & 0xFF}.{i & 0xFF}"

        if hashlib.md5(ip.encode()).hexdigest() == TARGET_HASH:
            result_queue.put(ip)
            return

    result_queue.put(None)


def main():
    num_cores = multiprocessing.cpu_count()
    chunk_size = TOTAL_IPS // num_cores

    print(f"Target hash  : {TARGET_HASH}")
    print(f"CPU cores    : {num_cores}")
    print(f"Total IPs    : {TOTAL_IPS:,}")
    print("Scanning...\n")

    result_queue = multiprocessing.Queue()
    processes = []
    start_time = time.time()

    for i in range(num_cores):
        start = i * chunk_size
        end = TOTAL_IPS if i == num_cores - 1 else start + chunk_size

        p = multiprocessing.Process(
            target=search_chunk,
            args=(start, end, result_queue)
        )
        p.start()
        processes.append(p)

    found = None
    finished = 0

    while finished < num_cores:
        result = result_queue.get()
        finished += 1

        if result is not None:
            found = result
            for p in processes:
                p.terminate()
            break

    for p in processes:
        p.join()

    elapsed = time.time() - start_time

    if found:
        verification = hashlib.md5(found.encode()).hexdigest()
        print(f"FOUND!       →  {found}")
        print(f"Elapsed      : {elapsed:.2f} seconds")
        print(f"Verification : md5('{found}') = {verification}")
        print(f"Match        : {verification == TARGET_HASH}")
    else:
        print(f"Not found. Elapsed: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
