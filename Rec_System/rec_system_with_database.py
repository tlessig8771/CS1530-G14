from collections import Counter
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
import os
import sqlite3

def get_sport_recs(username):
        userobj = cursor.execute("SELECT * FROM USER WHERE name='{}'".format(username))
        for row in userobj:
                if(row[0] != None):
                        hockey = row[3]
                        football = row[4]
                        soccer = row[5]
   

        sportTotal = hockey+football+soccer
        sportProb = {"hockey":hockey/sportTotal, "football":football/sportTotal, "soccer":soccer/sportTotal}
        favoredSport = max(sportProb, key=sportProb.get)
        return(favoredSport, sportProb[favoredSport], sportProb)

def get_food_recs(username):
        userobj = cursor.execute("SELECT * FROM USER WHERE name='{}'".format(username))
        for row in userobj:
                if(row[0] != None):
                        restaurant = row[9]
                        dessert = row[10]
                        chinese = row[11]
   

        foodTotal = restaurant+dessert+chinese
        foodProb = {"restaurant":restaurant/foodTotal, "dessert":dessert/foodTotal, "chinese":chinese/foodTotal}
        favoredFood = max(foodProb, key=foodProb.get)
        return(favoredFood, foodProb[favoredFood], foodProb)

def get_act_recs(username):
        userobj = cursor.execute("SELECT * FROM USER WHERE name='{}'".format(username))
        for row in userobj:
                if(row[0] != None):
                        swimming = row[6]
                        concert = row[7]
                        hiking = row[8]
   

        actTotal = swimming+concert+hiking
        actProb = {"swimming":swimming/actTotal, "concert":concert/actTotal, "hiking":hiking/actTotal}
        favoredAct = max(actProb, key=actProb.get)
        return(favoredAct, actProb[favoredAct], actProb)
        



con = sqlite3.connect('my-test.db')
con.execute("DROP TABLE USER")


with con:
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            hockey INTEGER,
            football INTEGER,
            soccer INTEGER,
            swimming INTEGER,
            concert INTEGER,
            hiking INTEGER,
            restaurant INTEGER,
            dessert INTEGER,
            chinese INTEGER
        );
    """)


sql = 'INSERT INTO USER (id, name, password, hockey,football,soccer,swimming,concert,hiking,restaurant,dessert,chinese) values(?,?,?,?,?,?,?,?,?,?,?,?)'
data = [
    (1, 'Alice', 'pass', 0,5,3,2,3,4,1,1,2),
    (2, 'Bob', 'bob', 1,2,3,4,4,5,7,6,6),
    (3, 'Chris', 'stewart', 7,1,1,4,2,3,4,5,6)
]

with con:
    con.executemany(sql, data)

with con:
    data = con.execute("SELECT * FROM USER")
    for row in data:
        print(row)

cursor = con.cursor()

print("Strictly Restricted to food: chinese, restaurant, dessert; sports: hockey, soccer, football; events: concerts, swimming, hiking")

while True:
        username = input("Enter name: ")

        userobj = cursor.execute("SELECT * FROM USER WHERE name='{}'".format(username))
        for row in userobj:
                if(row[0] != None):
                        ID = row[0]
                        name = row[1]
                        pas = row[2]
                        print(ID, name, pas)

                        password = input("Enter password: ")
                        if password == pas:
                                userid = ID
                                print("Welcome ", name,"!")
                        else:
                                print("Incorrect Password, Try again")
                                break

                        while True:
                                updatekeys = input("What is something you like doing: ")
                                if (updatekeys == "food"):
                                        con.execute("UPDATE USER SET chinese = chinese+1, restaurant = restaurant+1, dessert = dessert+1")
                                elif(updatekeys == "sports"):
                                        con.execute("UPDATE USER SET hockey = hockey+1, soccer = soccer+1, football = football+1")
                                elif(updatekeys == "events"):
                                        con.execute("UPDATE USER SET concerts = concerts+1, swimming = swimming+1, hiking = hiking+1")
                                        
                                else:
                                        con.execute("UPDATE USER SET {} = {}+1 WHERE name = '{}'".format(updatekeys,updatekeys,username))

                                with con:
                                    data = con.execute("SELECT * FROM USER")
                                    for row in data:
                                        print(row)

                

                                exits = input("Would you like to switch users? (y/n)")
                                if(exits == 'y'):
                                    break
                                
                else:
                        print("No user exists")
        print(get_sport_recs(username))
        print(get_act_recs(username))
        print(get_food_recs(username))

        exits = input("Would you like to exit? (y/n)")
        if(exits == 'y' or exits == 'Y' or exits == "yes" or exits == "Yes" or exits == "YES"):
                break


con.close()

print("\nTHANK YOU FOR WORKING")

 
