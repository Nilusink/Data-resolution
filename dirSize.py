from os import walk, listdir
from os.path import join, getsize, isdir
from tkinter import filedialog, Tk
from time import time

def GetFolderSize(path):
    TotalSize = 0
    for item in walk(path):
        for file in item[2]:
            try:
                TotalSize = TotalSize + getsize(join(item[0], file))
            except:
                print("error with file:  " + join(item[0], file))
    return TotalSize

root = Tk()
direc = filedialog.askdirectory()+'/'
root.destroy()
print(f'Directory: {direc}\n')

start = time()
dirs = list()
for element in listdir(direc):
    if isdir(direc+element):
        dirs.append([direc+element, float(GetFolderSize(direc+element)) /1024 /1024 /1024])
end = time()

max = [str(), int()]
min = [str(), int()]
for element in dirs:
    print(f'{element[0]}: {round(element[1], 2)} GB')

    if element[1]==max[1]:
        max = [f'{max[0]} \n{element}', element[1]]
    elif element[1]>max[1]:
        max = [element[0], element[1]]
    
    if element[1]==min[1]:
        min = [f'{min[0]} \n{element[0]}', element[1]]
    elif element[1]<min[1]:
        min = [element[0], element[1]]

print(f'\nBiggest folder(s): {max[0]} with {round(max[1], 2)} GB stored')
print(f'\nSmallest folder(S): {min[0]} with {round(min[1], 2)} GB stored')


input(f'\n\ntook {round(end-start, 2)} sek.')