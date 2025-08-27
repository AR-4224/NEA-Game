import mysql.connector
import random


def generate_ID():
    generate_Number = random.randint(0, 9999)
    ID = str(generate_Number)
    if len(ID) < 4:
        for count in range(4-len(ID)):
            ID = '0' + ID
    print(ID)

    return ID


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Project@1025',
    port='3306',
    database='amitdb'
)

cursor = mydb.cursor()

cursor.execute(f"INSERT INTO leaderboard(ScoreID, UserID, Username, HighestScore)"
               f"VALUES {''}, {''}, {''}, {''}")

