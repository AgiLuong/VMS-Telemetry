# VMS Telemetry System (VTS)
## Run
* install everything in `requirements.txt`
* `python .\dashboardGUI.py` on the base laptop - contains all the graphs
* `python .\base-record.py` actual CAN-Xbee communication. Run this on the base laptop as a background process and decode CAN messages
* `python3 on-board.py` onboard utility that sends select CAN messages to the base station
