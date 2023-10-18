# CS-4800 Project S.H.E.R.L.O.C.K.
**S**erver **H**ealth and **E**mpirical **R**eal-time **L**atency for **O**nline **C**onnection **K**nowledge)

This program is designed for California State University Stanislaus' CS-4800 2023 Fall class with Dr. Hatem. It is meant to be able to ping servers to check to see if they are up (responsive) or if they are down (unresponsive). The program will ping based on a user given or predetermined poll rate. The status of the server is then saved to a file alongside a timestamp which will be used later to display a histogram of each indvidual server's status.  This program is hosted on the local machine and will require an internet conneciton to be useful, however, it is also capable of pinging device on the Local Area Network (LAN) and Wide Area Network (WAN).

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

#### Explanation of Folders
- client: Contains a python file for which the controllers will be working out of and the file will be used to communicate with the server.
- controllers: These python files will be the controllers for our project.
- exampleCode: Just some exploration on how things work and give a shot to some things.
- server: Python files responsible for our server.
- static: Holds a folder of images and a folder of css files.
- templates: Hold html files that import from the static pictures and css folders.
- oldFiles: Temporary Storage of old files. (Do we need them?)
