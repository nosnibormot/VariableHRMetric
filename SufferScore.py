import re
import os

##Need to make this vary by user input
z1 = 115
z2 = 134
z3 = 154
z4 = 173
z5 = 220

sufferArr = []
avgHR = []

path = "/Users/Tom/Desktop/StravaFiles/"

#Ensure results file is closed, otherwise screws up folder with what i think is temp file
n = open(path+"Results.csv","w")
n.close()

for filename in os.listdir(path):
    f = open(path+filename, "r")

#Reset all temp vars
    startRec = False
    totalHRM = 0
    instHRM = 0
    totSec = 0
    tz1 = tz2 = tz3 = tz4 = tz5 = 0

#Iterate through each line of file
    for line in f:
        #Checks that we have passed metadata and that file is .TCX
        if "<Track>" in line:
            startRec = True
        if "<TotalTimeSeconds>" in line:
            m = re.search("<TotalTimeSeconds>(.+?)</TotalTimeSeconds>", line)
            totSec = float(m.group(1))
        if "<Value>" in line and startRec:
            m = re.search("<Value>(.+?)</Value>", line)
            if m:
                bpm = int(m.group(1))
                totalHRM += bpm
                instHRM += 1

                if bpm < z1:
                    tz1 += 1
                elif bpm < z2:
                    tz2 += 1
                elif bpm < z3:
                    tz3 += 1
                elif bpm < z4:
                    tz4 += 1
                elif bpm < z5:
                    tz5 += 1

    #Won't calc. 0 suffer score if file is not .tcx i.e. if it is results file
    if startRec != False:
        sufferscore =       (12 / 3600) * tz1 * (totSec / instHRM) \
                            + (24 / 3600) * tz2 * (totSec / instHRM) \
                            + (45 / 3600) * tz3 * (totSec / instHRM) \
                            + (100 / 3600) * tz4 * (totSec / instHRM) \
                            + (120 / 3600) * tz5 * (totSec / instHRM)
        #Modified from http://djconnel.blogspot.co.uk/2011/08/strava-suffer-score-decoded.html
        #Need to make zone weightings variable
        sufferArr.append(sufferscore)
        avgHR.append(totalHRM/instHRM)
        f.close()

#Create .CSV file
n = open(path+"Results.csv","w")
n.write("Ride,Suffer Score, Average BPM\n")
for i in range(len(sufferArr)):
    n.write(str(i+1)+","+str(sufferArr[i])+","+str(avgHR[i])+'\n')
n.close()
print("Success!")