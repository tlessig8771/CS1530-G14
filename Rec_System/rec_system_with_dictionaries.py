from collections import Counter
from datetime import datetime
import json
import os


def get_sport_recommendations(int):
    userSports = users[userid]['Sports']
    items = len(userSports)
    occurences = Counter(userSports)
    probability = {key:value for key, value in occurences.items()}
    
    for value in probability:
        probability[value] = '{0:.3g}'.format(probability[value]/items)

    favoredSport = max(probability, key=probability.get)
    return favoredSport,probability


def get_activity_recommendations(int):
    userActivities = users[userid]['Activities']
    items = len(userActivities)
    occurences = Counter(userActivities)
    probability = {key:value for key, value in occurences.items()}
    
    for value in probability:
        probability[value] = '{0:.3g}'.format(probability[value]/items)

    favoredActivity = max(probability, key=probability.get)
    return favoredActivity, probability



                                ###OPEN FILE###
##with open('UserStats.txt') as f: 
##    data = f.read() 
##  
##print("Data type before reconstruction : ", type(data))
##print(data)
##
##dictionary = dict(subString.split(":") for subString in data.split(";"))
##print(dictionary)
##
### reconstructing the data as a dictionary 
##js = json.loads(data) 
##  
##print("Data type after reconstruction : ", type(js)) 
##print(js)
##
##d = {}
##with open("UserStats.txt") as f:
##    for line in f:
##       (key, val) = line.split()
##       d[int(key)] = val
##
##print(d)


#sports = ["Hockey", "Football", "Basketball", "Soccer", "Rugby", "Lacrosse", "Baseball", "Cricket", "Tennis", "Volleyball", "Swimming",
         # "Gymnastics"]

#activities = ["Hiking", "Exercise", "Biking", "Concerts", "Eating", "Drinking"]



users = {1: {'Name':"Bob", "Pass":"pass123", 'Sports':["Hockey", "Football"], 'Activities':[]},
         2: {'Name':"Kayla", "Pass":"cyansus", 'Sports': [], 'Activities': []}}

print(users)


username = input("Enter name: ")
for i in users:
    if username == users[i]['Name']:
        password = input("Enter password: ")
        if password == users[i]['Pass']:
            userid = i
            print("Welcome ", username,"!")

            while True:
                activ = input("What is an activity you like doing: ")
                users[userid]['Activities'].append(activ)
                
                sport = input("Sports you've been watching: ")
                users[userid]['Sports'].append(sport)

                recommendedSport = get_sport_recommendations(userid)
                print("Your recommended sport: ",recommendedSport)
                recommendedActivity = get_activity_recommendations(userid)
                print("Your recommended activity: ",recommendedActivity)

                exits = input("Would you like to exit? (y/n)")
                if(exits == 'y'):
                    break
        else:
            print("Incorrect password. Restart.")
            break
        
        print(users)


                                ###WRITE TO FILE###
##file1 = open("UserProbs.txt", "a")  # append mode 
##file1.write("Today \n") 
##file1.close()

##file = open("UserStats.txt", "w")
##stats = open("UserProbs.txt", "a")
##file.write(str(users)+'\n')
##stats.write(str(datetime.now())+'\n')
##stats.write(users[userid]['Name'])
##stats.write("\nSports Probabilities\n")
##stats.writelines(str(recommendedSport[1]))
##stats.write("\nActivities Probabilities\n")
##stats.writelines(str(recommendedActivity[1])+"\n\n")
##file.close()
##stats.close()











