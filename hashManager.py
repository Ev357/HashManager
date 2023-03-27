#!/usr/bin/python3
import tkinter as tk, tkinter.messagebox as mb, tkinter.filedialog as fd, json, sqlite3 as sl, atexit, signal, os, pyperclip, platform;from PIL import Image, ImageTk

#Settings
itemsWidth = 100 #in %, can be more than a hundred. I think this is what you are looking for ;D
askForDeleteConfirmation = True
sqliteDebug = False
deleteDataOnStartup = False
resetTerminalAfterClosing = True
programColors = "Custom" #Just type anything else if you wanna default tk

#Detect OS
if "parrot" not in platform.release():
    osName = "parrot"
else:
    osName = "other"

#Tkinter setup stuff
root = tk.Tk()
root.title("Hash Manager")
icon = tk.PhotoImage(file='./assets/icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.wait_visibility(root)
root.wm_attributes("-alpha", 0.95)

#Atexit
@atexit.register 
def mexit():
    slExit()
    print("\nBye :)")
    if resetTerminalAfterClosing:
        os.system("reset")
signal.signal(signal.SIGTERM, mexit)
signal.signal(signal.SIGINT, mexit)

#Variables
if osName != "parrot" or programColors == "Custom":
    defColor = "#383c4a"
    abbColor = "#434859"
    fgColor = "#000000"
    afbColor = "#000000"
    fgColor = "#000000"
else:
    defColor = root.cget('bg')
    tmpData = tk.Checkbutton(root)
    abbColor = tmpData.cget("activebackground")
    afbColor = tmpData.cget("activeforeground")
    tmpData.destroy()
    tmpData = tk.Label(root)
    fgColor = tmpData.cget("fg")
    tmpData.destroy()
fcd = os.path.dirname(os.path.realpath(__file__)) + '/'
swidth = root.winfo_screenwidth()
sheigth = root.winfo_screenheight()
rooticonsize = 30
imagesize = 30
frames = {}
widgets = {}
select_all = tk.StringVar()
cracked = tk.StringVar()
match = tk.StringVar()
uentry = tk.StringVar()
hentry = tk.StringVar()
pentry = tk.StringVar()
entryData = {0: "", 1: "", 2: ""}
match_state = 0
chosen = {}
photos = {}
d = {}
e = {}
iList = []
ss = []
sss = None
photos['selected_all'] = ImageTk.PhotoImage(Image.open(fcd + './assets/selected_all.png').resize((rooticonsize, rooticonsize)))
photos['unselected_all'] = ImageTk.PhotoImage(Image.open(fcd + './assets/unselected_all.png').resize((rooticonsize, rooticonsize)))
photos['edit'] = ImageTk.PhotoImage(Image.open(fcd + './assets/edit.png').resize((rooticonsize, rooticonsize)))
photos['delete'] = ImageTk.PhotoImage(Image.open(fcd + './assets/delete.png').resize((rooticonsize, rooticonsize)))
photos['upload'] = ImageTk.PhotoImage(Image.open(fcd + './assets/upload.png').resize((rooticonsize, rooticonsize)))
photos['export'] = ImageTk.PhotoImage(Image.open(fcd + './assets/export.png').resize((rooticonsize, rooticonsize)))
photos['add'] = ImageTk.PhotoImage(Image.open(fcd + './assets/add.png').resize((rooticonsize, rooticonsize)))
stop_run_continuously = None
fr = "SELECT * FROM data;"

#Sqlite stuff
conn = None

if not os.path.exists("db"):
    os.makedirs("db")

if deleteDataOnStartup:
    os.system(f"rm {fcd}./db/database.db")
try:
    conn = sl.connect(fcd + "./db/database.db")
except sl.Error as e:
    mb.showerror(title='Error', message=e)

def slExec(cmd, s=conn):
    try:
        cur = s.cursor()
        if isinstance(cmd, str):
            cur.execute(cmd)
        elif isinstance(cmd, list):
            cur.execute(cmd[0], tuple(cmd[1]))
        s.commit()
        if sqliteDebug:
            print(str(cmd) + "\n-------------------------------------------------------")
        return cur.fetchall()
    except sl.Error as e:
        if sqliteDebug:
            print(str(cmd) + "\n------------------------ Error ------------------------\n" + str(e))
        return e

def slExit():
    conn.close()

slExec('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, username TEXT, hash TEXT, password TEXT, state BOOLEAN, UNIQUE(username, hash, password, state));')

#Functions
def qm(index):
    x = ""
    for _ in range(index):
        x += '?, '
    return x[:-2]

def selAll():
    if int(select_all.get()) == 1:
        color = 'grey'
        su = True
    else:
        color = defColor
        su = False
    
    for w1 in frames['dataframe'].winfo_children():
            for widget in w1.winfo_children():
                widget.configure(bg=color)
    for _ in iList:
        chosen[_] = su
    updateSelected()

def edit():
    global ss, sss
    edWidgets = {}
    edFrames = {}
    toEdit = []
    for key, value in chosen.items():
        if value == True:
            toEdit.append(key)
    if len(toEdit) == 1:
        title = "Edit Account"
        multiple = False
    elif len(toEdit) != 0:
        title = "Edit Accounts"
        multiple = True

    if toEdit:
        edWindow = tk.Toplevel(root)
        edWindow.title(title)
        edWindow.tk.call('wm', 'iconphoto', edWindow._w, icon)
        edWindow.geometry(f"+{int(swidth / 4.2)}+{int(sheigth / 3)}")
        edWindow.wait_visibility(edWindow)
        edWindow.wm_attributes("-alpha", 0.95)
        edUname = tk.StringVar()
        edHash = tk.StringVar()
        edPass = tk.StringVar()
        edCracked = tk.StringVar()
        edUentry = tk.StringVar()
        edHentry = tk.StringVar()
        edPentry = tk.StringVar()
        edSize = 30

        def slEdit():
            if multiple:
                if edUentry.get() != "" and edHentry.get() != "":
                    finalData = [int(edUname.get()), int(edHash.get()), int(edPass.get()), int(edCracked.get()), edUentry.get(), edHentry.get(), edPentry.get()]
                    comma = False
                    slArray = []
                    sql = "UPDATE data SET "
                    if finalData[0] == 0:
                        sql += "username = ?"
                        slArray.append(finalData[4])
                        comma = True
                    if finalData[1] == 0:
                        if comma:
                            sql += ', '
                        sql += "hash = ?"
                        slArray.append(finalData[5])
                        comma = True
                    if finalData[2] == 0:
                        if comma:
                            sql += ', '
                        if finalData[3] == 1:
                            sql += "password = ?, state = 1"
                            slArray.append(finalData[6])
                        else:
                            sql += 'password = "", state = 0'
                    sql += f' WHERE id IN ({str(toEdit)[1:-1]});'
                    answer = slExec([sql, slArray])
                    if "UNIQUE constraint failed" in str(answer):
                        mb.showerror(title='Error', message="Account already exists!", parent=edWindow)
                    else:
                        loadData()
                        edWindow.destroy()
                else:
                    mb.showerror(title='Error', message="Username and Password fields can't be empty!", parent=edWindow)
            else:
                if edUentry.get() != "" and edHentry.get() != "":
                    answer = slExec(["UPDATE data SET username = ?, hash = ?, password = ?, state = ? WHERE id LIKE ?;", [edUentry.get(), edHentry.get(), edPentry.get(), int(edCracked.get()), toEdit[0]]])
                    if "UNIQUE constraint failed" in str(answer):
                        mb.showerror(title='Error', message="Account already exists!", parent=edWindow)
                    else:
                        loadData()
                        edWindow.destroy()
                else:
                    mb.showerror(title='Error', message="Username and Password fields can't be empty!", parent=edWindow)

        def disEntry():
            if multiple:
                if int(edPass.get()) == 0 and multiple:
                    if int(edCracked.get()) == 1:
                        eState = tk.NORMAL
                        edPass.set(0)
                    else:
                        eState = tk.DISABLED
                        edPentry.set("")
                    edWidgets['pentry'].configure(state=eState)
            else:
                if int(edCracked.get()) == 1:
                    eState = tk.NORMAL
                else:
                    eState = tk.DISABLED
                    edPentry.set("")
                edWidgets['pentry'].configure(state=eState)

        def organize():
            global ss, sss
            sn = [int(edUname.get()), int(edHash.get()), int(edPass.get())]
            x = 0
            cBox = None
            for _ in sn:
                if ss[x] != _:
                    cBox = x
                    break
                x += 1
            ss = sn
            if sn[0] == 1:
                edUentry.set('*')
                edWidgets['uentry'].configure(state=tk.DISABLED)
            elif cBox == 0:
                edUentry.set("")
                edWidgets['uentry'].configure(state=tk.NORMAL)
            if sn[1] == 1:
                edHentry.set('*')
                edWidgets['hentry'].configure(state=tk.DISABLED)
            elif cBox == 1:
                edHentry.set("")
                edWidgets['hentry'].configure(state=tk.NORMAL)

            if sn[2] == 1:
                edPass.set(1)
                edWidgets['cracked'].pack_forget()
                edPentry.set('*')
                edWidgets['pentry'].configure(state=tk.DISABLED)
            else:
                edWidgets['cracked'].pack(anchor=tk.NE, side=tk.RIGHT)
                if sss == 0:
                    edCracked.set(0)
                if cBox == 2:
                    edPentry.set("")
            disEntry()

        edFrames['cframe'] = tk.Frame(edWindow)
        edFrames['cframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.X)

        edFrames['lbframe'] = tk.Frame(edWindow)
        edFrames['lbframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.X)

        edFrames['eframe'] = tk.Frame(edWindow)
        edFrames['eframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.X)

        edWidgets["cracked"] = tk.Checkbutton(
            edFrames['cframe'], 
            variable=edCracked,
            text='cracked',
            onvalue=1,
            offvalue=0,
            command=disEntry,
            selectcolor=defColor,
            activebackground=abbColor,
            activeforeground=afbColor,
            fg=fgColor
        )
        edWidgets['cracked'].pack(anchor=tk.NE, side=tk.RIGHT)
        edCracked.set(1)

        edCheckbuttons = [
            {'widget': 'ucheck','text': 'Usernames', 'command': 'uname', 'variable': edUname},
            {'widget': 'hcheck', 'text': 'Hashes', 'command': 'pass', 'variable': edHash},
            {'widget': 'pcheck', 'text': 'Passwords', 'command': 'hash', 'variable': edPass}
        ]
        if multiple:
            for _ in edCheckbuttons:
                edWidgets[_['widget']] = tk.Checkbutton(
                    edFrames['cframe'], 
                    variable=_['variable'],
                    text=_['text'],
                    onvalue=1,
                    offvalue=0,
                    command=organize,
                    selectcolor=defColor,
                    activebackground=abbColor,
                    activeforeground=afbColor,
                    fg=fgColor
                )
                edWidgets[_['widget']].pack(anchor=tk.NW, side=tk.LEFT)

        edLabels = [
            {'widget': 'ulabel', 'text': 'Username'}, 
            {'widget': 'hlabel', 'text': 'Hash'}, 
            {'widget': 'plabel', 'text': 'Password'}
        ]

        for _ in edLabels:
            edWidgets[_['widget']] = tk.Label(
                edFrames['lbframe'],
                text=_['text'],
                relief=tk.RAISED,
                width=edSize,
                fg=fgColor
            )
            edWidgets[_['widget']].pack(fill=tk.X, side=tk.LEFT, expand=True)

        edEntries = [
            {'widget': 'uentry', 'variable': edUentry}, 
            {'widget': 'hentry', 'variable': edHentry}, 
            {'widget': 'pentry', 'variable': edPentry}
        ]

        for _ in edEntries:
            edWidgets[_['widget']] = tk.Entry(
                edFrames['eframe'], 
                textvariable=_['variable'],
                width=edSize,
                disabledbackground="grey",
                disabledforeground="black",
                fg=fgColor
            )
            edWidgets[_['widget']].pack(fill=tk.X, side=tk.LEFT, expand=True)

        if multiple:
            accounts = slExec([f"SELECT * FROM data WHERE id IN ({qm(len(toEdit))});", toEdit])
            tmpData = ['uname', 'hash', 'pass']
            same = {}
            same['uname'] = accounts[0][1]
            same['hash'] = accounts[0][2]
            same['pass'] = accounts[0][3]
            same['state'] = accounts[0][4]
            same['states'] = {'uname': True, 'hash': True, 'pass': True}
            for _ in accounts:
                x = 1
                for _1 in tmpData:
                    if _[x] != same[_1]:
                        same['states'][_1] = False
                    x += 1
            sss = 0
            for _ in accounts:
                if _[4] == 1:
                    sss = 1
                    break
            tmpData = {'uname': edUname, 'hash': edHash, 'pass': edPass}
            tmpData2 = {'uname': edUentry, 'hash': edHentry, 'pass': edPentry}
            x = 1
            for key, value in same['states'].items():
                if value:
                   v = 0
                   tmpData2[key].set(accounts[0][x])
                else:
                   v = 1
                tmpData[key].set(v)
                x += 1
            ss = [int(edUname.get()), int(edHash.get()), int(edPass.get())]
            organize()

        else:
            account = slExec(["SELECT * FROM data WHERE id LIKE ?;", [toEdit[0]]])[0]
            edUentry.set(account[1])
            edHentry.set(account[2])
            edPentry.set(account[3])
            edCracked.set(account[4])
            disEntry()

        edWidgets['save'] = tk.Button(
            edWindow, 
            command=slEdit, 
            text="Save",
            activebackground=abbColor,
            activeforeground=afbColor,
            fg=fgColor
        )
        edWidgets['save'].pack(anchor=tk.SE, side=tk.RIGHT)

        if osName != "parrot" or programColors == "Custom":
            edWindow.configure(background=defColor, highlightbackground=defColor)
            for key, value in edFrames.items():
                if key == 'eframe':
                    for _ in value.winfo_children():
                        _.configure(background=defColor, highlightbackground=defColor)
                    continue
                if key == 'lbframe':
                    for _ in value.winfo_children():
                        _.configure(background=defColor, highlightbackground=defColor)
                    continue
                value.configure(background=defColor, highlightbackground=defColor)
            for key, value in edWidgets.items():
                value.configure(background=defColor, highlightbackground=defColor)

        edWindow.transient(root)
        edWindow.grab_set()
        root.wait_window(edWindow)

def add():
    addWidgets = {}
    addFrames = {}
    addWindow = tk.Toplevel(root)
    addWindow.title("Add Account")
    addWindow.tk.call('wm', 'iconphoto', addWindow._w, icon)
    addWindow.geometry(f"+{int(swidth / 4.2)}+{int(sheigth / 3)}")
    addWindow.wait_visibility(addWindow)
    addWindow.wm_attributes("-alpha", 0.95)
    addCracked = tk.StringVar()
    addUentry = tk.StringVar()
    addHentry = tk.StringVar()
    addPentry = tk.StringVar()
    addSize = 30

    def slAdd():
        if addUentry.get() != "" and addHentry.get() != "":
            answer = slExec(["INSERT INTO data (username, hash, password, state) VALUES(?, ?, ?, ?);", [addUentry.get(), addHentry.get(), addPentry.get(), int(addCracked.get())]])
            if "UNIQUE constraint failed" in str(answer):
                mb.showerror(title='Error', message="Account already exists!", parent=addWindow)
            else:
                loadData()
                addWindow.destroy()
        else:
            mb.showerror(title='Error', message="Username and Password fields can't be empty!", parent=addWindow)

    def disEntry():
        if int(addCracked.get()) == 1:
            eState = tk.NORMAL
        else:
            eState = tk.DISABLED
            addPentry.set("")
        addWidgets['pentry'].configure(state=eState)

    addWidgets["cracked"] = tk.Checkbutton(
        addWindow, 
        variable=addCracked,
        text='cracked',
        onvalue=1,
        offvalue=0,
        command=disEntry,
        selectcolor=defColor,
        activebackground=abbColor,
        activeforeground=afbColor,
        fg=fgColor
    )
    addWidgets['cracked'].pack(anchor=tk.NE, side=tk.TOP)
    addCracked.set(1)

    addLabels = [
        {'widget': 'ulabel', 'text': 'Username'}, 
        {'widget': 'hlabel', 'text': 'Hash'}, 
        {'widget': 'plabel', 'text': 'Password'}
    ]

    addFrames['lbframe'] = tk.Frame(addWindow)
    addFrames['lbframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.X)

    addFrames['eframe'] = tk.Frame(addWindow)
    addFrames['eframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.X)

    for _ in addLabels:
        addWidgets[_['widget']] = tk.Label(
            addFrames['lbframe'],
            text=_['text'],
            relief=tk.RAISED,
            width=addSize,
            fg=fgColor
        )
        addWidgets[_['widget']].pack(fill=tk.X, side=tk.LEFT, expand=True)

    addEntries = [
        {'widget': 'uentry', 'variable': addUentry}, 
        {'widget': 'hentry', 'variable': addHentry}, 
        {'widget': 'pentry', 'variable': addPentry}
    ]

    for _ in addEntries:
        addWidgets[_['widget']] = tk.Entry(
            addFrames['eframe'], 
            textvariable=_['variable'],
            width=addSize,
            fg=fgColor
        )
        addWidgets[_['widget']].pack(fill=tk.X, side=tk.LEFT, expand=True)
    addWidgets['pentry'].configure(disabledbackground="grey")

    addWidgets['add'] = tk.Button(
        addWindow, 
        command=slAdd, 
        text="Add",
        activebackground=abbColor,
        activeforeground=afbColor,
        fg=fgColor
    )
    addWidgets['add'].pack(anchor=tk.SE, side=tk.RIGHT)

    if osName != "parrot" or programColors == "Custom":
        addWindow.configure(background=defColor, highlightbackground=defColor)
        for key, value in addFrames.items():
            value.configure(background=defColor, highlightbackground=defColor)
        for key, value in addWidgets.items():
            value.configure(background=defColor, highlightbackground=defColor)

    addWindow.transient(root)
    addWindow.grab_set()
    root.wait_window(addWindow)

def delete():
    toDelete = []
    for key, value in chosen.items():
        if value == True:
            toDelete.append(key)
    if toDelete and (askForDeleteConfirmation == False or mb.askyesno(title='Confirmation', message=f'Do you really want to delete {len(toDelete)} items?')):
        slExec([f"DELETE FROM data WHERE id IN ({qm(len(toDelete))});", toDelete])
        loadData()

def upload():
    filetypes = (
        ('SQLite 3.x Database Files', '*.db'),
        ('All Files', '*.*')
    )
    filenames = fd.askopenfilenames(
        title='Open Files',
        initialdir=fcd,
        filetypes=filetypes
    )
    for _ in filenames:
        slExec(['ATTACH DATABASE ? AS new_db;', [_]])
        slExec('INSERT OR IGNORE INTO data (username, hash, password, state) SELECT username, hash, password, state FROM new_db.data;')
        slExec('DETACH DATABASE new_db;')
    if len(filenames) != 0:
        loadData()

def export():
    filetypes = (
        ('SQLite 3.x Database Files', '*.db'),
        ('All Files', '*.*')
    )
    filename = fd.asksaveasfilename(filetypes=filetypes, initialdir=fcd)
    if filename:
        try:
            eConn = sl.connect(filename)
        except sl.Error as e:
            mb.showerror(title='Error', message=e)
        slExec('CREATE TABLE IF NOT EXISTS data (username TEXT, hash TEXT, password TEXT, state BOOLEAN, UNIQUE(username, hash, password, state));', eConn)
        slExec(["ATTACH DATABASE ? AS new_db;", [fcd + "db/database.db"]], eConn)
        slExec('INSERT INTO data (username, hash, password, state) SELECT username, hash, password, state FROM new_db.data;', eConn)
        slExec('DETACH DATABASE new_db;', eConn)
        eConn.close()

def choose(x):
    def check():
        if "False" not in str(chosen) and len(chosen) == len(iList):
                select_all.set(1)

    if chosen.__contains__(x):
        if chosen[x]:
            color = defColor
            chosen[x] = False
            try:
                if int(select_all.get()) == 1:
                    select_all.set(0)
            except:
                pass
        else:
            color = 'grey'
            chosen[x] = True
            check()
    else:
        color = 'grey'
        chosen[x] = True
        check()
    for widget in d[x].winfo_children():
            widget.configure(bg=color)
    updateSelected()

def copy(dataToCopy):
    pyperclip.copy(frames['dataframe'].winfo_children()[iList.index(dataToCopy[0])].winfo_children()[dataToCopy[1]].cget("text"))

def loadData(data=None):
    global chosen, iList, d, e, fr
    data = fr
    rows = slExec(data)
    for widget in frames['dataframe'].winfo_children():
        widget.destroy()
    d = {}
    e = {}
    iList = []
    x = 0
    for _0 in rows:
        d[_0[0]] = tk.Frame(frames['dataframe'])
        d[_0[0]].pack(anchor=tk.N, side=tk.TOP, fill=tk.X, expand=True)

        dataLabel = [_0[1], _0[2], _0[3]]
        iList.append(_0[0])

        y = 0
        for _1 in dataLabel:
            if y != 0:
                w = int(swidth / 24 * itemsWidth / 100)
            else:
                w = int(swidth / 24.1 * itemsWidth / 100)
            e[y] = tk.Label(
                d[_0[0]],
                text=dataLabel[y],
                relief=tk.GROOVE,
                width=w,
                fg=fgColor
            )
            e[y].pack(fill=tk.X, expand=True, side=tk.LEFT, anchor=tk.N)
            exec(f"e[y].bind('<Button-1>', lambda eff: choose({_0[0]}))")
            exec(f"e[y].bind('<Button-3>', lambda eff: copy([{_0[0]}, {y}]), add='+')")
            if osName != "parrot" or programColors == "Custom":
                e[y].configure(background=defColor)
            e[y].focus()
            y += 1
        x += 1
    chosen = {}
    updateTotal(len(rows))
    select_all.set(0)

def reloadData(event=None):
    global fr, match_state
    if int(cracked.get()) == 1:
        c = 1
    else:
        c = '%'
    if int(match.get()) == 0:
        fr = ['SELECT * FROM data WHERE username LIKE ? AND hash LIKE ? AND password LIKE ? AND state LIKE ?;', ['%' + pentry.get() + '%', '%' + hentry.get() + '%', '%' + uentry.get() + '%', c]]
    else:
        tmpData = [uentry.get(), hentry.get(), pentry.get()]
        uhp = []
        for _ in tmpData:
            if _ == "":
                uhp.append('%')
            else:
                uhp.append(_)
        fr = ['SELECT * FROM data WHERE username LIKE ? AND hash LIKE ? AND password LIKE ? AND state LIKE ?;', [uhp[2], uhp[1], uhp[0], c]]
    if not (match_state != int(match.get()) and (uentry.get() == "" and hentry.get() == "" and pentry.get() == "")):
        loadData()
    match_state = int(match.get())
        

def updateTotal(total):
    widgets['total'].configure(text='total: ' + str(total))
    updateSelected()

def updateSelected():
    x = 0
    for key, value in chosen.items():
        if value == True:
            x += 1
    widgets['selected'].configure(text='   selected: ' + str(x))

#Configure Frames
frames['lrframe'] = tk.Frame(root)
frames['lrframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH, pady=(0, 1))

frames['lframe'] = tk.Frame(frames['lrframe'])
frames['lframe'].pack(anchor=tk.NW, side=tk.LEFT)

frames['rframe'] = tk.Frame(frames['lrframe'])
frames['rframe'].pack(anchor=tk.NE, side=tk.RIGHT)

frames['mainframe'] = tk.Frame(root, relief=tk.RAISED)
frames['mainframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH, expand=True)

frames['infoframe'] = tk.Frame(root)
frames['infoframe'].pack(anchor=tk.SW, side=tk.BOTTOM)

frames['eframe'] = tk.Frame(frames['mainframe'])
frames['eframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH)

frames['lbframe'] = tk.Frame(frames['mainframe'])
frames['lbframe'].pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH)

frames['container'] = tk.Frame(frames['mainframe'])
frames['container'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frames['canvas'] = tk.Canvas(frames['container'])
frames['canvas'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frames['scrollbar'] = tk.Scrollbar(frames['mainframe'], orient="vertical", command=frames['canvas'].yview)
frames['scrollbar'].pack(anchor=tk.E, side="right", fill=tk.Y)
frames['dataframe'] = tk.Label(frames['canvas'])

frames['dataframe'].bind(
    "<Configure>",
    lambda e: frames['canvas'].configure(
        scrollregion=frames['canvas'].bbox("all")
    )
)

frames['canvas'].create_window((0, 0), window=frames['dataframe'], anchor=tk.NW)
frames['canvas'].configure(yscrollcommand=frames['scrollbar'].set)

#Configure Widgets
widgets['select_all'] = tk.Checkbutton(
    frames['lframe'], 
    variable=select_all, 
    onvalue=1, 
    offvalue=0,
    command=selAll,
    image=photos['unselected_all'], 
    selectimage=photos['selected_all'],
    indicatoron=False, 
    selectcolor=defColor,
    width=imagesize + 2, 
    height=imagesize + 2,
    activebackground=abbColor,
    activeforeground=afbColor,
)
widgets['select_all'].pack(side=tk.LEFT, padx=(2, 0), expand=True)
select_all.set(0)

buttons = [
    {'widget': 'edit_bt', 'frame': 'lframe', 'function': edit,'photo': 'edit', 'side': tk.LEFT},
    {'widget': 'add', 'frame': 'lframe', 'function': add,'photo': 'add', 'side': tk.LEFT},
    {'widget': 'delete', 'frame': 'lframe', 'function': delete, 'photo': 'delete', 'side': tk.LEFT},
    {'widget': 'upload', 'frame': 'rframe', 'function': upload, 'photo': 'upload', 'side': tk.RIGHT}, 
    {'widget': 'export', 'frame': 'rframe', 'function': export, 'photo': 'export', 'side': tk.RIGHT}
]

for _ in buttons:
    widgets[_['widget']] = tk.Button(
        frames[_['frame']], 
        command=_['function'], 
        image=photos[_['photo']],
        width=imagesize, 
        height=imagesize,
        activebackground=abbColor,
        activeforeground=afbColor
    )
    widgets[_['widget']].pack(side=_['side'], expand=True)
widgets['upload'].pack(padx=(0, 2))

widgets['match'] = tk.Checkbutton(
    frames['rframe'], 
    variable=match,
    text='match case',
    onvalue=1,
    offvalue=0,
    selectcolor=defColor,
    command=reloadData,
    activebackground=abbColor,
    activeforeground=afbColor,
    fg=fgColor
)
match.set(0)
widgets['match'].pack(anchor=tk.SE, side=tk.RIGHT, expand=True)

widgets['cracked'] = tk.Checkbutton(
    frames['rframe'], 
    variable=cracked,
    text='cracked',
    onvalue=1,
    offvalue=0,
    selectcolor=defColor,
    command=reloadData,
    activebackground=abbColor,
    activeforeground=afbColor,
    fg=fgColor
)
cracked.set(0)
widgets['cracked'].pack(anchor=tk.SE, side=tk.RIGHT, expand=True)

entries = [
    {'widget': 'uentry', 'variable': uentry}, 
    {'widget': 'hentry', 'variable': hentry}, 
    {'widget': 'pentry', 'variable': pentry}
]

for _ in entries:
    widgets[_['widget']] = tk.Entry(
        frames['eframe'], 
        textvariable=_['variable'],
        width=1,
        fg=fgColor
    )
    widgets[_['widget']].pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    widgets[_['widget']].bind('<FocusOut>', reloadData)
    widgets[_['widget']].bind('<Return>', reloadData, add='+')

labels = [
    {'widget': 'ulabel', 'text': 'Username'}, 
    {'widget': 'hlabel', 'text': 'Hash'}, 
    {'widget': 'plabel', 'text': 'Password'}
]

for _ in labels:
    widgets[_['widget']] = tk.Label(
        frames['lbframe'],
        text=_['text'],
        relief=tk.RAISED,
        width=1,
        fg=fgColor
    )
    widgets[_['widget']].pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

widgets['total'] = tk.Label(frames['infoframe'], fg=fgColor)
widgets['total'].pack(side=tk.LEFT)

widgets['selected'] = tk.Label(frames['infoframe'], fg=fgColor)
widgets['selected'].pack(side=tk.LEFT)

loadData()

if osName != "parrot" or programColors == "Custom":
    root.configure(background=defColor)
    for key, value in frames.items():
        value.configure(background=defColor, highlightbackground=defColor)
    for key, value in widgets.items():
        value.configure(background=defColor, highlightbackground=defColor)

#Mainloop
try:
    root.mainloop()
except:
    pass #Perfection!!!
