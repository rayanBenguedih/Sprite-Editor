from enum import IntEnum, auto

class Events(IntEnum):
    LCLICK =  auto()
    LHOLD = auto()
    RCLICK =  auto()
    RHOLD = auto()
    
    CURSOR = auto()

    KEYDOWN = auto()
    KEYUP = auto()
    KEYHOLD = auto()
    
    QUIT = auto()

class Manager:
    toclear = [Events.LCLICK,
               Events.RCLICK,
               Events.KEYDOWN,
               Events.KEYUP,]
    def __init__(self, loader):
        self.events = {Events.LCLICK:False,
                       Events.LHOLD:False,
                       Events.RCLICK:False,
                       Events.RHOLD:False,
                       Events.CURSOR:[999999, 99999],
                       Events.KEYDOWN:False,
                       Events.KEYUP:False,
                       Events.KEYHOLD:set(),
                       Events.QUIT:False,}

        self.loader = loader

    def update(self, events):
        oldevents = self.events.copy()
        self.clear()
        for event in events:
            if event.type == self.loader.pygame.QUIT:
                self.events[Events.QUIT] = True
            if event.type == self.loader.pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.events[Events.LCLICK] = event.pos
                    self.events[Events.LHOLD] = True
                if event.button == 1:
                    self.events[Events.RCLICK] = event.pos
                    self.events[Events.RHOLD] = True
            if event.type == self.loader.pygame.MOUSEMOTION:
                self.events[Events.CURSOR] = event.pos
            if event.type == self.loader.pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.events[Events.LHOLD] = False
                if event.button == 1:
                    self.events[Events.RHOLD] = False
            if event.type == self.loader.pygame.KEYDOWN:
                self.events[Events.KEYDOWN] = event.key
                self.events[Events.KEYHOLD].add(event.key)
            if event.type == self.loader.pygame.KEYUP:
                self.events[Events.KEYUP] = event.key
                self.events[Events.KEYHOLD].remove(event.key)
        
    def clear(self):
        for e in Manager.toclear:
            self.events[e] = False
    def __getitem__(self, key):
        return self.events[key]
