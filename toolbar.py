from sys import modules
from events import Events

class toolbar:
    class tool:
        def __init__(this, self, name, f, pos):
            this.self = self
            this.call = f
            this.name = name
            this.up = self.loader.get([name, 'up'], None).resize(.5)
            this.down = self.loader.get([name, 'down'], None).resize(.5)

            this.cursor = self.loader.get([name, 'cursor'], None)
            iterator = iter(this.cursor.asbytes)
            tmp = [[b, next(iterator)][0] for b in iterator]
            tmp = [' X'[round(i / 255)] for i in tmp]
            s = []
            w = this.cursor.size[0]
            h = this.cursor.size[1]
            for i in range(0, len(this.cursor.asbytes), w):
                v = ''.join(tmp[i:i+w-w%8])
                if 'X' in v:
                    s.append(v)

            s = s[:len(s)-len(s)%8]
            this.compiled_cursor = self.loader.pygame.cursors.compile(s)
            this.csize = [len(s[0]), len(s)]
            
            this.up.ToPygame()
            this.down.ToPygame()

            this.pos = [pos + 10, 10]
            this.size = this.up.size
            self.pos = this.pos[0] + this.size[0]

        def __call__(this):
            this.call(this.self)
        
        def draw(this, display):
            if this.self.tool == this:
                display.blit(this.down.img, this.pos)
                cpos = this.self.events[Events.CURSOR]
                if toolbar.pointinobject(cpos, this.self.loader.windowentity):
                    this.self.loader.pygame.mouse.set_cursor(
                            this.csize,
                            [0, 0],
                            *this.compiled_cursor)
            else:
                display.blit(this.up.img, this.pos)

    def __init__(self, events, loader):
        self.loader = loader
        self.objects = []
      
        self.events = events

        self.tool = None
        self.tools = {}

        self.pos = 0

        self.addtool('select')
        self.addtool('offset')

        self.tool = self.tools['select']
        self.selected = None
        self.offset = [0, 0]

    def __getattr__(self, attr):
        if attr in self.tools:
            return self.tools[attr]
        raise AttributeError(f"type object '{type(self)}' has no attribute '{attr}'")
    def addtool(self, name):
        self.tools[name] = toolbar.tool(self, 
                name, 
                getattr(self, '_' + name), 
                self.pos)

    def run(self, display):
        if self.events[Events.LCLICK]:
            pos = self.events[Events.CURSOR]
            if toolbar.pointinrect(pos, [0, 0, 600, 60]):
                for name, tool in self.tools.items():
                    if toolbar.pointinobject(pos, tool):
                        self.tool = tool
                        break
                else:
                    self.tool = None
        self.draw(display)

        if self.tool:
            self.tool()
        else:
            self.loader.pygame.mouse.set_system_cursor(self.loader.pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, display):
        if not self.tool:
            self.loader.pygame.mouse.set_system_cursor(self.loader.pygame.SYSTEM_CURSOR_ARROW)
        if self.selected:
            self.selected.bbox(display)
        for tool in self.tools.values():
            tool.draw(display)
        for o in self.objects:
            o.draw(display)
        
    @staticmethod 
    def pointinrect(point, rect):
        return point[0] > rect[0] and point[0] < rect[0] + rect[2] and \
               point[1] > rect[1] and point[1] < rect[1] + rect[3]
    @staticmethod
    def pointinobject(point, self):
        return point[0] > self.pos[0] and point[0] < self.pos[0] + self.size[0] and \
               point[1] > self.pos[1] and point[1] < self.pos[1] + self.size[1]

    @staticmethod
    def _select(self):
        if self.events[Events.LCLICK]:
            for o in self.objects:
                if self.pointinrect(self.events[Events.CURSOR], [*o.pos, *o.size]): 
                    self.selected = o
                    print(f"Selected {o}.")
                    break
            else:
                print(f"Unselected {o}.")
                self.selected = None

    @staticmethod
    def _offset(self):
        if self.events[Events.LCLICK]:
            self.offset = self.events[Events.CURSOR]
            print(f"offset -> {self.offset}")

modules['toolbar'] = toolbar
