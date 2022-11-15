import pygame as pygame
from DATA import *

import toolbar
from events import Events, Manager
import loader



from os import system

def clear(): system('cls')

class Entity:
    def __init__(self, *, size, pos, sprite=None, imgdata=None):
        self.imgdata = imgdata
        self.sprite = sprite
        self.size = size
        self.pos = pos

    def __repr__(self):
        if self.imgdata:
            return f"{self.imgdata}"
        return f"{self.pos} {self.size}"
    def draw(self, window):
        if self.sprite:
            window.blit(self.sprite, self.pos)

    def bbox(self, window):
        pygame.draw.rect(window, (0, 0, 0), [*self.pos, *self.size], 1)


pygame = loader.pygame
WIDTH, HEIGHT = 600, 600
display = pygame.display.set_mode((WIDTH, HEIGHT))

#loader.windowentity = entity({'size': [WIDTH, HEIGHT], 'pos': [0, 0]})
loader.windowentity = Entity(size=[WIDTH, HEIGHT], pos=[0, 0])
events = Manager(loader)
t = toolbar(events, loader)

query = ''

clear()

offset = 0, 0

Clock = pygame.time.Clock()

to_blit = []
loop = True
while loop:
    events.update(pygame.event.get())
    Clock.tick(30)
    if events[Events.QUIT]:
        loop = False
    if event := events[Events.KEYDOWN]:
        if event == pygame.K_BACKSPACE:
            query = query[:-1]
        elif event == pygame.K_ESCAPE:
            query = ''
        elif event == pygame.K_RETURN:
            if query == 'cls':
                to_blit = []
                clear()
            if query == 'exit':
                loop = False
            else:
                try:
                    sprite = loader.get(query)
                    sprite = sprite.resize(.5)
                    sprite.ToPygame()
                    pos = [t.offset[0] - sprite.size[0] // 2, t.offset[1] - sprite.size[1] // 2]
                    t.objects.append(Entity(pos=pos, size=sprite.size, sprite=sprite.img, imgdata=sprite))
                    print(to_blit)
                except StopIteration:
                    pass

            query = ''
        else:
            try:
                c = chr(event)
                if c == '-':
                    c = '_'
                query += c 
            except:
                pass
        print(query)   

    display.fill(0xffffff)
    t.run(display)

    t.draw(display)

    pygame.display.flip()
pygame.quit()
