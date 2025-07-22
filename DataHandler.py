import json
import os
import datetime

class DataHandler():    

    varRouterServerData = {}
    varPPPoeSecretData = {}
    varPPPoeActiveData = {}

    varBase_dir = './Data'
    varCurDay = datetime.date.today()
    varPPPoeDirToday = f'{varBase_dir}/{varCurDay.day}-{varCurDay.month}-{varCurDay.year}'
    varRouterServerDataFullPath = os.path.join(varBase_dir, 'RouterData.json')
    varRCInstance = {}


    def __init__(self):
        DataHandler.fncLoadRouterServerData()

    @staticmethod
    def fncCheckAllDataFolder(path):
        folders = []
        for folder in os.listdir(path):
            folder_fullpath = os.path.join(path, folder)
            if os.path.isdir(folder_fullpath):
                try:
                    date = datetime.datetime.strptime(folder, "%d-%m-%Y")
                    folders.append((date, folder_fullpath))
                except Exception as e:
                    print(f"fncCheckAllDataFolder error : {str(e)} \n")
                    continue
        print(f"fncCheckAllDataFolder folders variable contains: {folders} \n")
        sorted_folders = sorted(folders, key=lambda folder: folder[0], reverse=True)
        sorted_folder_paths = [folder[1] for folder in sorted_folders]
        print(f"fncSortFolderBasedOnDatetime : {sorted_folder_paths} \n")
        return sorted_folder_paths
    


    @classmethod
    def fncAddRouterServerData(cls, value):
        cls.varRouterServerData.update(value)
        cls.fncExportRouterServerData()
        print('RouterServerData : ', cls.varRouterServerData)

    @classmethod
    def fncEditValueServerData(cls, old_key, new_key, new_value):
        if old_key in cls.varRouterServerData:
            cls.varRouterServerData[new_key] = new_value
            if old_key != new_key:
                del cls.varRouterServerData[old_key]
        cls.fncExportRouterServerData()
    
    @classmethod
    def fncGetRouterServerData(cls):
        return cls.varRouterServerData
    
    @classmethod
    def fncLoadRouterServerData(cls):
        os.makedirs(cls.varBase_dir, exist_ok=True)
        os.makedirs(cls.varPPPoeDirToday, exist_ok=True)
        if os.path.exists(cls.varRouterServerDataFullPath):
            with open(cls.varRouterServerDataFullPath, 'r') as f:
                cls.varRouterServerData = json.load(f)
    
    @classmethod
    def fncExportRouterServerData(cls):
        with open(cls.varRouterServerDataFullPath, 'w') as f:
            json.dump(cls.varRouterServerData, f, indent=4)
    
    @staticmethod
    def fncPPPoeDataExport(name, data):
        PPPoeFullPath = os.path.join(DataHandler.varPPPoeDirToday, f'{name}.json')
        with open(PPPoeFullPath, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def fncPPPoeDataImport(name):
        datax = []
        PPPoeFullPath = os.path.join(DataHandler.varPPPoeDirToday, f'{name}.json')
        if os.path.exists(PPPoeFullPath):
            with open(PPPoeFullPath, 'r') as f:
                datax = json.load(f)
                print(f"fncPPPoeDataImport : found {name} at {PPPoeFullPath} \n")
        else:
            folderExists = DataHandler.fncCheckAllDataFolder(DataHandler.varBase_dir)
            for i in folderExists:
                PPPoeFullPath = os.path.join(i, f'{name}.json')
                if os.path.exists(PPPoeFullPath):
                    with open(PPPoeFullPath, 'r') as f:
                        datax = json.load(f)
                        print(f"fncPPPoeDataImport : found {name} at {PPPoeFullPath} \n")
                        break
            
        return datax
    
