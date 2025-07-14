import tkinter as tk
from tkinter import ttk, font
from DataHandler import DataHandler as dh
import threading
from RouterHandler import RouterConnecter as RC
from RouterHandler import PPPoePull as PPull
import sys
import ctypes
import win32con
import win32gui
import win32api
import os
import time



class ControlPanel():


    def __init__(self, root):
        self.root = root
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "icon.ico")
        self.root.iconbitmap(icon_path)
        self.root.geometry("500x500")
        self.root.title('MikroPPPull')
        self.filterRouterAndPPPoeList = {}
        self.fontx = font.Font(family='Courier New', size=12) 
        self.fontxmini = font.Font(family='Courier New', size=8)
        self.fontx2mini = font.Font(family='Courier New', size=6)
        self.selectedserver = ''
        self.selectedPPPoe = ''
        self.onsearch = False

        #root.overrideredirect(True)
        self.root.update_idletasks()


        self.colorpallete = {
            'bg' : '#10141f',
            'shadow' : '#090a14',
            'btn' : '#151d28',
            'txtcolor' : '#4f8fba',
            'hover' : '#411d31',
            'pressed' : '#241527',
            'hovertxt' : '#a53030'
        }
        self.root.configure(bg = self.colorpallete['bg'])
        self.fncConfigStyle()
        self.fncCreateInterface()
        self.fncInitSyncRouterData()

    def remove_bar(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("your.app.id")
        hwnd = win32gui.FindWindow(None, "MikroPPPull")
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        style = style & ~win32con.WS_CAPTION & ~win32con.WS_THICKFRAME
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
        win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE |
                            win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)

    def fncStartmove(self, event):
        self._offset_x = event.x_root - self.root.winfo_x()
        self._offset_y = event.y_root - self.root.winfo_y()

    def fncMovewindow(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        #self.root.geometry(f"+{x}+{y}")
        hwnd = win32gui.FindWindow(None, "MikroPPPull") 
        win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

    def fncCreateInterface(self):
        self.exitframe = ttk.Frame(self.root, style="Dark.TFrame", height=30)
        self.exitframe.pack(side='top', fill='x')
        self.exitframe.bind('<Button-1>', self.fncStartmove)
        self.exitframe.bind('<B1-Motion>', self.fncMovewindow)
        exitBtn = ttk.Button(self.exitframe, width=3, style="Dark.TButton", command=lambda: sys.exit(0), text='X')
        exitBtn.pack(side='right', padx=7, pady=10)
        minimBtn = ttk.Button(self.exitframe, width=3, style="Dark.TButton", command=self.root.iconify, text='-')
        minimBtn.pack(side='right', padx=5, pady=10)
        self.mainframe = ttk.Frame(self.root, style="Dark.TFrame")
        self.mainframe.pack(expand=True, fill=tk.BOTH)
        self.fncCreateHeader(self.exitframe)
        self.fncNotebook(self.mainframe)


    def fncConfigStyle(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TNotebook', background=self.colorpallete['bg'], darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'], font=self.fontx )
        style.configure('Dark.TNotebook.Tab', background=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'], padding=[10, 10], font=self.fontx)
        style.map('Dark.TNotebook.Tab', 
                  background=[('selected', self.colorpallete['hover'])],
                  foreground=[('selected', self.colorpallete['hovertxt'])],
                  bordercolor=[('selected', self.colorpallete['hovertxt'])],
                  lightcolor=[('selected', self.colorpallete['hover'])],
                  darkcolor=[('selected', self.colorpallete['pressed'])],
                )
        style.configure('Dark.TEntry', background=self.colorpallete['btn'], fieldbackground=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], font=self.fontx, darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'])
        style.configure('Dark.TFrame', background=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'])
        style.configure('2Dark.TFrame', background=self.colorpallete['btn'], bordercolor=self.colorpallete['bg'])
        style.configure('Dark.TLabel', background=self.colorpallete['bg'], foreground=self.colorpallete['txtcolor'], font=self.fontx)
        style.configure('2Dark.TLabel', background=self.colorpallete['bg'], foreground=self.colorpallete['txtcolor'], font=self.fontxmini)
        style.configure('4Dark.TLabel', background=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], font=self.fontxmini)
        style.configure('Dark.TButton', background=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], font=self.fontx, darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'])
        style.map('Dark.TButton', 
                  background=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hover']), ('disabled', self.colorpallete['shadow'])],
                  foreground=[('pressed', self.colorpallete['pressed']), ('active', self.colorpallete['hovertxt']), ('disabled', self.colorpallete['shadow'])],
                  bordercolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hovertxt'])],
                  lightcolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hover'])],
                  darkcolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['pressed'])]
                  )
        style.configure('2Dark.TButton', background=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], font=self.fontxmini, darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'])
        style.map('2Dark.TButton', 
                  background=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hover']), ('disabled', self.colorpallete['shadow'])],
                  foreground=[('pressed', self.colorpallete['pressed']), ('active', self.colorpallete['hovertxt']), ('disabled', self.colorpallete['shadow'])],
                  bordercolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hovertxt'])],
                  lightcolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['hover'])],
                  darkcolor=[('pressed', self.colorpallete['shadow']), ('active', self.colorpallete['pressed'])]
                  )
        style.configure('Dark.Vertical.TScrollbar', background=self.colorpallete['bg'], troughcolor=self.colorpallete['shadow'],darkcolor=self.colorpallete['shadow'], lightcolor=self.colorpallete['bg'], bordercolor=self.colorpallete['shadow'], arrowcolor=self.colorpallete['txtcolor'] )
        style.map('Dark.Vertical.TScrollbar', 
                  background=[('active', self.colorpallete['hover'])],
                  arrowcolor=[('active', self.colorpallete['hovertxt'])],
                  bordercolor=[('active', self.colorpallete['hovertxt'])],
                  lightcolor=[('active', self.colorpallete['hover'])],
                  darkcolor=[('active', self.colorpallete['pressed'])]
                  )
        style.configure('3Dark.TLabel', background=self.colorpallete['btn'], foreground=self.colorpallete['txtcolor'], font=self.fontx)


    def fncCreateHeader(self, parent):
        CPanelLabel = ttk.Label(parent, style='Dark.TLabel', text="MikroPPPull")
        CPanelLabel.bind('<Button-1>', self.fncStartmove)
        CPanelLabel.bind('<B1-Motion>', self.fncMovewindow)
        CPanelLabel.pack(side=tk.LEFT, pady=10, padx=10)

    def fncNotebook(self, parent):
        self.CpanelNotebook = ttk.Notebook(parent, style='Dark.TNotebook')
        self.CpanelNotebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.fncDashboard()
        self.fncPPPull()
    
    def fncDashboard(self):
        DashboardFrame = ttk.Frame(self.CpanelNotebook, style='Dark.TFrame')
        self.CpanelNotebook.add(DashboardFrame, text='Server Panel')
        self.fncAddandImportbtn(DashboardFrame)
        self.fncScrolllist(DashboardFrame)
    
    def fncPPPull(self):
        PPPullFrame = ttk.Frame(self.CpanelNotebook, style='Dark.TFrame', padding=3)
        self.CpanelNotebook.add(PPPullFrame, text='PPPoe Menu')
        self.fncPPPullMenu(PPPullFrame)
    
    def fncPPPullMenu(self, parent):
        self.PPPullMainFrame = ttk.Frame(parent, padding=2, style='2Dark.TFrame')
        self.PPPullMainFrame.pack(fill='both', expand=True)
        SearchFrame = ttk.Frame(self.PPPullMainFrame, padding=2, height=35, style='Dark.TFrame')
        SearchFrame.pack(fill='x', side='top', padx=2, pady=2)
        self.SearchVar = tk.StringVar()
        self.SearchLabel = ttk.Label(SearchFrame, padding=2, style='Dark.TLabel', text='Search : ').grid(row=0, column=0)
        self.SearchEntry = ttk.Entry(SearchFrame, style='Dark.TEntry', width=55, textvariable=self.SearchVar, state='disabled')
        self.SearchEntry.grid(row=0, column=1)
        self.SearchEntry.bind("<Return>", self.fnconsearch)
        self.RefreshBtn = ttk.Button(SearchFrame, padding=2, style='Dark.TButton', width=2, text='\uE895', command=self.fncStartRefreshThread, state='disabled')
        self.RefreshBtn.grid(row=0, column=2, padx=5)
        ServerListFrame = ttk.Frame(self.PPPullMainFrame, width=120, style='Dark.TFrame')
        ServerListFrame.pack(side='left', fill='y', padx=2, pady=2)
        self.ServerListCanvas = tk.Canvas(ServerListFrame, background=self.colorpallete['bg'], borderwidth=0, highlightthickness=0, width=100)
        ServerScroll = ttk.Scrollbar(ServerListFrame, style='Dark.Vertical.TScrollbar', orient='vertical', command=self.ServerListCanvas.yview)
        self.ServerListItemContainer = ttk.Frame(self.ServerListCanvas, padding=1, style='Dark.TFrame')
        ServerListItemContainerWindow = self.ServerListCanvas.create_window((0, 0), window=self.ServerListItemContainer, anchor='nw')
        self.ServerListItemContainer.bind('<Configure>', lambda e: self.ServerListCanvas.configure(scrollregion=self.ServerListCanvas.bbox('all')))
        self.ServerListCanvas.bind('<Configure>', lambda e: self.ServerListCanvas.itemconfig(ServerListItemContainerWindow, width=e.width))
        self.ServerListCanvas.configure(yscrollcommand=ServerScroll.set)
        self.ServerListCanvas.pack(fill='both', expand=False, side='left')
        ServerScroll.pack(fill='y', padx=1, side='right')
        PPPoeListFrame = ttk.Frame(self.PPPullMainFrame, padding=2, width=120, style='Dark.TFrame')
        self.PPPoeCanvas = tk.Canvas(PPPoeListFrame, background=self.colorpallete['bg'], borderwidth=0, highlightthickness=0, width=100)
        PPPoeScroll = ttk.Scrollbar(PPPoeListFrame, style='Dark.Vertical.TScrollbar', orient='vertical', command=self.PPPoeCanvas.yview)
        self.PPPoeListItemContainer = ttk.Frame(self.PPPoeCanvas, width=120, style='Dark.TFrame')
        self.PPPoeListItemContainer.bind("<Configure>", lambda e: self.PPPoeCanvas.configure(scrollregion=self.PPPoeCanvas.bbox('all')))
        PPPoeListItemContainerWindow = self.PPPoeCanvas.create_window((0,0), anchor='nw', window=self.PPPoeListItemContainer)
        self.PPPoeCanvas.bind("<Configure>", lambda e: self.PPPoeCanvas.itemconfig(PPPoeListItemContainerWindow, width=e.width))
        PPPoeListFrame.pack(side='left', fill='y', padx=2, pady=2)
        self.PPPoeCanvas.configure(yscrollcommand=PPPoeScroll.set)
        #self.PPPoeDataLabel = ttk.Label(self.PPPullMainFrame, style='4Dark.TLabel', text="", justify='left', anchor='nw', wraplength=210)
        self.PPPoeDataLabel = tk.Text(self.PPPullMainFrame, wrap='word', borderwidth=0, relief='flat', background=self.colorpallete['shadow'], foreground=self.colorpallete['txtcolor'], font=self.fontxmini, state='disabled')
        self.PPPoeDataLabel.pack(side='top', fill='both', expand=True, pady=2)
        self.PPPoeBTN = ttk.Button(self.PPPullMainFrame, text='Monitor', style='2Dark.TButton', command=self.fncPPPoeMonit, state='disabled')
        self.PPPoeBTN.pack(side='bottom', fill='both', pady=2)
        self.PPPoeCanvas.pack(side='left', fill='both', expand=False)
        PPPoeScroll.pack(side='right', fill='y', padx=1)


    def fncAddandImportbtn(self, parent):
        headerx = ttk.Frame(parent, style="Dark.TFrame", height=40)
        headerx.pack(fill='x')
        headerx.pack_propagate(False)
        addbtn = ttk.Button(headerx, style="Dark.TButton", width=2, text='+', command=lambda: self.fncPopUpItem('Add Server'))
        addbtn.pack(side='right', padx=5)
        addbtn.pack_propagate(False)
        importbtn = ttk.Button(headerx, style="Dark.TButton", width=2, text='\uE895', command=lambda: self.fncSync(dh.varRouterServerData))
        importbtn.pack(side='right', padx=5)
        importbtn.pack_propagate(False)


    def fncSync(self, data):
        self.selectedserver = ''
        self.selectedPPPoe = ''
        self.PPPoeBTN.configure(state='disabled')
        for x in self.ServerListItemContainer.winfo_children():
            x.destroy()
        for i in self.PPPoeListItemContainer.winfo_children():
            i.destroy()
            # print(f'PPPoe Height : {self.PPPoeListItemContainer.winfo_height()}')
        self.PPPoeListItemContainer.configure(height=1)
        self.ServerListItemContainer.configure(height=1)
        self.ServerListCanvas.yview_moveto(0)
        self.PPPoeCanvas.yview_moveto(0)
        # print(f'PPPoe Height : {self.PPPoeListItemContainer.winfo_height()}')
        # self.PPPoeListItemContainer.update_idletasks()
        # self.PPPoeCanvas.update_idletasks()
        # self.PPPoeCanvas.configure(scrollregion=self.PPPoeCanvas.bbox("all"))
        # self.ServerListItemContainer.update_idletasks()
        # self.ServerListCanvas.configure(scrollregion=self.ServerListCanvas.bbox('all'))
        self.thr = []
        thrlock = threading.Lock
        if data:
            for i in data:
                if i in dh.varRCInstance.keys():
                    curobj = dh.varRCInstance[i]
                    curobjapi = RC.fncclassGetAPI()[i]['routerapi']
                    curobjapib = RC.fncclassGetAPI()[i]['routerapib']
                    print(f"detected {i} in varRCInstance check {curobj} and {curobjapi} \n")
                    if RC.fncstaticIsisValidAPI(curobjapi) and RC.fncstaticIsisValidAPI(curobjapib):
                        print(f"{curobjapi} is valid bypass current iteration \n")
                        continue
                t = threading.Thread(target=self.fncRC, args=(i, data[i]['ip'], data[i]['username'], data[i]['password'], data[i]['port']), daemon=True)
                self.thr.append(t)
            print(f"fncSync : thread {self.thr} \n")
            for i in self.thr:
                i.start()
            print("fncSync done \n")
            self.fncCheckThread()

    def fncCheckThread(self):
        alive = any(t.is_alive() for t in self.thr)
        if alive:
            self.root.after(100, self.fncCheckThread)
        else:
            # print('adsadsasdads')
            threading.Thread(target=self.fncPopulateServerList, daemon=True).start()


    @staticmethod
    def fncRC(keyx, routerip, router_username, router_password, router_port):
        thrlock = threading.Lock()
        abc = RC(routerip, router_username, router_password, router_port)
        with thrlock:
            dh.varRCInstance[keyx] = abc
        #print(f"fncRC varRCInstance : {dh.varRCInstance} \n")


    def fncPopulateServerList(self, filterRouterList=None, filterRouterAndPPPoeList=None):
        for x in self.ServerListItemContainer.winfo_children():
            x.destroy()
        self.ServerListItemContainer.configure(height=1)
        self.ServerListCanvas.yview_moveto(0)
        for i in self.PPPoeListItemContainer.winfo_children():
            i.destroy()
        self.PPPoeListItemContainer.configure(height=1)
        self.PPPoeCanvas.yview_moveto(0)
        self.RefreshBtn.configure(state='disabled')

        if self.SearchVar.get().strip().lower() != '':
            for name in self.filterRouterAndPPPoeList:
                serverbtn = ttk.Button(self.ServerListItemContainer, padding=1, style='2Dark.TButton', text=name, command=lambda svrname=name: self.fncPopulatePPPoeList(svrname))
                serverbtn.pack(fill='x', padx=1, pady=3)
        else:
            for servername in dh.varRouterServerData:
                serverbtn = ttk.Button(self.ServerListItemContainer, padding=1, style='2Dark.TButton', text=servername, command=lambda svrname=servername: self.fncPopulatePPPoeList(svrname))
                serverbtn.pack(fill='x', padx=1, pady=3)
        self.SearchEntry.configure(state='normal')
    
    def fncStartRefreshThread(self):
        self.selectedPPPoe = ''
        for i in self.PPPoeListItemContainer.winfo_children():
            i.destroy()
        self.PPPoeListItemContainer.configure(height=1)
        self.PPPoeCanvas.yview_moveto(0)
        self.PPPoeBTN.configure(state='disabled')
        self.RefreshBtn.configure(state='disabled')
        self.SearchEntry.configure(state='disabled')
        t = threading.Thread(target=self.fncRefresh, daemon=True)
        t.start()

    def fncRefresh(self):
        if self.selectedserver != '':
            curobj = dh.varRCInstance[self.selectedserver]
            curobj.fncPPPoeRefresh()
            self.root.after(0, lambda: self.fncPopulatePPPoeList(self.selectedserver))
    
    def fncPopulatePPPoeList(self, svrname):
        for i in self.PPPoeListItemContainer.winfo_children():
            i.destroy()
        self.PPPoeListItemContainer.configure(height=1)
        self.PPPoeCanvas.yview_moveto(0)
        #self.PPPoeDataLabel.config(text='')
        self.PPPoeDataLabel.configure(state='normal')
        self.PPPoeDataLabel.delete("1.0", "end")
        self.PPPoeDataLabel.configure(state='disabled')
        self.RefreshBtn.configure(state='disabled')
        self.PPPoeBTN.configure(state='disabled')
        self.selectedPPPoe = ''
        # print(f'fncPopulatePPPoeList : {dh.varRCInstance}')

        curobj = dh.varRCInstance[svrname]
        curobjapi = RC.fncclassGetAPI()[svrname]['routerapi']
        self.selectedserver = svrname
        # if curobjapi:
        #     if curobj.fncstaticIsisValidAPI(curobjapi):
        #         if self.SearchVar.get().strip().lower() != '':
        #             for client in self.filterRouterAndPPPoeList[ipserver]:
        #                 # print(f'fncPop : {client}')
        #                 tbn = ttk.Button(self.PPPoeListItemContainer, text=client['name'], padding=1, style='2Dark.TButton', command=lambda a=client['name']:self.fncShowDetail(a, curobj))
        #                 tbn.pack(fill='x', padx=1, pady=2)
        #         else:
        #             for client in curobj.PPPoeData:
        #                 tbn = ttk.Button(self.PPPoeListItemContainer, text=client['name'], padding=1, style='2Dark.TButton', command=lambda a=client['name']:self.fncShowDetail(a, curobj))
        #                 tbn.pack(fill='x', padx=1, pady=2)
        if curobj:
            if self.SearchVar.get().strip().lower() != '':
                for client in self.filterRouterAndPPPoeList[svrname]:
                    # print(f'fncPop : {client}')
                    tbn = ttk.Button(self.PPPoeListItemContainer, text=client['name'], padding=1, style='2Dark.TButton', command=lambda a=client['name']:self.fncShowDetail(a, curobj))
                    tbn.pack(fill='x', padx=1, pady=2)
            else:
                for client in curobj.PPPoeData:
                    tbn = ttk.Button(self.PPPoeListItemContainer, text=client['name'], padding=1, style='2Dark.TButton', command=lambda a=client['name']:self.fncShowDetail(a, curobj))
                    tbn.pack(fill='x', padx=1, pady=2)
        self.RefreshBtn.configure(state='normal')
        self.SearchEntry.configure(state='normal')
    
    def fncShowDetail(self, name, rcinstance):
        result = [entry for entry in rcinstance.PPPoeData if entry.get('name') == name]
        data = (
            f"PPPoe name : {result[0].get('name', '-')}\n"
            f"Profile : {result[0].get('profile', '-')}\n"
            f"IP Address : {result[0].get('address', '-')} \n"
            f"Comment : {result[0].get('comment', '-')}\n"
            f"Uptime : {result[0].get('uptime', '-')}\n"
            f"Caller-Id : {result[0].get('caller-id', '-')}\n"
            f"Last-logout : {result[0].get('last-logged-out', '-')}\n"
            f"Service : {result[0].get('service', '-')}\n"
            f"Mark : {result[0].get('mark', '-')}\n"
        )
        #self.PPPoeDataLabel.configure(text=data)
        self.PPPoeDataLabel.configure(state='normal')
        self.PPPoeDataLabel.delete("1.0", 'end')
        self.PPPoeDataLabel.insert("1.0", data)
        self.PPPoeDataLabel.configure(state='disabled')
        if result[0].get('mark', '-') == 'Active' or result[0].get('mark', '-') == 'Both':
            self.PPPoeBTN.configure(state='normal')
        else:
            self.PPPoeBTN.configure(state='disabled')
        self.selectedPPPoe = result[0]

    def fncPPPoeMonit(self):
        if self.selectedPPPoe != '' and self.selectedserver != '':
            MonitDialog = PopUpDialog(self.root, self.selectedPPPoe.get('name', '-'), self.selectedserver, self.selectedPPPoe)
            self.root.wait_window(MonitDialog)

    def fnconsearch(self, event=None):
        if self.onsearch:
            return
        self.SearchEntry.configure(state='disabled')
        query = self.SearchVar.get().strip().lower()
        print(f"Search : {event}, {query}")

        if not query:
            self.filterRouterAndPPPoeList = {}
            self.SearchEntry.configure(state='normal')
            self.fncPopulateServerList()
            return
        self.onsearch = True
        self.filterRouterAndPPPoeList = {}
        words = query.split()
        for x in self.ServerListItemContainer.winfo_children():
            x.destroy()
        self.ServerListItemContainer.configure(height=1)
        self.ServerListCanvas.yview_moveto(0)
        for i in self.PPPoeListItemContainer.winfo_children():
            i.destroy()
        self.PPPoeListItemContainer.configure(height=1)
        self.PPPoeCanvas.yview_moveto(0)
        self.RefreshBtn.configure(state='disabled')

        # print(f'fnconsearch : {self.filterRouterAndPPPoeList} \n')
        threading.Thread(target=self.fnconsearchbg, args=(words, ), daemon=True).start()
        
    def fnconsearchbg(self, query):
        for x in dh.varRCInstance:
            ss = dh.varRCInstance[x]
            api = RC.varAllAPI[x]['routerapi']
            isitvalid = RC.fncstaticIsisValidAPI(api)
            for i in ss.PPPoeData:
                combined = f"{i.get('name', '-')} {i.get('address', '-')} {i.get('profile', '-')} {i.get('comment', '-')} {i.get('caller-id', '-')} {i.get('last-logged-out', '-')} {i.get('service', '-')} {i.get('mark', '-')}".lower()
                if all(word in combined for word in query):
                    if ss.varIdentity not in self.filterRouterAndPPPoeList:
                        self.filterRouterAndPPPoeList[ss.varIdentity] = []
                    self.filterRouterAndPPPoeList[ss.varIdentity].append(i)
        self.onsearch = False
        self.root.after(0, lambda: self.fncPopulateServerList())



    def fncScrolllist(self, parent):
        scrollcontainerframe = ttk.Frame(parent, style="Dark.TFrame")
        scrollcontainerframe.pack(expand=True, fill='both', padx=1, pady=1)
        self.DashboardCanvas = tk.Canvas(scrollcontainerframe, bg=self.colorpallete['bg'], borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scrollcontainerframe, style='Dark.Vertical.TScrollbar', orient='vertical', command=self.DashboardCanvas.yview)
        self.scrollframe = ttk.Frame(self.DashboardCanvas, style="Dark.TFrame")
        self.scrollframe.bind(
            "<Configure>",
            lambda e: self.DashboardCanvas.configure(
                scrollregion=self.DashboardCanvas.bbox("all")
            )
        )
        self.scroll_window_id = self.DashboardCanvas.create_window(
            (0, 0), window=self.scrollframe, anchor="nw"
        )
        self.DashboardCanvas.bind(
            "<Configure>",
            lambda e: self.DashboardCanvas.itemconfig(self.scroll_window_id, width=e.width)
        )
        self.DashboardCanvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill='y', side='right', padx=5)
        self.DashboardCanvas.pack(side="left", fill='both', expand=True)

    def fncPopUpItem(self, title):
        dialog = InputDialog(self.root, title)
        self.root.wait_window(dialog)
        if dialog.result:
            # ip_exists = any(dialog.result['ip'] == item['ip'] for item in dh.varRouterServerData.values())
            server_exists = dialog.result['servername'] in dh.varRouterServerData
            if not server_exists:
                print("User input:", dialog.result, '\n')
                self.fncAddItem(dialog.result)
                datas = {dialog.result['servername'] : {
                    'ip' : dialog.result['ip'],
                    'username' : dialog.result['username'],
                    'password' : dialog.result['password'],
                    'port' : dialog.result['port'],
                    } 
                }
                dh.fncAddRouterServerData(datas)

    def fncInitSyncRouterData(self):
        if dh.varRouterServerData != None:
            for i in dh.varRouterServerData:
                x = {'servername': i, 'ip': dh.varRouterServerData[i]['ip'], 'username': dh.varRouterServerData[i]['username'], 'password': dh.varRouterServerData[i]['password'], 'port': dh.varRouterServerData[i]['port']}
                self.fncAddItem(x)
                print(f"fncInitSynchRouterData : {i} \n")
    
    def fncAddItem(self, data):

        itemDataFrame = ttk.Frame(self.scrollframe, style="2Dark.TFrame", padding=1)
        itemDataFrame.pack(fill='x', padx=5, pady=5)
        itemDataFrameHeader = ttk.Frame(itemDataFrame, style="Dark.TFrame", padding=2)
        itemDataFrameHeader.pack(fill='x', padx=1, pady=1)
        editbtn = ttk.Button(itemDataFrameHeader, style="Dark.TButton", width=2, text='\U0001F4E5', command=lambda: self.fncEditData(data, item_labels))
        delbtn = ttk.Button(itemDataFrameHeader, style="Dark.TButton", width=2, text='X', command= lambda : self.fncDeleteData(data['servername'], itemDataFrame))
        editbtn.pack(side='right', padx=5)
        delbtn.pack(side='right', padx=5)
        itemGridManagerFrame = ttk.Frame(itemDataFrame, style="Dark.TFrame", padding=1)
        itemGridManagerFrame.pack(fill='both', padx=1, pady=1)
        item_labels = {
            'ip': ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=data['ip']),
            'username': ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=data['username']),
            'password': ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=data['password']),
            'port': ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=data['port']),
            'servername': ttk.Label(itemDataFrameHeader, style='Dark.TLabel', text=data['servername'])
        }
        IPaddresslabel1 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text="IP Addres").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        Usernamelabel1 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text="Username").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        Passwordlabel1 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text="Password").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        Portlabel1 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text="Port").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        IPaddresslabel2 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=":").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        Usernamelabel2 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=":").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        Passwordlabel2 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=":").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        Portlabel1 = ttk.Label(itemGridManagerFrame, style='Dark.TLabel', text=":").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        item_labels['ip'].grid(row=1, column=2, padx=10, pady=5, sticky="w")
        item_labels['username'].grid(row=2, column=2, padx=10, pady=5, sticky="w")
        item_labels['password'].grid(row=3, column=2, padx=10, pady=5, sticky="w")
        item_labels['port'].grid(row=4, column=2, padx=10, pady=5, sticky="w")
        item_labels['servername'].pack(fill='x', side='left', padx=5)

    def fncDeleteData(self, data, frame):
        del dh.varRouterServerData[data]
        frame.destroy()
        dh.fncExportRouterServerData()

    def fncEditData(self, data_dict, frame):
        dialog = InputDialog(self.root, 'Edit Server', data_dict)
        self.root.wait_window(dialog)
        if dialog.result:
            localdata = dh.varRouterServerData.copy()
            localdata.pop(data_dict['servername'], None)
            ip_exist = any(dialog.result['ip'] == item['ip'] for item in localdata.values())
            print(f'localdata : {localdata.values()} ip_exist: {ip_exist} \n')
            if dialog.result['servername'] in dh.varRouterServerData:
                if dialog.result['servername'] == data_dict['servername']:
                    if all([
                        dialog.result['ip'] == dh.varRouterServerData[dialog.result['servername']]['ip'],
                        dialog.result['username'] == dh.varRouterServerData[dialog.result['servername']]['username'],
                        dialog.result['password'] == dh.varRouterServerData[dialog.result['servername']]['password'],
                        dialog.result['port'] == dh.varRouterServerData[dialog.result['servername']]['port']
                    ]):
                        print(dh.varRouterServerData[dialog.result['servername']]['ip'], '\n')
                        return
                else:
                    return
            print("User input:", dialog.result, '\n')
            dh.fncEditValueServerData(data_dict['servername'], dialog.result['servername'], {
                'ip' : dialog.result['ip'],
                'username' : dialog.result['username'],
                'password' : dialog.result['password'],
                'port' : dialog.result['port'],
            } )
            for key in ['servername', 'ip', 'username', 'password', 'port']:
                data_dict[key] = dialog.result[key]
                if key in frame: 
                    frame[key].config(text=dialog.result[key])
            



class PopUpDialog(tk.Toplevel):
    def __init__(self, parent, title, serverapi=None, pppoedata=None):
        super().__init__(parent)
        self.withdraw()
        parent.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        dialog_w = 300
        dialog_h = 280
        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2
        self.geometry(f"{dialog_w}x{dialog_h}+{x}+{y}")
        self.resizable(False, False)

        self._offset_x = x
        self._offset_y = y
        self.fontx = font.Font(family='Courier New', size=12) 
        self.overrideredirect(True)
        self.colorpallete = {
            'bg' : '#10141f',
            'shadow' : '#090a14',
            'btn' : '#151d28',
            'txtcolor' : '#4f8fba',
            'hover' : '#411d31',
            'pressed' : '#241527',
            'hovertxt' : '#a53030'
        }

        self.configure(background=self.colorpallete['shadow'], padx=5, pady=5)
        self.configure(background=self.colorpallete['shadow'], padx=5, pady=5)
        # self.fncConfigStyle()
        self.headerframe = ttk.Frame(self, style="2Dark.TFrame", height=10)
        self.headerframe.pack(side='top', fill='x')
        titlelabel = ttk.Label(self.headerframe, style='3Dark.TLabel', text=title, anchor='n', justify='center')
        titlelabel.pack(side='top', pady=10, padx=10)
        self.grab_set()
        self.running = True
        self.MainFrame = ttk.Frame(self, style="Dark.TFrame")
        self.MainFrame.pack(side='top', fill='both', expand=True)
        maincontenttext = (
            f"Profile : {pppoedata.get('profile', '-')}\n"
            f"IP Address : {pppoedata.get('address', '-')} \n"
            f"Comment : {pppoedata.get('comment', '-')}\n"
        )
        self.maincontentlLabel = ttk.Label(self.MainFrame, style='2Dark.TLabel', wraplength=280, text=maincontenttext, justify='center')
        self.maincontentlLabel.pack(side='top', fill='both', expand=True)
        self.contentlLabel = ttk.Label(self.MainFrame, style='2Dark.TLabel', wraplength=280, text='Invalid', justify='center')
        self.contentlLabel.pack(side='top', fill='x')
        self.contentlLabel2 = ttk.Label(self.MainFrame, style='2Dark.TLabel', wraplength=280, text='', justify='center')
        self.contentlLabel2.pack(side='bottom', fill='both', expand=True)
        self.button_frame = ttk.Frame(self, style="Dark.TFrame")
        self.button_frame.pack(side='bottom', fill='x')
        ttk.Button(self.button_frame, style='Dark.TButton', text="Close", command=self.fncOnClose).pack(side="right")
        self.deiconify()
        if serverapi and pppoedata.get('mark', 'Local') != 'Local':
            curobj = RC.fncclassGetAPI()[serverapi]
            self.receivedapi = [curobj['routerapi'], curobj['routerapib']]
            self.validAPI = all([RC.fncstaticIsisValidAPI(self.receivedapi[0]), RC.fncstaticIsisValidAPI(self.receivedapi[0])])
            self.pppoeip = pppoedata.get('address', '-')
            self.pppoename = pppoedata.get('name', '-')
            threading.Thread(target=self.fncPPPoePing, daemon=True).start()
            threading.Thread(target=self.fncPPPoeBW, daemon=True).start()

            
    def fncPPPoePing(self):
        if self.pppoeip != '-' and self.validAPI:
            #print(f"fncPPPoePing : {self.receivedapi} | {self.pppoeip} \n")
            while self.running and self.winfo_exists():
                resulttext = PPull.PPPoePing(self.receivedapi[0], self.pppoeip)
                if self.winfo_exists():
                    self.after(0, lambda: self.contentlLabel.configure(text=resulttext))
                    #self.contentlLabel.configure(text=PPull.PPPoePing(self.receivedapi[0], self.pppoeip))
                time.sleep(1)
    
    def fncPPPoeBW(self):
        if self.pppoename != '-' and self.validAPI:
            interfacename = f'<pppoe-{self.pppoename}>'
            while self.running and self.winfo_exists():
                #print(interfacename)
                resulttext = PPull.PPPoeBW(self.receivedapi[1], interfacename)
                if self.winfo_exists():
                    self.after(0, lambda : self.contentlLabel2.configure(text=resulttext))
                    #self.contentlLabel2.configure(text=PPull.PPPoeBW(self.receivedapi[1], interfacename))
                time.sleep(1)

    def fncOnClose(self):
        self.running = False
        self.destroy()
                  

class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, initial_values=None):
        super().__init__(parent)
        self.withdraw()
        parent.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        dialog_w = 400
        dialog_h = 280
        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2
        self.geometry(f"{dialog_w}x{dialog_h}+{x}+{y}")
        self.resizable(False, False)

        self._offset_x = x
        self._offset_y = y
        self.fontx = font.Font(family='Courier New', size=12) 

        self.overrideredirect(True)
        self.colorpallete = {
            'bg' : '#10141f',
            'shadow' : '#090a14',
            'btn' : '#151d28',
            'txtcolor' : '#4f8fba',
            'hover' : '#411d31',
            'pressed' : '#241527',
            'hovertxt' : '#a53030'
        }
        self.configure(background=self.colorpallete['shadow'], padx=5, pady=5)
        # self.fncConfigStyle()
        self.headerframe = ttk.Frame(self, style="Dark.TFrame", height=10)
        self.headerframe.pack(side='top', fill='x')
        self.headerframe.bind('<Button-1>', self.fncStartmove)
        self.headerframe.bind('<B1-Motion>', self.fncMovewindow)
        titlelabel = ttk.Label(self.headerframe, style='Dark.TLabel', text=title)
        titlelabel.bind('<Button-1>', self.fncStartmove)
        titlelabel.bind('<B1-Motion>', self.fncMovewindow)
        titlelabel.pack(side=tk.LEFT, pady=10, padx=10)
        self.grab_set()
        self.result = None
        self.entries = {}
        fields = [
            ('Servername', 'servername'),
            ('IPaddress', 'ip'),
            ('Username', 'username'),
            ('Password', 'password'),
            ('Port', 'port'),
        ]
        self.mainframe = ttk.Frame(self, style="Dark.TFrame", height=10)
        self.mainframe.pack(side='top', fill='both', expand=True)
        self.deiconify()

        for i, (label_text, keys) in enumerate(fields):
            ttk.Label(self.mainframe, style='Dark.TLabel', text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self.mainframe, style='Dark.TEntry')
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[keys] = entry
        
            if initial_values and keys in initial_values:
                    entry.insert(0, initial_values[keys])
                
        self.mainframe.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.mainframe, style='Dark.TFrame')
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, style='Dark.TButton', text="OK", command=self.fncOnOk).pack(side="left", padx=10)
        ttk.Button(button_frame, style='Dark.TButton', text="Cancel", command=self.destroy).pack(side="left")

    def fncStartmove(self, event):
        self._offset_x = event.x_root - self.winfo_x()
        self._offset_y = event.y_root - self.winfo_y()

    def fncMovewindow(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.geometry(f"+{x}+{y}")

    def fncOnOk(self):
        self.result = {key: entry.get() for key, entry in self.entries.items()}
        self.destroy()

if __name__ == "__main__":
    dh.fncLoadRouterServerData()
    root = tk.Tk()
    CPanel = ControlPanel(root)
    CPanel.remove_bar()

    root.mainloop()