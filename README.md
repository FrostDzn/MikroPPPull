# MikroPPPull
Just some scripts to pull PPPoe Secret from Mikrotik Router

- On init it will load Router data from 'Data' folder, and it will search json file called RouterData, you can add it manually or add the router data from the Server Panel when you start the scripts / exe
- to search PPPoe on the search column, you must press enter to submit the word you want to search


- the MikroPPPull folder is py venv with the depedency required on it such as
    - pywin32 for moving the gui windows
    - pyinstaller to compile
    - routeros_api to connect and pull the PPPoe from api
    - and possibly other else i forgot to remove when testing stuff
- dist and build folder is output from pyinstaller

