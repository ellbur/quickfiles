# encoding=utf-8

from __future__ import print_function
from collections import namedtuple as nt
import os
import sys
import shutil
from glob import glob
from subprocess import Popen, PIPE
import re
import time

class PTuple(tuple):
    def __floordiv__(self, pat):
        return self.flatmap(lambda _: _//pat)
    def flatmap(self, func):
        res = []
        for _ in self:
            res.extend(func(_))
        return PTuple(res)
    
class Path(nt('Path', ['path'])):
    @staticmethod
    def mktemp():
        import tempfile
        _, path = tempfile.mkstemp()
        return p(path)
    def __repr__(self): return './' + self.path
    @property
    def realpath(self): return os.path.realpath(self.path)
    def __truediv__(self, next):
        return self.__div__(next)
    def __div__(self, next):
        return p(str(self) + '/' + str(next))
    @property
    def exists(self): return os.path.exists(str(self))
    def against(self, where): return './' + os.path.relpath(str(self), str(where))
    def replant(self, src, dst): return p(dst) / self.against(src)
    def indir(self, dst): return self.replant(self.dir, dst)
    @property
    def isdir(self): return os.path.isdir(str(self))
    def chext(self, old, new):
        assert self.path.endswith(old)
        return p(seld.path[:-len(old)] + new)
    def setext(self, new):
        prefix = re.sub(r'\.[^\.\/]*$', '', self.path)
        return p(prefix + new)
    @property
    def name(self): return os.path.split(os.path.realpath(str(self)))[1]
    @property
    def dir(self):
        if os.path.isdir(str(self)): return self
        else: return p(os.path.split(os.path.realpath(str(self)))[0])
    def make_parents(self): self.dir.makedir()
    def mkdir(self): return self.makedir()
    def makedir(self):
        try:
            os.makedirs(str(self))
        except OSError as e:
            if e.errno != 17: raise e
    @property
    def name(self):
        return os.path.split(os.path.realpath(str(self)))[1]
    @property
    def realpath(self):
        return os.path.realpath(str(self))
    def __floordiv__(self, pat):
        if pat == '**':
            dirs = []
            def see(_, dir, __):
                dirs.append(p(dir))
            os.path.walk(str(self), see, None)
            return PTuple(dirs)
        else:
            return PTuple(p(_) for _ in glob(str(self) + '/' + pat))
    def __mod__(self, how):
        if isinstance(how, RAND):
            import tempfile
            self.makedir()
            _, path = tempfile.mkstemp(dir=str(self), prefix=how.prefix, suffix=how.suffix)
            return p(path)
        elif isinstance(how, COUNTER):
            candidates = (_ for _ in os.listdir(str(self)) if _.startswith(how.prefix))
            number_strs = (c[len(how.prefix):] for c in candidates)
            numbers = [ ]
            for s in number_strs:
                try: numbers.append(int(s))
                except ValueError: pass
            now = max(numbers) + 1 if len(numbers)>0 else 1
            return self/(how.prefix + str(now))
        else:
            raise TypeError(how, 'should be one of', [RAND, COUNTER])
    
    def rm(self): shutil.rmtree(str(self))
    def set(self, wth):
        self.make_parents()
        open(str(self), 'w').write(wth)
    def clear(self):
        self.set('')
    def setas(self, wth):
        self.make_parents()
        wth(open(str(self), 'w'))
    def append(self, wth):
        self.make_parents()
        open(str(self), 'a').write(wth)
    def open(self):
        return open(str(self), 'r')
    def read(self):
        return self.open().read()
    def cp(self, dest):
        dest = p(dest)
        if dest.isdir:
            dest = dest / self.name
        if self.isdir:
            shutil.copytree(str(self), str(dest))
        else:
            shutil.copy2(str(self), str(dest))
    
class COUNTER(nt('COUNTER', ['prefix'])): pass
_RAND = nt('RAND', ['prefix', 'suffix'])
class RAND(_RAND):
    @staticmethod
    def __new__(_cls, prefix='', suffix=''):
        return _RAND.__new__(_cls, prefix, suffix)

def p(s):
    if isinstance(s, Path): return s
    elif isinstance(s, basestring): return Path(os.path.normpath(os.path.relpath(s)))
    else: raise TypeError
_p = p

t = tuple
def tt(*things): return tuple(things)

def adict(**things):
    return things
    
def struct(**things):
    return nt('Struct', things.keys())(**things)
    
def nstruct(name):
    return struct(
        of = lambda **things: nt(name, things.keys())(**things)
    )
    
