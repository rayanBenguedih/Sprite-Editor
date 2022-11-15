import json
import pip

from dataclasses import dataclass, field
from itertools import product
from os import walk
from os.path import join

from utils import colors


data_path = 'data.json'

files = lambda path: next(walk(path), (None, None, []))[2]
folders = lambda path: next(walk(path), ([], None, None))[1]


class _metaLoader(type):

    fparse = None
    fcompile = None
    image = None
    pygame = None
    _pygameinit = False

    @staticmethod
    def __call__(*, import_only=False):
        if not Loader.image:
            try:
                from PIL import Image
            except ModuleNotFoundError:
                Image = Loader.pip_Pillow
            Loader.image = Image
        if not Loader.fparse or not Loader.fcompile:
            try:
                from parse import parse as fparse, compile as fcompile
            except ModuleNotFoundError:
                fparse, fcompile = Loader.pip_parse
            Loader.fparse = fparse
            Loader.fcompile = fcompile
        if not Loader.pygame:
            try:
                import pygame
            except ModuleNotFoundError:
                pygame = Loader.pip_pygame
            Loader.pygame = pygame
            if not Loader._pygameinit:
                pygame.init()
                Loader._pygameinit = True

        if import_only:
            return
        data = Loader.images
        images = []
        for key, value in data.items():
            for group in product(*value['iter']):
                if group[1] == '*':
                    for d in folders(value['path'].format(*group)[:-2]):
                        path = value['path'].format(group[0], d)
                            
                        images += Loader._walk(path, group, key)
                else:
                    path = value['path'].format(*group)
                    images += Loader._walk(path, group, key)
        loader = Loader.__new__(Loader)
        loader.__init__(images)
        return loader

    @staticmethod
    def _walk(path, group, key):
        images = []
        for image in files(path):
            cf = [key.lower()] + [c.lower() for c in group]
            result = Loader.fparse('{:w}{number:d}.png', image)

            if result: number = result['number']
            else: number = None
            
            images.append(ImageData(join(path, image), tuple(cf), number))
        return images
    @classmethod
    def __getattr__(cls, attr):
        if attr == "images":
            with open(data_path, 'r', encoding="utf*") as f:
                data = json.load(f)
            return data
        if attr == "pip_Pillow":
            pip.main(["install", "Pillow"])
            return __import__("PIL", fromlist=['Image']).Image
        if attr == "pip_parse":
            pip.main(["install", "parse"])
            return (lambda m:[m.parse,m.compile])(__import__("parse", fromlist=['parse', 'compile']))
        if attr == "pip_pygame":
            pip.main(["install", "pygame"])
            return __import__("pygame")
        return None

class Loader(metaclass=_metaLoader):
    def __init__(self, images):
        self.images = images
        for image in self.images:
            with Loader.image.open(image.path) as img:
                image.load(img)
    
    def iget(self, cl, number):
        if number:
            for i in self.images:
                r = [c in i.classification for c in cl]
                if all(r) and i.number == number:
                    yield i
        else:
            for i in self.images:
                r = [c in i.classification for c in cl]
                if all(r):
                    yield i

    def query(self, text):
        compiled = Loader.fcompile("{}_{:w}")
        cl = []
        while result := compiled.parse(text):
            cl.append(result[0])
            text = result[1]
        number = Loader.fparse('{:d}', text)
        if number:
            number = n[0]
        else:
            cl.append(text)
        return cl, number

    def get(self, *args):
        assert len(args) in [1, 2], "'get' takes 1 or 2 arguments"
        if isinstance(args[0], str):
            return next(self.iget(*self.query(args[0])))
        return next(self.iget(*args))

    def __getattr__(self, attr):
        if attr[:2] != 'q_':
            return object.__getattr__(self, attr)
        yield from self.iget(attr[2:])

    def pretty(self, l):
        w = ''
        for i in l:
            w += repr(i)
            w += '\n'
        return w

Loader(import_only=True)

@dataclass
class ImageData:
    path: str
    classification: tuple
    number: int=None

    img:  Loader.pygame.surface=field(repr=False, init=False)

    pilimg: Loader.image.Image=field(repr=False, init=False)
    size: tuple=field(init=False)
    mode: str=field(init=False)

    asbytes: bytes=field(repr=False, init=False)

    def ToPygame(self):
        assert self.asbytes, f'Image has not been loaded'  

        self.img = Loader.pygame.image.fromstring(self.asbytes, self.size, self.mode).convert_alpha()
        print(colors.green(f"Convert {self.path} success."))

    def load(self, img):
        self.asbytes = img.tobytes()

        self.size  = img.size
        self.mode  = img.mode
        self.pilimg = img
    
    def resize(self, size, mode=1, inplace=False):
        """The function used to resize the PIL image saved inside pilimg
        size:
            2-tuple or float
            If a tuple, used as the new size directly,
            if a float, the new size will be the factor of the current size

        mode:
            Corresponds to the mode used in PIL.Image.Image.resize

        inplace:
            If true, will use the current ImageData as the output,
            if False, returns a new one."""
        if isinstance(size, (int, float)):
            size = (int(self.size[0] * size), int(self.size[1] * size))
        assert isinstance(size, (tuple, list)), f"Type '{type(size)}' not supported for size"
        assert 0 <= mode <= 3, "Mode must be between 0 and 3"
        img = self.pilimg.resize(size, resample=mode)
        
        if inplace:
            self.load(img)
            return self
        new = type(self)(self.path, self.classification, self.number)
        new.load(img)

        return new

if __name__ == "__main__":
    l = Loader()
    print(colors.blue(f"With hair_bangs as query."))
    print(l.pretty(l.q_hair_bangs))
    print(colors.cyan("----------sep----------"))
    print(colors.blue(f"Query hair_bangs_1 and convert to pygame surface."))
    for i in l.q_hair_bangs_1:
        i.ToPygame()
else:
    from sys import modules
    modules['loader'] = Loader()
