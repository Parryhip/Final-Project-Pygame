#Final Project: Leaderboard handling

#importing csv
import csv

#function to input a score
def input_score(username, score, position):
    #finds the username line
    with open("high_scores.csv", "r") as file:
        csvreader = csv.reader(file)
        next(file)
        for line in csvreader:
            if username == line[0]:
                previousline = line
                previouslineasalist = previousline.split(",")
                break

        #lines to rewrite
        lines = []
        
        #saves the previous lines
        for line in csvreader:
            if line == previousline:
                continue
            else:
                lines.append(line)

    #writes the new line
    with open("high_scores.csv", "a+") as file:
        itemsinnewline = []
        num = 0
        for item in previouslineasalist:
            if num == position:
                itemsinnewline.append(str(score))
            else:
                itemsinnewline.append(item)
            num += 1
            
