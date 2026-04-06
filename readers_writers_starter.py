"""
COMPX234 - Lab Assignment 2
Readers-Writers Problem using a Monitor in Python

Starter code
------------
Complete the TODO sections to implement a correct monitor solution.

Rules:
1. Multiple readers may read together if no writer is writing.
2. A writer must have exclusive access.
3. Use the monitor methods only to control access.

After you finish:
- test the program,
- rename this file to readers_writers.py if required by your instructor,
- commit your work to GitHub with meaningful commit messages.
"""

from __future__ import annotations

import random
import threading
import time


class ReadersWritersMonitor:
    """
    A monitor-style class that controls access to one shared resource.

    Suggested shared state:
    - active_readers: number of readers currently reading
    - active_writers: 0 or 1
    - waiting_writers: number of writers waiting (optional, but useful)
    """

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

        self.active_readers = 0
        self.active_writers = 0
        self.waiting_writers = 0

    def start_read(self, reader_id: int) -> None:
        """
        Called before a reader starts reading.
        Block the reader if a writer is writing.

        TODO:
        1. Acquire the condition using 'with self.condition:'.
        2. Wait while a writer is active.
        3. Increase active_readers.
        4. Print a useful log message.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            pass

    def end_read(self, reader_id: int) -> None:
        """
        Called after a reader finishes reading.

        TODO:
        1. Decrease active_readers.
        2. Print a useful log message.
        3. If this was the last reader, wake waiting threads.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            pass

    def start_write(self, writer_id: int) -> None:
        """
        Called before a writer starts writing.
        Block the writer if any reader is reading or another writer is active.

        TODO:
        1. Increase waiting_writers before waiting (optional but recommended).
        2. Wait while active_readers > 0 or active_writers > 0.
        3. Update counters carefully when the writer can proceed.
        4. Print a useful log message.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            pass

    def end_write(self, writer_id: int) -> None:
        """
        Called after a writer finishes writing.

        TODO:
        1. Decrease active_writers.
        2. Print a useful log message.
        3. Wake waiting threads.
        """
        with self.condition:
            # TODO: Replace 'pass' with your logic
            pass

# Donot Change this
class Reader(threading.Thread):
    def __init__(self, reader_id: int, monitor: ReadersWritersMonitor, rounds: int = 3) -> None:
        super().__init__()
        self.reader_id = reader_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.1, 0.7))  # stagger thread arrival

            print(f"Reader {self.reader_id} wants to read")
            self.monitor.start_read(self.reader_id)

            print(f"Reader {self.reader_id} is READING")
            time.sleep(random.uniform(0.3, 0.8))  # simulate reading

            self.monitor.end_read(self.reader_id)
            print(f"Reader {self.reader_id} finished reading")

# Donot Change this
class Writer(threading.Thread):
    def __init__(self, writer_id: int, monitor: ReadersWritersMonitor, rounds: int = 2) -> None:
        super().__init__()
        self.writer_id = writer_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.2, 0.9))  # stagger thread arrival

            print(f"Writer {self.writer_id} wants to write")
            self.monitor.start_write(self.writer_id)

            print(f"Writer {self.writer_id} is WRITING")
            time.sleep(random.uniform(0.4, 0.9))  # simulate writing

            self.monitor.end_write(self.writer_id)
            print(f"Writer {self.writer_id} finished writing")


def main() -> None:
    """
    Create the monitor and start the simulation.

    TODO ideas:
    - Create at least 3 readers and 2 writers.
    - Start all threads.
    - Join all threads.
    - Print a final message when the simulation is complete.
    """
    random.seed(42)

    monitor = ReadersWritersMonitor()

    #TODO: Create at least 3 Reader threads.
    readers = [
        Reader(reader_id=1, monitor=monitor)
    ]
    
    #TODO: Create at least 2 writer threads.
    writers = [
        Writer(writer_id=1, monitor=monitor)
    ]

    all_threads = readers + writers
    
    # TODO: Start all threads

    
    # TODO: Wait for all threads to finish


    # TODO: Print final message that simulation completed


if __name__ == "__main__":
    main()
