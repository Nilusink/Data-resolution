from os import system, listdir, path
from tkinter import filedialog, Tk


paths = list()
files = list()

root = Tk()
dir = filedialog.askdirectory()+'/'
root.destroy()

paths2 = [dir+x for x in listdir(dir)]

invalid = list()

scanned_pahts = list()
def is_scanned(path):
    return path in scanned_paths

newelements = int()

while True:
    try:
        for dire in paths2:
            if path.isdir(dire):
                new = listdir(dire)
                for element in new:
                    print(dire+element, end='\r')
                    if not dire+'/'+element in paths2 and not dire+'/'+element in invalid:
                        if dire=='C:/':
                            if path.isdir(dire+'/'+element):
                                paths2.append(dire+'/'+element)

                        else:
                            if path.isdir(dire+'/'+element):
                                paths2.append(dire+'/'+element)
                            else:
                                paths2.append(dire+'/'+element)

        if not newelements:
            break

        newelements = 0

    except PermissionError:
        paths2.remove(dire)
        print('Peremission Denied: '+dire)
        invalid.append(dire)

paths2.sort()

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
        print('----'+elements[elLen-1])

input('\n\nPress Enter to exit')