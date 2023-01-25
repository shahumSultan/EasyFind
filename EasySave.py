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
            [CREATE DB ACTION] -> 
            [RESET DB ACTION] ->
            [DELETE DB ACTION] ->
            [IMAGE FOLDER] ->
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