import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from tkinter import Tk, Label, Button, Checkbutton, Entry, FLAT, filedialog, ttk, IntVar, messagebox, NO, Menu
from contextlib import suppress
import numpy as np

messperperson = list()
messperday = list()
filename = str()

def browsefile(reopen=True): # browse files and analyse read data
    global messperperson, messperday, filename
    if reopen:
        filename = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")), parent=mainloop.root) # chose file, only .txt (you can choose to see all, if you may have an other file format)
        #filename = 'C:/Python/Data_resolution/Whatsapp chats/chat_4b.txt' #for debugging, so it doesn't always open a explorer window
    f_name = filename.split('/'); f_name = f_name[len(f_name)-1]
    dat = open(filename, 'r', encoding='utf-8').readlines()
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

    #   -----------------------Statistics---------------------------
    mainloop.f_b['text'] = f'File: {f_name}'    # set "File: " to current file

    pers_mes = str()                                                                                # goes thru every person and counts its messages
    for person in messperperson:
        pers_mes+=f'\n{person}: '.ljust(30, ' ')+f'| {len(messperperson[person])}'.ljust(10, ' ')
    
    xp = max(messperperson)#("{:<30}|  {:<}".format(i, results[0]))
    xd = max(messperday)

    messages = list()
    for element in messperday:
        for message in messperday[element]:
            messages.append(message)
    
    mainloop.stats['text'] = f'''   
Total Messages sent: {len(messages)}

'''
    mainloop.stats2['text'] = f'''
Most messages were sent by 
{xp}
Ammount: {len(messperperson[xp])}

Most messages were sent on 
{xd}
Ammount: {len(messperday[xd])}
'''

    cols = ['Name', 'Messages']                                                                                         # Treeview for person/message
    cols_width = [130, 60]
    statsTree = ttk.Treeview(mainloop.root, columns=cols, height=19, show='headings', selectmode="extended")
    for i, element in enumerate(cols):
        statsTree.column(element, minwidth=0, width=cols_width[i], stretch=NO)   
        statsTree.heading(element, text=element)
    statsTree.place(x=0, y=80)

    for name in messperperson:                                                      # append person to treeview
        vals = (name, len(messperperson[name]))
        statsTree.insert('', 'end', values=vals)

    #   ---------------graph--------------------
    dates = list(); mes_count = list()                                              # format data for graph
    for element in messperday:
        dates.append(element)
        mes_count.append(len(messperday[element]))

    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 5}

    matplotlib.rc('font', **font)

    f = Figure(figsize=(4.1, 4.1), dpi=100)                                         # create graph
    f.set_facecolor('xkcd:gray')
    a = f.add_subplot(111)
    a.plot(dates, mes_count)
    a.xaxis.set_major_locator(MaxNLocator(prune='both',nbins=6))
    a.set_facecolor('xkcd:gray')
    
    canvas = FigureCanvasTkAgg(f, mainloop.root)                                    # convert graph to tkinter object
    canvas.get_tk_widget().place(x=190, y=80)

    '''peop = list(); mes = list()
    for person in messperperson:
        peop.append(person)
        mes.append(len(messperperson[person]))                                      # bar chart, not working

    x = np.arrange(len(peop))
    f2 = Figure(figsize=(2, 2), dpi=100)
    a2 = f2.add_subplot(111)
    rect1 = a2.bar(peop, mes)

    canvas2 = FigureCanvasTkAgg(f2, mainloop.root)
    canvas2.get_tk_widget().place(x=200, y=500)'''
    
def max(dictionary): #function to determine the element of an dictionary with the longest list 
    max = 0; maxone = str()
    for element in dictionary:
        if len(dictionary[element])>max:
            maxone = element; max = len(dictionary[element])
    return maxone

class search_window():  # class for the search window
    def __init__(self):
        self.cols = ['Message', 'From', 'Date']

    def run(self):  # creates new windows, sets buttons and stuff and starts mainloop
        mainloop.root.destroy()
        self.root = Tk()
        self.root.title('Whatsapp - Search')
        self.root.geometry('600x500')
        self.root.resizable(width = False, height=False)
        self.root.configure(bg='grey25')
        self.root.geometry("+%d+%d" % (100, 100))

        self.colls_width = [400, 150, 50]
        self.statsBox = ttk.Treeview(self.root, columns=self.cols, height=20, show='headings', selectmode="extended")    # create the "Results" list
        for i, element in enumerate(self.cols):
            self.statsBox.column(element, minwidth=0, width=self.colls_width[i], stretch=NO)    # make The first element the biggest column, the second one the socond biggest...
            self.statsBox.heading(element, text=element)
        self.statsBox.place(x=0, y=80)

        self.searchE = Entry(self.root, width=30, bg='grey24', fg='white')  # search bar
        self.searchE.place(x=130, y=10)
        self.searchE.insert(0, '')
        searchB = Button(self.root, text='Search', width =15, command=self.search, relief=FLAT, bg='grey25', fg='white')    # search button
        searchB.place(x=300, y=10)

        self.res_l = Label(self.root, text='Results found: 0', bg='grey25', fg='white')
        self.res_l.place(x=130, y=30)

        self.ex_b = Button(self.root, text='Back', width=15, command=mainloop.run, bg='grey25', fg='white', relief=FLAT)
        self.ex_b.place(x=10, y=10)

        self.Kw = IntVar(); self.Kw.set(1)  # create variables for Checkbutton and set them to true
        self.Da = IntVar(); self.Da.set(1)
        self.Na = IntVar(); self.Na.set(1)
        optK = Checkbutton(self.root, text='Keywords', width=10, bg='grey25', fg='white', activebackground='grey24', activeforeground='white', selectcolor="grey25", variable=self.Kw)  # create Checkbuttons
        optD = Checkbutton(self.root, text='  Dates', width=10, bg='grey25', fg='white', activebackground='grey24', activeforeground='white', selectcolor="grey25", variable=self.Da) 
        optN = Checkbutton(self.root, text='  Names', width=10, bg='grey25', fg='white', activebackground='grey24', activeforeground='white', selectcolor="grey25", variable=self.Na)
        optK.place(x=450, y=10) # place Checkbuttons
        optD.place(x=442, y=30)
        optN.place(x=446, y=50)

        self.root.mainloop()
        
    def search(self):
        global messperperson, messperday
        res = list()
        keyword = self.searchE.get()
        if self.Kw.get() or self.Da.get() or self.Na.get():
            if self.Kw.get():
                for person in messperperson:                                    # searches the keyword in all messages
                    for message in messperperson[person]:
                        if keyword.lower() in message[0].lower():
                            res.append([message[0], person, message[1]])

            if self.Da.get():
                for date in messperday:                                         # searches the keyword in all dates
                    for element in messperday[date]:
                        if keyword in element[1]:
                            with suppress(IndexError):
                                res.append([element[0], element[2], element[1]])

            if self.Na.get():
                for person in messperperson:                                    # searches the keyword in all names
                    if keyword.lower() in person.lower():
                        for message in messperperson[person]:
                            res.append([message[0], person, message[1]])

            # return sorted list
            res = sorted(sorted(sorted(sorted(sorted(res, key=lambda x: int(x[2][13:15])), key=lambda x: int(x[2][10:12])), key=lambda x: int(x[2][0:2])), key=lambda x: int(x[2][3:5])), key=lambda x: int(x[2][6:8]))
            for item in self.statsBox.get_children():
                self.statsBox.delete(item)
            
            for i, message in enumerate(res):
                self.statsBox.insert('', 'end', values=(message[0], message[1], message[2]), tags = ('odd' if i%2==0 else 'even',))
            
            
            self.statsBox.tag_configure('odd', background='grey24')
            self.statsBox.tag_configure('even', background='grey20')
    
            self.res_l['text'] = f'Results found: {len(res)}'

        else:
            messagebox.showerror("Error", "Please select at lest 1 option")

def donothing():
    pass

class main():
    def __init__(self):
        pass

    def run(self):
        global messperday, messperperson, messages
        self.root = Tk()                                                # Window config
        self.root.title('Whatsapp - Statistics')
        self.root.geometry('600x600')
        self.root.resizable(width = False, height=False)
        self.root.configure(bg='grey25')
        self.root.geometry("+%d+%d" % (100, 100))

        menubar = Menu(self.root)                                       # create Menu bar
        filemenu = Menu(menubar, tearoff=0)                             #
        filemenu.add_command(label="Open", command=browsefile)          #
        filemenu.add_separator()                                        #
        filemenu.add_command(label="Exit", command=self.root.destroy)   #
        menubar.add_cascade(label="File", menu=filemenu)                #

        self.root.config(menu=menubar)

        filename = 'None'
        self.f_b = Button(self.root, text=f'File: {filename}', bg='grey25', fg='white', command=browsefile, relief=FLAT)  # Label to show file name
        self.f_b.place(x=10, y=10)

        search_button = Button(self.root, text='Search Chat', width=15, command=searchloop.run,  relief=FLAT, bg='grey25', fg='white')  # button for witching to Search window
        search_button.place(x=500, y=10)

        self.stats = Label(self.root, text=str(), width=60, bg='grey25', fg='white', anchor='w')                     # labels for stats
        self.stats2 = Label(self.root, text=str(), width=60, bg='grey25', fg='white', anchor='w')
        self.stats.place(x=10, y=40)
        self.stats2.place(x=10, y=470)
        
        with suppress(AttributeError):                                                                              # tries to destroy the searchloop window and if it sucseeds, reopens its old stats
            searchloop.root.destroy()
            browsefile(reopen=False)

        self.root.mainloop()

searchloop = search_window()
mainloop = main()
mainloop.run()
