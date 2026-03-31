import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines
    QUEUE_MAX_SIZE = 5       # Incremental Queue Length
    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads
        # Add synchronization locks and condition variables
        self.lock = threading.Lock()
        self.queue_not_full = threading.Condition(self.lock)
        self.queue_not_empty = threading.Condition(self.lock)
    def startSimulation(self):
        # Create Machine and Printer threads
        # writ code here
        for i in range(self.NUM_MACHINES):
            t = self.machineThread(i, self)
            self.mThreads.append(t)
            
        # Start all the threads
        # Write code here
        for t in self.mThreads:
            t.start()
        for t in self.pThreads:
            t.start()

        # Let the simulation run for some time
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        self.sim_active = False
        # Weak up all waiting threeads
        with self.lock:
            self.queue_not_full.notify_all()
            self.queue_not_empty.notify_all()

        # Wait until all printer threads finish by joining them
        # Write code here
        for t in self.mThreads:
            t.join()
        for t in self.pThreads:
            t.join()

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                with self.outer.queue_not_empty:
                    while len(self.outer.print_list) == 0 and self.outer.sim_active:
                        self.outer.queue_not_empty.wait()

                    if not self.outer.sim_active:
                        break

                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)
                self.outer.queue_not_full.notify()

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                with self.outer.queue_not_full:
                    while len(self.outer.print_list) >= self.outer.QUEUE_MAX_SIZE and self.outer.sim_active:
                        self.outer.queue_not_full.wait()

                    if not self.outer.sim_active:
                        break
                # Machine wakes up and sends a print request
                # Write code here
                self.printRequest(self.machineID)
                self.outer.queue_not_empty.notify()

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)