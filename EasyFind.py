#!/usr/bin/env python

import re
import sqlite3
import sys


def splitIcon(word):
    return word.replace('-', '')


# Function for fetching data from database for the user
def getDataFromDB(userWord):
    allWords = re.split(r"[+-]\s*", userWord)
    excludedMatches = re.findall(r"[-][a-z]*", userWord)
    excludedWords = list(map(splitIcon, excludedMatches))
    excludedSet = set(excludedWords)
    
    includedWords = []
    for word in allWords:
        if (word not in excludedSet):
            includedWords.append(word)

    finalList = set()
    resultsLists = []
    allresults = set()
    excludedPaths = set()

    try:
        connection = sqlite3.connect('Final_Images.db')
        cursor = connection.cursor()
        print("Connected to Database")

        for word in includedWords:
            cursor.execute(
                "SELECT distinct Images.path FROM Images INNER JOIN Objects ON Images.id=Objects.path_id WHERE objects in(?);", (word,))
            rows = cursor.fetchall()
            resultsLists.append(set(rows))
            allresults.update(rows)

        for word in excludedWords:
            cursor.execute(
                "SELECT distinct Images.path FROM Images INNER JOIN Objects ON Images.id=Objects.path_id WHERE objects in(?);", (word,))
            rows = cursor.fetchall()
            excludedPaths.update(rows)

        for item in allresults:
            existsInAll = True
            if (item in excludedPaths):
                existsInAll = False
                break
            for x in resultsLists:
                if (item not in x):
                    existsInAll = False
                    break
            if (existsInAll):
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
        if connection:
            connection.close()
            print("\nDatabase Connection Closed")


def printHelp():
    print(f"""
Usage: {sys.argv[0]} [OBJECT_NAME]
          
Parameters:
    OBJECT_NAME   The name of the object you want to search for.
    
""")


def main():
    if sys.argv[1] == "-h" or sys.argv[1] == '--help':
        printHelp()
        return

    if len(sys.argv) == 2:
        object_name = sys.argv[1].lower()
        getDataFromDB(object_name)


if __name__ == "__main__":
    main()
