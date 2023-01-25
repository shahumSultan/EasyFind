#!/usr/bin/env python

from re import S
import sqlite3
import sys
import os
import ObjectDetection

def printHelp():
    print(f"""
Usage: {sys.argv[0]} [ACTION]
          
Parameters:
    [CREATE DB ACTION] -> Creates Database and Tables, invoked by using -c or --create.
    [RESET DB ACTION] -> Resets the table and then creates fresh tables for use, invoked by using -r or --reset
    [DELETE DB ACTION] -> Delete the database, invoked by using -d ["KEYWORD"] or --delete ["KEYWORD"]
    [IMAGE FOLDER] -> The folder path needs to given, containing the images to be scanned and saved to the database. A single file path can also be used.
          """)
    

def getImagePaths(path):
    files = []
    with os.popen(f'find {path} -name *.jpeg -o -name *.JPG') as pipe:
        for line in pipe:
            files.append(line.strip())
    return files


def createDB():
    fileName = "Final_Images.db"
    
    try:
        connection = sqlite3.connect(fileName)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images(
            id INTEGER PRIMARY KEY,
            path TEXT unique
            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Objects(
            path_id INTEGER,
            objects TEXT
            )''')
        print("New Database Created and Connected")
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        if connection:
            connection.close()
            

def resetDB():
    try:
        connection = sqlite3.connect('Final_Images.db')
        cursor = connection.cursor()
        #Deleting tables first if exists
        cursor.execute("DROP TABLE Images")
        cursor.execute("DROP TABLE Objects")
        #Creating the tables again
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images(
            id INTEGER PRIMARY KEY,
            path TEXT unique
            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Objects(
            path_id INTEGER,
            objects TEXT
            )''')
        print("\n")
        print("Database Reset")
        print("\n")
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        if connection:
            connection.close()
            

def deleteDB():
    try:
        connection = sqlite3.connect('Final_Images.db')
        cursor = connection.cursor()
        cursor.execute("""drop table Images""")
        cursor.execute("""drop table Objects""")
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
            print("Database Deleted")
            
            
def getDataToSave(files):
    all_objects = []
    print("\n")
    print("Connected to Database")
    for file_path in files:
        try:
            connection = sqlite3.connect('Final_Images.db')
            cursor = connection.cursor()
            sql_insert = """insert into Images (path) values (?);"""
            all_objects = ObjectDetection.getObjects(file_path)
            data_one = [file_path]
            cursor.execute(sql_insert, data_one)
            connection.commit()
            last_id = cursor.lastrowid
            
            sql_insert_object = """insert into Objects (path_id, objects) values (?,?);"""
            for x in range(len(all_objects)):
                data_two = last_id, all_objects[x]
                cursor.execute(sql_insert_object, data_two)
                connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print("Error: Duplicate Image(s) being Inserted")
            print("\n")
            exit()
        finally:
            if connection:
                connection.close()
    print("Data Inserted into Database")
    print("Database Connection Closed")
    print("\n")
    

def main():
    if sys.argv[1] == '-h' or sys.argv[1] == "--help":
        printHelp()
        return
    
    if sys.argv[1] == "-c" or sys.argv[1] == "--create":
        createDB()
        return
    
    if sys.argv[1] == "-r" or sys.argv[1] == "--reset":
        resetDB()
        return
    
    if sys.argv[1] == "-d" or sys.argv[1] == "--delete":
        deleteDB()
        return
    
    image_dir = sys.argv[1]
    
    image_dir = os.path.abspath(image_dir)
    image_paths = getImagePaths(image_dir)
    getDataToSave(image_paths)
    

if __name__ == "__main__":
    main()