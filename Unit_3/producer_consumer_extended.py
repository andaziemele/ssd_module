from threading import Thread
from queue import Queue
import hashlib
import logging

q = Queue()
final_results = []

logging.basicConfig(level=logging.INFO)


def encrypt(data):
    return hashlib.sha256(str(data).encode()).hexdigest()


def decrypt(data):
    # In a real scenario, use proper encryption/decryption
    return int(data[:2], 16)


def producer():
    for n in range(100):
        encrypted_data = encrypt(n)
        q.put(encrypted_data)
        logging.info(f"Produced: {encrypted_data}")


def consumer():
    while True:
        encrypted_data = q.get()
        decrypted_data = decrypt(encrypted_data)
        result = (decrypted_data, decrypted_data ** 2)
        final_results.append(result)
        logging.info(f"Consumed: {encrypted_data}")
        q.task_done()


for i in range(5):
    t = Thread(target=consumer)
    t.daemon = True
    t.start()

producer()

q.join()

print(final_results)
