# World-Cup-Passing-Networks
A python script for parsing StatsBomb .json data (See this [Github page](https://github.com/statsbomb/open-data)) The *data* folder in the statsbomb open-data repository isthe folder that this script uses as its default folder. The files that the application reads are in the *events* subfolder.

Currently, the application only parses the "Pass" and "Ball Receipt*" tags, though possibly more functionality will be added in the future.
Dependencies: numpy, webweb (Both can be downloaded with pip)

Run from main.py which runs the passingGUI.py Tkinter dialog

error handling/comments not yet implemented

VisualizePassingData and Visualize PassingDataCollection are stepping stones to the GUI version and are nice little tests to run one or several match files.
