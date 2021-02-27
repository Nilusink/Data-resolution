from os import system, listdir, path
import concurrent.futures
from tkinter import filedialog, Tk
from time import time

class MyClass:
    def __init__(self):
        self.dirs = list()
        pass

    def myfunc(self, direcotrys):
        direcotrys = [direcotrys]
        invalid = list()
        newelements = int()
        while True:
            try:
                for dire in direcotrys:
                    if path.isdir(dire):
                        new = listdir(dire)
                        newelements+=len(new)
                        for element in new:
                            print(dire+element, end='\r')
                            if not dire+'/'+element in direcotrys and not dire+'/'+element in invalid:
                                if dire=='C:/':
                                    if path.isdir(dire+'/'+element):
                                        self.dirs.append(dire+'/'+element)

                                else:
                                    if path.isdir(dire+'/'+element):
                                        self.dirs.append(dire+'/'+element)
                                    else:
                                        self.dirs.append(dire+'/'+element)
                if newelements<=0:
                    print(newelements)
                    break

                newelements = 0

            except PermissionError:
                direcotrys.remove(dire)
                print('Peremission Denied: '+dire)
                invalid.append(dire)
            
            except Exception as e:
                print(e)

        return self.dirs


if __name__=='__main__':
    paths = list()
    files = list()

    root = Tk()
    dir = filedialog.askdirectory()+'/'
    root.destroy()

    paths2 = [dir+x for x in listdir(dir)]


    scanned_pahts = list()
    def is_scanned(path):
        return path in scanned_pahts

    newelements = int()

    clas = MyClass()
    start = time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for elements in executor.map(clas.myfunc, paths2):
            for element in elements:
                #print(elements)
                if not element in paths2:
                    paths2.append(element)

    end = time()

    paths2.sort()
    #print(paths2)
    for element in paths2:
        #print(element)
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
    
    print('\n\n\n',end-start)
    input('\n\nPress Enter to exit')