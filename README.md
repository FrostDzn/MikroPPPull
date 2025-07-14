# MikroPPPull
Just some scripts to pull PPPoe Secret from Mikrotik Router

- On init it will load Router data from 'Data' folder, and it will search json file called RouterData, you can add it manually or add the router data from the Server Panel when you start the scripts / exe
- after you load the Router data and sync it, it will log all the pppoe and reconstruct the data then dump it on the data folder for it to be used later when you cant connect to your router it will use the dumped data and mark it as local 
    - There is 4 PPPoe mark :
        - Active : Selected PPPoe currently only available in PPPoe Active tabs, most likely connected by radius
        - Secret : Selected PPPoe currently only available in PPPoe Secret tabs, most likely it is not active
        - Both : Selected PPPoe is on PPPoe Secret tabs and PPPoe Active tabs
        - Local : Currently you cant connect to the Mikrotik, or you cant access the pppoe and it load your already dumped data from your last connected session
- to search PPPoe on the search column, you must press enter to submit the word you want to search

- Please do keep in mind that it doesnt do live PPPoe data update, it will only pull PPPoe once when you sync it, so the pppoe data is static.
    Howerever you can refresh Selected Server on the PPPoe menu when you run the script by clicking the refresh button at the right side of the search column.

- the MikroPPPull folder is py venv with the depedency required on it such as
    - pywin32 for moving the gui windows
    - pyinstaller to compile
    - routeros_api to connect and pull the PPPoe from api
    - and possibly other else i forgot to remove when testing stuff
- dist and build folder is output from pyinstaller