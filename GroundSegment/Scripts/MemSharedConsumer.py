import pickle
from multiprocessing import shared_memory
# Attach to the existing shared memory block


#https://github.com/python/cpython/issues/82300

class OTest():
    def __init__(self, id, name):
        self.id = id
        self.name = name


existing_shm = shared_memory.SharedMemory(name='wnsm_f8f0d969') 
plist = pickle.loads(existing_shm.buf)

for o in plist:
    print(o.id, o.name)


input("Press Enter to exit...")


