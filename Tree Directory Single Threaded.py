from os import system, listdir, path
from tkinter import filedialog, Tk
from time import time


paths = list()
files = list()

root = Tk()
dir = filedialog.askdirectory()+'/'
root.destroy()

paths2 = [dir+x for x in listdir(dir)]

scanned_pahts = list()
def is_scanned(path):
    return path in scanned_pahts

class TreeDirectory:
    def __init__(self):
        pass
    
    def generate(self, directorys:list) -> list:
        self.directorys = directorys
        invalid = list()
        newelements = int()
        while True:
            try:
                for dire in self.directorys:
                    if path.isdir(dire):
                        new = listdir(dire)
                        for element in new:
                            #print(dire+element, end='\r')
                            if not dire+'/'+element in self.directorys and not dire+'/'+element in invalid:
                                if dire=='C:/':
                                    if path.isdir(dire+'/'+element):
                                        self.directorys.append(dire+'/'+element)

                                else:
                                    if path.isdir(dire+'/'+element):
                                        self.directorys.append(dire+'/'+element)
                                    else:
                                        self.directorys.append(dire+'/'+element)

                if not newelements:
                    break

                newelements = 0

            except PermissionError:
                self.directorys.remove(dire)
                print('Peremission Denied: '+dire)
                invalid.append(dire)

        self.directorys.sort()
        return self.directorys

tree = TreeDirectory()
start = time()
paths2 = tree.generate(paths2)
end = time()
'''
for element in paths2:
    elements = element.split('/')
    elLen = len(elements)

    if path.isdir(element):
        for i in range(elLen-len(dir.split('/'))):
            print('    |', end='')

        print('----'+elements[elLen-1])

    else:
        for i in range(elLen-len(dir.split('/'))):
            print('    |', end='')
        print('----'+elements[elLen-1])'''

input(f'\n\ntook {round(end-start, 2)} sek.')