#Final Project: Leaderboard handling

#importing csv
import csv

#function to input a score
def input_score(username, position, score):
    #finds the username line
    with open("high_scores.csv", "r") as file:
        #initializes csv reader
        csvreader = csv.reader(file)

        #skips header
        next(file)

        #finds the line with the username in it
        for line in csvreader:
            if username == line[0]:
                previousline = line

        #lines to rewrite
        lines = []

    with open("high_scores.csv", "r") as file:
        #initializes csv reader (again)
        csvreader2 = csv.reader(file)
        
        #saves the previous lines
        for line in csvreader2:
            if line == previousline:
                continue
            else:
                lines.append(",".join(line))

    #writes the new line
    with open("high_scores.csv", "a+") as file:
        itemsinnewline = []
        num = 0
        for item in previousline:
            if num == position:
                itemsinnewline.append(str(score))
            else:
                itemsinnewline.append(item)
            num += 1

        lines.append(",".join(itemsinnewline))

    #clears file
    with open("high_scores.csv", "w") as file:
        file.write("")

    #writes the new file
    with open("high_scores.csv", "a+") as file:
        for line in lines:
            file.write(line)
            file.write("\n")

#function to get a score for a user
def get_score(username, position):
    with open("high_scores.csv", "r") as file:
        #initializes csv reader
        csvreader = csv.reader(file)

        #iterates over the file to find the username line and get the target score at the postion
        for line in csvreader:
            if line[0] == username:
                targetscore = line[position]

        #returns target score
        return targetscore

#function to get the leaderboard for a game
def get_leaderboard(position):
    with open("high_scores.csv", "r") as file:
        #initializes csv reader
        csvreader = csv.reader(file)

        #skips header
        next(csvreader)

        #list of all scores with username association
        scores = []

        #iterates over file to get the scores for the leaderboard
        for line in csvreader:
            scores.append((line[0], line[position]))
            print(f"{line[0]}: {line[position]}")
            print(f"{line[0]}: {line[position]}".split())

        #if the game is the reaction speed game, the lowest score is the best (the lowest time that they reacted)
        if position == 5: 
            reverseornot = False
        else:
            reverseornot = True

        scores.sort(key= lambda x: float(x[1]), reverse=reverseornot)

        return scores
