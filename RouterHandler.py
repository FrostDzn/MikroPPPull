import routeros_api as rapi
from routeros_api.api_structure import StringField
import collections
import threading
from concurrent.futures import ThreadPoolExecutor
from DataHandler import DataHandler as dh


class RouterConnecter:

    varAllAPI : dict = {}
    default_structure = collections.defaultdict(lambda: StringField(encoding='windows-1250'))

    def __init__(self, routerip : str, router_username : str, router_password : str, router_port : str, router_plaintext : bool = True):
        self.varIpAddress = routerip
        self.varRouterUsername = router_username
        self.varRouterPassword = router_password
        self.varIdentity = ''
        self.varRouterPort = int(router_port)
        self.varPlaintext = router_plaintext
        for name, val in dh.varRouterServerData.items():
            #print(f' RH Init : {name} ---- {val.get('ip')} -- {val.get('port')}')
            #print(f' RH Init Compared : {self.varIpAddress} ---- {self.varRouterPort}')
            if val.get('ip') == self.varIpAddress and int(val.get('port')) == self.varRouterPort:
                self.varIdentity = name
                print(f'Identity : {self.varIdentity}')
        print(f"[RouterConnector Initialize]  \nIP Address : {self.varIpAddress} \nUsername : {self.varRouterUsername}\n Password : {self.varRouterPassword} \n Router Port : {self.varRouterPort} \n")
        if self.varIdentity in RouterConnecter.varAllAPI :
            currentAPI = RouterConnecter.varAllAPI[self.varIdentity]["routerapi"]
            currentAPIb = RouterConnecter.varAllAPI[self.varIdentity]["routerapib"]
            if currentAPI != "" and currentAPIb != "":
                if not RouterConnecter.fncstaticIsisValidAPI(currentAPI) and not RouterConnecter.fncstaticIsisValidAPI(currentAPIb):
                    self.fncConnect()
            else:
                self.fncConnect()
        else :
            self.fncConnect()
        

    # def fncConnect(self):
    #     connection = rapi.RouterOsApiPool(self.varIpAddress, self.varRouterUsername, self.varRouterPassword, self.varRouterPort, self.varPlaintext)
    #     varRouternameAndAPI = {self.varIdentity : { "name" : "", "ip" : "", "routerapi" : "", "reason" : "", "reasonb" : ""}}
    #     try : 
    #         self.varConnectionAPI = connection.get_api()
    #         connectionb = rapi.RouterOsApiPool(self.varIpAddress, self.varRouterUsername, self.varRouterPassword, self.varRouterPort, self.varPlaintext)
    #         try :
    #             self.varConnectionAPIb = connectionb.get_api()
    #             varRouternameAndAPI = {self.varIdentity : { "name" : self.fncGetRouterIdentity(), "ip" : self.varIpAddress, "routerapi" : self.varConnectionAPI, "routerapib" : self.varConnectionAPIb, "reason" : "", "reasonb" : ""}}
    #             print(f"fncConnect : Success : {varRouternameAndAPI} \n")
    #             pppoeobjinstance = PPPoePull(self.varConnectionAPI, self.varConnectionAPIb, self.varIdentity)
    #             self.secretPPPoe = pppoeobjinstance.secretPPPoe
    #             self.activePPPoe = pppoeobjinstance.activePPPoe
    #             self.markedPPPoe = pppoeobjinstance.markedname
    #             self.PPPoeData = pppoeobjinstance.pppoedata
    #         except Exception as e:
    #             self.PPPoeData = dh.fncPPPoeDataImport(self.varIdentity)
    #             varRouternameAndAPI[self.varIdentity]["reasonb"] = str(e)
    #             print(f"fncConnect {self.varIdentity} reason b : error {e} \n")
    #     except Exception as e:
    #         self.PPPoeData = dh.fncPPPoeDataImport(self.varIdentity)
    #         varRouternameAndAPI = {self.varIdentity : { "name" : "", "ip" : self.varIpAddress, "routerapi" : "",  "routerapib" : "", "reason" : str(e)}}
    #         print(f"fncConnect {self.varIdentity} main: error {e} \n")
    #     self.fncclassAddAPI(varRouternameAndAPI)

    def fncConnect(self):
        varRouternameAndAPI = {self.varIdentity : { "name" : "", "ip" : self.varIpAddress, "routerapi" : "", "routerapib" : "","reason" : "", "reasonb" : ""}}
        try : 
            connection = rapi.RouterOsApiPool(self.varIpAddress, self.varRouterUsername, self.varRouterPassword, self.varRouterPort, self.varPlaintext)
            self.varConnectionAPI = connection.get_api()
            varRouternameAndAPI[self.varIdentity]["routerapi"] = self.varConnectionAPI
            print(f"fncConnect : Success : {varRouternameAndAPI} \n")
        except Exception as e:
            #self.PPPoeData = dh.fncPPPoeDataImport(self.varIdentity)
            varRouternameAndAPI[self.varIdentity]['reason'] = str(e)
            print(f"fncConnect {self.varIdentity} main: error {e} \n")
        try :
            connectionb = rapi.RouterOsApiPool(self.varIpAddress, self.varRouterUsername, self.varRouterPassword, self.varRouterPort, self.varPlaintext)
            self.varConnectionAPIb = connectionb.get_api()
            varRouternameAndAPI[self.varIdentity]["routerapib"] = self.varConnectionAPIb
            print(f"fncConnect : Success : {varRouternameAndAPI} \n")
        except Exception as e:
            varRouternameAndAPI[self.varIdentity]['reasonb'] = str(e)
            print(f"fncConnect {self.varIdentity} second: error {e} \n")
        if varRouternameAndAPI[self.varIdentity]["routerapi"] != "" and varRouternameAndAPI[self.varIdentity]["routerapib"] != "":
            if RouterConnecter.fncstaticIsisValidAPI(self.varConnectionAPI) and RouterConnecter.fncstaticIsisValidAPI(self.varConnectionAPIb):
                pppoeobjinstance = PPPoePull(self.varConnectionAPI, self.varConnectionAPIb, self.varIdentity)
                self.secretPPPoe = pppoeobjinstance.secretPPPoe
                self.activePPPoe = pppoeobjinstance.activePPPoe
                self.markedPPPoe = pppoeobjinstance.markedname
                self.PPPoeData = pppoeobjinstance.pppoedata
        else:
            print(f"fncConnect {self.varIdentity} : unable to connect, will load local data if exist \n")
            print(f"fncConnect : {varRouternameAndAPI} \n")
            self.PPPoeData = dh.fncPPPoeDataImport(self.varIdentity)

        self.fncclassAddAPI(varRouternameAndAPI)

    def fncPPPoeRefresh(self):
        if self.varIdentity in RouterConnecter.varAllAPI :
            currentAPI = RouterConnecter.varAllAPI[self.varIdentity]["routerapi"]
            if currentAPI != "" :
                if RouterConnecter.fncstaticIsisValidAPI(currentAPI):
                    pppoeobjinstance = PPPoePull(self.varConnectionAPI, self.varConnectionAPIb, self.varIdentity)
                    self.secretPPPoe = pppoeobjinstance.secretPPPoe
                    self.activePPPoe = pppoeobjinstance.activePPPoe
                    self.markedPPPoe = pppoeobjinstance.markedname
                    self.PPPoeData = pppoeobjinstance.pppoedata
                    # print(f'active : {self.activePPPoe}')
                    # print(f'active : {self.secretPPPoe}')

    def fncGetRouterIdentity(self):
        varRouterName = self.varConnectionAPI.get_resource("/system/identity", structure=self.default_structure).get()
        # print(f"fncGetRouterIdentity : {varRouterName}")
        return varRouterName[0]["name"]
    
    

    @classmethod
    def fncclassGetAPI(cls):
        return cls.varAllAPI

    @classmethod
    def fncclassAddAPI(cls, value : dict):
        cls.varAllAPI.update(value)

    @staticmethod
    def fncstaticIsisValidAPI(yourapi):
        try:
            iden = yourapi.get_resource('/system/identity')
            iden.get()
            return True
        except Exception as e:
            return False


class PPPoePull():
    default_structure = collections.defaultdict(lambda: StringField(encoding='windows-1250'))
    def __init__(self, yourapi, yourapib, yourid):
        self.varCurrentIden = yourid
        self.varCurrentapi = yourapi
        self.varCurrentapib = yourapib
        with ThreadPoolExecutor() as excutor :
            ftr = excutor.submit(self.fncPullSecretPPPoe, self.varCurrentapi)
            ftr2 = excutor.submit(self.fncPullActivePPPoe, self.varCurrentapib)
            self.secretPPPoe = ftr.result()
            self.activePPPoe = ftr2.result()
            self.markedname = {}
            if self.secretPPPoe and self.activePPPoe:
                self.markedname = self.fncComparePPPoe(self.secretPPPoe, self.activePPPoe)
                self.pppoedata = self.fncPPPoeData(self.secretPPPoe, self.activePPPoe, self.markedname, self.varCurrentIden)
            else:
                print(f"PPPoePull Init {self.varCurrentIden} : error, will pull Data From Local Data")
                self.pppoedata = dh.fncPPPoeDataImport(self.varCurrentIden)
    
    @staticmethod
    def fncPullSecretPPPoe(api):
        try :
            pppoesecret = api.get_resource("/ppp/secret", structure=PPPoePull.default_structure)
            ppp = pppoesecret.get()
            return ppp
        except Exception as e:
            print(f"{api} error {e}")
            return []

        

    @staticmethod
    def fncPullActivePPPoe(api):
        try:
            pppoeactive = api.get_resource("/ppp/active", structure=PPPoePull.default_structure)
            ppp = pppoeactive.get()
            return ppp
        except Exception as e:
            print(f"{api} error {e}")
            return []
    
    @staticmethod
    def fncComparePPPoe(vala, valb):
        name_a = {namesa['name'] for namesa in vala}
        name_b = {namesb['name'] for namesb in valb}
        markedname = {}

        unitedname = name_a | name_b
        for curname in unitedname :
            if curname in name_a and curname in name_b :
                markedname[curname] = "Both"
            elif curname in name_a and curname not in name_b:
                markedname[curname] = "Secret"
            elif curname in name_b and curname not in name_a:
                markedname[curname] = "Active"
        
        return markedname
    
    @staticmethod
    def PPPoePing(api, ip):
        #print(f'fncPPPoePing {api}: IP {ip} \n')
        try:
            result = api.get_resource('/').call('ping', {
                'address': ip,
                'count': '1'
            })
            if result:
                #print(f"Ping {ip}: {result[0].get('time', 'N/A')} ms")
                return (f"Ping {ip}: {result[0].get('time', 'N/A')}")
            else:
                #print(f"Ping {ip}: Timeout")
                return (f"Ping {ip}: Timeout")
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def PPPoeCheckInterface(api, interface):
        res = api.get_resource('/interface')
        interfaces = res.get()

        exist = any(interfacex.get('name') == interface for interfacex in interfaces)
        return exist

    @staticmethod
    def PPPoeBW(api, interface):
        try:
            res = api.get_resource('/interface')

            result = res.call('monitor-traffic', {
                'interface' : interface,
                'once' : ''
            })
            rx = int(result[0].get('rx-bits-per-second', '0')) / 1000
            tx = int(result[0].get('tx-bits-per-second', '0')) / 1000
            #print(f"{interface} RX: {str(rx)} kbps | TX: {str(tx)} kbps")
            return (f'{interface} \n RX: {str(rx)} kbps \n TX: {str(tx)} kbps')
        except Exception as e:
            return (f'{interface} Not Found error : {str(e)}')
        #print(result)

    @staticmethod
    def PPPoeMonit(api, interface):
        pass

    @staticmethod
    def fncPPPoeData(secret, active, marked, ipx):
        data = []
        data2 = []
        ReconstructedPPPoe = {}
        ReconstructedPPPoe2 = {}
        for i in marked:
            pppoe = [name for name in secret if name.get('name') == i]
            activex = [name for name in active if name.get('name') == i]
            match marked[i]:
                case 'Both':
                    ReconstructedPPPoe = {'name' : pppoe[0].get('name', '-'), 
                                          'uptime' : activex[0].get('uptime', '-'), 
                                          'address' : activex[0].get('address', '-'), 
                                          'mark' : 'Both', 
                                          'caller-id' : activex[0].get('caller-id', '-'),
                                          'last-logged-out' : pppoe[0].get('last-logged-out', '-'),
                                          'comment' : activex[0].get('comment', '-'),
                                          'profile' : pppoe[0].get('profile', '-'),
                                          'service' : pppoe[0].get('service', '-')}
                    ReconstructedPPPoe2 = {'name' : pppoe[0].get('name', '-'), 
                                          'uptime' : activex[0].get('uptime', '-'), 
                                          'address' : activex[0].get('address', '-'), 
                                          'mark' : 'Local', 
                                          'caller-id' : activex[0].get('caller-id', '-'),
                                          'last-logged-out' : pppoe[0].get('last-logged-out', '-'),
                                          'comment' : activex[0].get('comment', '-'),
                                          'profile' : pppoe[0].get('profile', '-'),
                                          'service' : pppoe[0].get('service', '-')}                    
                case 'Secret':
                    ReconstructedPPPoe = {'name' : pppoe[0].get('name', '-'), 
                                          'uptime' : '-', 
                                          'address' : pppoe[0].get('remote-address', '-'), 
                                          'mark' : 'Secret', 
                                          'caller-id' : pppoe[0].get('last-caller-id', '-'),
                                          'last-logged-out' : pppoe[0].get('last-logged-out', '-'),
                                          'comment' : pppoe[0].get('comment', '-'),
                                          'profile' : pppoe[0].get('profile', '-'),
                                          'service' : pppoe[0].get('service', '-')}
                    ReconstructedPPPoe2 = {'name' : pppoe[0].get('name', '-'), 
                                          'uptime' : '-', 
                                          'address' : pppoe[0].get('remote-address', '-'), 
                                          'mark' : 'Local', 
                                          'caller-id' : pppoe[0].get('last-caller-id', '-'),
                                          'last-logged-out' : pppoe[0].get('last-logged-out', '-'),
                                          'comment' : pppoe[0].get('comment', '-'),
                                          'profile' : pppoe[0].get('profile', '-'),
                                          'service' : pppoe[0].get('service', '-')}
                case 'Active':
                    ReconstructedPPPoe = {'name' : activex[0].get('name', '-'), 
                                          'uptime' : activex[0].get('uptime', '-'), 
                                          'address' : activex[0].get('address', '-'), 
                                          'mark' : 'Active', 
                                          'caller-id' : activex[0].get('caller-id', '-'),
                                          'last-logged-out' : '-',
                                          'comment' : activex[0].get('comment', '-'),
                                          'profile' : '-',
                                          'service' : activex[0].get('service', '-')}
                    ReconstructedPPPoe2 = {'name' : activex[0].get('name', '-'), 
                                          'uptime' : activex[0].get('uptime', '-'), 
                                          'address' : activex[0].get('address', '-'), 
                                          'mark' : 'Local', 
                                          'caller-id' : activex[0].get('caller-id', '-'),
                                          'last-logged-out' : '-',
                                          'comment' : activex[0].get('comment', '-'),
                                          'profile' : '-',
                                          'service' : activex[0].get('service', '-')}
            data.append(ReconstructedPPPoe)
            data2.append(ReconstructedPPPoe2)
        dh.fncPPPoeDataExport(ipx, data2)
        return data
    


