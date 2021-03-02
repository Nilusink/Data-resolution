from os import system, listdir, path
import concurrent.futures
from tkinter import filedialog, Tk
from time import time

class TreeDirectory:
    def __init__(self):
        pass
    
    def generate(self, directorys):
        self.directorys = [directorys]
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
                try:
                    self.directorys.remove(dire)
                except ValueError:
                    pass
                print('Peremission Denied: '+dire)
                invalid.append(dire)

        self.directorys.sort()
        return self.directorys


if __name__=='__main__':
    root = Tk()
    dir = filedialog.askdirectory()+'/'
    root.destroy()

    print(f'Directory: {dir}')
    pahts = [dir+x for x in listdir(dir)]

    scanned_pahts = list()
    def is_scanned(path):
        return path in scanned_pahts

    tree = TreeDirectory()
    start = time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for elements in executor.map(tree.generate, pahts):
            for element in elements:
                #print(elements)
                if not element in pahts:
                    pahts.append(element)

    end = time()
    '''
    for element in pahts:
        elements = element.split('/')
        elLen = len(elements)

        if path.isdir(element):
            for i in range(elLen-len(dir.split('/'))):
                print('    |', end='')

            print('----'+elements[elLen-1])

        else:
            for i in range(elLen-len(dir.split('/'))):
                print('    |', end='')
            print('----'+elements[elLen-1])
    '''
    print(f'\n\n\ntookk {round(end-start, 2)} sek.')
    input('\n\nPress Enter to exit')