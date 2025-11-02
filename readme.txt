This is a project for the Toyota GR hackathon project where we utilize the dta provided to make a software that utilizes the power of AI to provided extensive breakdown of the performace of a driver and areas where improvements can e made. This would be integrated in a well designed software application.


Instructions:
- Create a root folder (name this folde "hackathon)
- Create a folder named "Datasets"
    - Download data files from this url: https://trddev.com/hackathon-2025/
    - Unzip all data files and place each folder into the Datasets folder.
- Create a folder named "TrackMaps"
    - Download track maps from this url: https://trddev.com/hackathon-2025/
    - Unzip all maps and place each folder into the TrackMaps folder.
- Clone repositotry into root folder
- Work in respective folder. 
- When you want to push code, please make sure to be in the OTG---OnTheGo folder.


######## NOTICE #########

If you need to use a large model, please upload it to Google Drive and include the link—along with clear folder structure instructions—in your submission. Make sure not to include large files in the Git repository to prevent pushing excessively heavy data to the repo. Please include your name and a date in the instruction you include.


````````````````````````````
Team Members - Role
---------------------------------
- Hamza Tai - Frontend
- Oluwasoji Lasaki - Frontend - Logic 
- Nakshatra Bobbili - Model Refinement
- Tina Oyatobo - Backend 
````````````````````````````

Project Commenecement date - October 22nd, 2025


Soji - October 24th, 2025
- Install latest version of python
    - check python versioin with python3 --version
    If python version is earlier than 3.9, upgrade python versioin with:
        - python3 -m pip install --upgrade pi
- Install virtualenv 
    - python3 -m pip install virtualenv
    - Create new virtualenv
        - python3 -m venv venv
    - Activate virtualenv
        - source venv/bin/activate   # macOS/Linux
        - venv\Scripts\activate      # Windows
- Install packages
    - pip install dash plotly pandas numpy dash-bootstrap-components
    - pip install dash_daq  # for gauge/speedometer components
    - pip install scipy     # for signal filtering
