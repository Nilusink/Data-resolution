from tkinter import filedialog, Tk # import filedialog for choosing the file to compute
from contextlib import suppress
root = Tk()
filename = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*"))) # chose file, only .txt (you can choose to see all, if you may have an other file format)
root.destroy()
dat = open(filename, 'r', encoding='utf-8').readlines()

def max(dictionary): #funktion to determine the element of an dictionary with the longest list 
    max = 0; maxone = str()
    for element in dictionary:
        if len(dictionary[element])>max:
            maxone = element; max = len(dictionary[element])
    return maxone

x = str()
messages = list()# split messages (new message when correct time format is given at the beginning of the line)
for element in dat:
    try:
        if element[2] =='.' and element[5] =='.' and element[8] ==',':
            messages.append([element[0:16], x.replace('\n', '')]); x = str()
            x = element[18::]
            pass
        else:
            x += element
    except IndexError:
        x += element
messages.append([element[0:16], x.replace('\n', '')]); x = str()

messperperson = dict() 
for i in range(len(messages)):# assign all messages sent by a specific person to it
    try:
        messperperson[messages[i][1].split(':')[0]].append([messages[i][1][messages[i][1].find(': ')+2:], messages[i][0]])# if the person is already in the dictionary, append the message
    except (AttributeError, KeyError):
        if len(messages[i][1].split(':'))>1:
            messperperson[messages[i][1].split(':')[0]] = list()                            # if the person isn't in the dictionary already, create new element
            messperperson[messages[i][1].split(':')[0]].append([messages[i][1][messages[i][1].find(': ')+2:], messages[i][0]])
    
messperday = dict()
for i in range(len(messages)):# assing all messages sent on a specific day (same as with persons, but with dates)
    try:
        messperday[messages[i][0].split(',')[0]].append([messages[i][1][messages[i][1].find(': ')+2:], messages[i][0], messages[i][1].split(':')[0]])
    except (AttributeError, KeyError):
        if len(messages[i][1].split(':'))>1:
            messperday[messages[i][0].split(',')[0]] = list()
            messperday[messages[i][0].split(',')[0]].append([messages[i][1][messages[i][1].find(': ')+2:], messages[i][0], messages[i][1].split(':')[0]])

#### Print the data
print((filename.split('/'))[len(filename.split('/'))-1])# prints the choosen filename for clarification
print()
print('Total messages sent: '+str(len(messages)))# Total elements is the leng of the list with all messages
print()

for element in messperperson: # for every person, print the ammount of messages sent
    print('Messages sent by '+element+': '+str(len(messperperson[element])))
    print()

print()
x = max(messperperson)
print('Most messages were sent by: '+x)
print('Ammount: ',len(messperperson[x]))# the person with most messages assigned to it
print()

x = max(messperday)
print('Most messages were sent on: '+x)# the day with most messages assigned to it
print('Ammount: ',len(messperday[x]))
print()


# Search for spezific Messages (optional)
while True:
    print('\n')
    keyword = input('search chat: ')   #get the keyword to search for
    res = list()
    k = input('Include Keywords? [y/n] ')
    d = input('Include Dates? [y/n] ')
    n = input('Include Names? [y/n] ')

    if k == 'y':
        for person in messperperson:                                    # searches the keyword in all messages
            for message in messperperson[person]:
                if keyword.lower() in message[0].lower():
                    res.append([message[0], person, message[1]])

    if d == 'y':
        for date in messperday:                                         # searches the keyword in all dates
            for element in messperday[date]:
                if keyword in element[1]:
                    with suppress(IndexError):
                        res.append([element[0], element[2], element[1]])
    
    if n == 'y':
        for person in messperperson:                                    # searches the keyword in all names
            if keyword.lower() in person.lower():
                for message in messperperson[person]:
                    res.append([message[0], person, message[1]])

    # return sorted list
    res = sorted(sorted(sorted(sorted(sorted(res, key=lambda x: int(x[2][13:15])), key=lambda x: int(x[2][10:12])), key=lambda x: int(x[2][0:2])), key=lambda x: int(x[2][3:5])), key=lambda x: int(x[2][6:8]))
    print(f'{len(res)} messages found with: {keyword}\n')  
    ans = str()

    if len(res)!=0:
        ans = input('Should i show them? [y/n] ').lower()           # asks if to print the messages or not

    if ans == 'y':
        try:
            for message in res:
                if message[1]:
                    print(message[0], ' --- sent by '+message[1]+' on '+message[2])

                else:
                    print(message[0], ' --- sent on '+message[2])

        except KeyboardInterrupt:
            ans = None