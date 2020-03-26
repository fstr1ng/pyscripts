from enum import enum

class config(enum):
    path = '/var/log'
    mode = 0o600
    user = 'tester'

print(config.path.value)

from enum import unique

#@unique
class programstate(enum):
    queued = (0, 'in queue')
    runnning = (1, 'is running')
    waiting = (3, 'waiting for it\'s turn')
    done = (4, 'successfully done')
    failed = (5, 'error')

    sleeping = (3, 'waiting for it\'s turn')

    def __init__(self, id, title):
        self.id = id
        self.title = title

print(ProgramState.SLEEPING)
print(ProgramState.FAILED.id)



from enum import auto as a

class Color(Enum):
    RED = a()
    BLUE = a()
    GREEN = a()

for i in list(Color): print(i, i.value)


