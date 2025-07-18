# MikroPPPull
This script is used to pull PPPoE Secrets from MikroTik routers. 
I made this script for my own convenience. If you think this script also meets your needs, feel free to use or modify it as you wish.

Here is some brief explanation about this script: 

    On startup, it loads router data from the Data folder by looking for a JSON file named RouterData. You can add routers manually to this file or use the Server Panel to add router data after launching the script or executable.

    After loading and syncing router data, the script logs all PPPoE entries, reconstructs the data, and stores a dumped copy in the Data folder. This dumped data is used when the router is unreachable and is marked as Local.

        There are 4 PPPoE status types:

            Active: The PPPoE is currently listed in the "Active" tab only — most likely connected via RADIUS.

            Secret: The PPPoE is listed only in the "Secret" tab — most likely disconnected.

            Both: The PPPoE is listed in both "Active" and "Secret" tabs.

            Local: The router is currently unreachable, so previously dumped data is used instead.

    To search for PPPoE entries, type your query in the search bar and press Enter to apply the search.


    Note: Please keep in mind the script does not update PPPoE data in real time. It pulls the data only once during syncing. which why the PPPoE data is static.

        However, you can refresh the selected server in the PPPoE tab while the script is running by clicking the refresh button next to the search bar.
    


    These are the required depedencies:

        pywin32 – for moving the GUI window

        pyinstaller – for building the executable

        routeros_api – for connecting to MikroTik and pulling PPPoE data

        tkinter - for GUI
        
        (Other packages may be present from testing and im forgot to remove it.)

    The dist and build folders are generated by PyInstaller during the compilation process.