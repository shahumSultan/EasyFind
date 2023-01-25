#!/usr/bin/env python

import re
import sqlite3
import sys

def getDatafromDB(userWord):
    wordResult = re.split(r"[+-]\s*", userWord)
    finalList = set()
    resultList = []
    allResult = set()
    
    try:
        connection = sqlite3.connect("Final_Images.db")
        cursor = connection.cursor()
        print("Connected to Database")
        
        for word in wordResult:
            cursor.execute("SELECT distinct Images.path FROM Images INNER JOIN Objects ON Images.id=Objects.path_id WHERE objects in(?);", (word,))
            rows = cursor.fetchall()
            resultList.append(set(rows))
            allResult.update(rows)
            
        for item in allResult:
            existInAll = True
            for x in resultList:
                if (item not in x):
                    existInAll = False
                    break
                if(existInAll):
                    finalList.add(item)
        
        if not finalList:
            print("\n----------RESULTS----------")
            print("Nothing in Database")
        else:
            print("\n----------RESULTS----------")
            print("Image(s) Containg:", userWord, "\n")
            for row in finalList:
                print(row[0])
                
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        if(connection):
            connection.close()
            print("Database Connection Closed")


def printHelp():
        print(f"""
Usage: {sys.argv[0]} ["OBJECT_NAME"]

Parameters:
    "OBJECT_NAME"   The name of the object you want to search for (IN DOUBLE SPEECH MARKS).
    
""")
        

def main():
    if  sys.argv[1] == "-h" or sys.argv[1] == '--help':
        printHelp()
        return
    
    if len(sys.argv) == 2:
        object_name = sys.argv[1].lower()
        #print(object_name)
        getDatafromDB(object_name)

if __name__ == "__main__":
    main()