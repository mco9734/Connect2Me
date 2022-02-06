# MeetandHack2022
Repository for M&amp;T Bank RIT Meet and Hack 2022 

# Development
To run the application, you must have the latest version of Python 3 and virtualenv installed. Once you have those installed, create a new virtualenv and install the Python dependencies:
## Windows CMD
```
    virtualenv .meetandhack2022env
    .\.meetandhack2022env\Scripts\activate
    pip install -r requirements.txt
    set FLASK_APP=src/project
    flask run
```
 ## Bash 
 ```
    virtualenv .meetandhack2022env
    source .meetandhack2022env/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=src/project
    flask run
 ```

 You'll need to make a .env file in the project directory formatted as follows:
 ```
 EMAIL={email to send verification codes with}
 PASSWORD={password for email}
 ```
