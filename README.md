# Easy Find

## How to start with the project
    1. unzip the file "EasyFind.zip" on your desktop
    2. open terminal and navigate to the folder by:
        a. cd Desktop
        b. cd EasyFind
    3. use command "./EasySave.py --help" and "./EasyFind.py --help" to understand on how to use

## How to run the project
You can run the project by running the following bash commands:

```bash
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
./EasySave.py [ACTION/IMAGE_PATH]
./EasyFind.py [OBJECT_NAME]
```
Please note, this project requires python 3.9 to run

## Getting the path for the folder
### On Mac:
    1. Press the option button and right click on the folder
    2. There will be an option "Copy [FOLDER_NAME] as pathname", press that and your path is copied
    3. Simply paste the path name when you use ./EasySave.py [IMAGE_PATH]


## Future Developments
 Supporting multiple search query inputs to get the file paths of all the images where image1 and image2 exists.
