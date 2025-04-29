#Final Project: Leaderboard handling

#importing csv
import csv

#function to input a score
def input_score(username, score, position):
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

        #initializes csv reader (again)
        csvreader2 = csv.reader(file)
        
        #saves the previous lines
        for line in csvreader2:
            print(line)
            if line == previousline:
                print("yes")
                continue
            else:
                print("gothere")
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

    print(lines)

    #writes the new file
    with open("high_scores.csv", "a+") as file:
        for line in lines:
            file.write(line)
            file.write("\n")

    


#calling function ------REMOVE AT THE END--------
input_score("tim", 700, 1)