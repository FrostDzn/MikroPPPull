import json
import datetime
import os

class DataHandler():

    varRouterServerData = {}
    varPPPoeSecretData = {}
    varPPPoeActiveData = {}

    varBase_dir = './Data'
    varRouterServerDataFullPath = os.path.join(varBase_dir, 'RouterData.json')
    varRCInstance = {}


    def __init__(self):
        os.makedirs(self.varBase_dir, exist_ok=True)
        if os.path.exists(self.varRouterServerDataFullPath):
            DataHandler.fncLoadRouterServerData()

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
        if os.path.exists(cls.varRouterServerDataFullPath):
            with open(cls.varRouterServerDataFullPath, 'r') as f:
                cls.varRouterServerData = json.load(f)
    
    @classmethod
    def fncExportRouterServerData(cls):
        with open(cls.varRouterServerDataFullPath, 'w') as f:
            json.dump(cls.varRouterServerData, f, indent=4)
    
    @staticmethod
    def fncPPPoeDataExport(name, data):
        PPPoeFullPath = os.path.join('./Data', f'{name}.json')
        with open(PPPoeFullPath, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def fncPPPoeDataImport(name):
        datax = []
        PPPoeFullPath = os.path.join('./Data', f'{name}.json')
        if os.path.exists(PPPoeFullPath):
            with open(PPPoeFullPath, 'r') as f:
                datax = json.load(f)
        return datax
