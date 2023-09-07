# CS-4800_Project_Sherlock
This program is designed for California State University Stanislaus' CS-4800 2023 Fall class. It is meant to be able to ping servers to check to see if they are up (responsive) or if they are down (unresponsive). The program will ping based on a user given or predetermined poll rate. The status of the server is then saved to a file alongside a timestamp which will be used later to display a histogram of each indvidual server's status.  This program is hosted on the local machine and will require an internet conneciton to be useful, however, it is also capable of pinging device on the Local Area Network (LAN) and Wide Area Network (WAN).

## Team Members
- Christian Alameda
- Anthony Castillo
- Sierra Pangilinan
- Vel Perez-Barba

## Capabilities
- Runs locally
- Accept user given IP addresses, domain names, and/or websites
- Stores given IP addresses in a database
- Polls those addresses every (user defiend elapsed period) and stores latency, downtime and uptime info
- Display an uptime/downtime histogram
- A webui is used to manage the program
- Can trace connections to see where the connection ends if it is unable to reach its destination.

### Disclaimer
- All aspects are subject to change as the project progresses.
