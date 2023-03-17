import pickle
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager  

#https://github.com/python/cpython/issues/82300

class OTest():
    def __init__(self, id, name):
        self.id = id
        self.name = name


plist = [OTest(1,"Juan"), OTest(2, "Maria")]

ba = pickle.dumps(plist)
#sl = smm.ShareableList(ba) #porque no se puede guardar directamente plist?

shm_a = shared_memory.SharedMemory(create=True, size=len(ba))
#shm_a.buf
#buffer = shm_a.buf
print("Shared memory name: ", shm_a.name)

shm_a.buf[:] = ba

plist = pickle.loads(shm_a.buf)

for o in plist:
    print(o.id, o.name)


input("Press Enter to exit...")
shm_a.close()
shm_a.unlink()


