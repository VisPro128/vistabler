# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 10:44:30 2016
author: Patrik Toobe
"""

import time

"""###############~~~~Path Variables~~~~###############"""
# your timetable html file location and file name
input_file = "/sdcard/Vistabler/mytimetable.html"

# the path you want your file to export to
output_path = "/sdcard/Vistabler/"

# the filename and extension you want to export with
output_filename = "myTimetable.txt"
"""###############~~~~~~~~~~~~~~~~~~~~~~###############"""

year = time.strftime("/%Y")
current_date = time.strftime("%d/%m/%Y")
current_time = time.strftime("%H:%M")
courses = ["MATH1054", "SESA1015", "FEEG1001", "FEEG1002",
           "FEEG1003", "FEEG1004"]

# import offline timetable 
timetable = open(input_file, 'r')
global lines
lines = timetable.readlines()
lines = lines.__str__()

# define data arrays
sesh = []
date = []
stime = []
etime = []
loc = []

# remove all before first lecture
lines = lines.partition(courses[0])
sesh.append(lines[1])
lines = lines[1] + lines[2]


def sesh_date_time():
    """look for sesh date and times"""
    w = lines.index(year)
    date.append(lines[(w - 5):(w + 5)])
    stime.append(lines[(w + 6):(w + 11)])
    w = lines.index(year, (w + 11))
    etime.append(lines[(w + 6):(w + 11)])


def next_loc():
    """look for next sesh location"""
    global lines

    w = lines.index(year)
    w1 = lines.index("<", w+45)
    w2 = lines[(w + 45):(w1)]
    loc.append(w2)
    lines = lines.partition(w2)
    lines = lines[1] + lines[2]


def next_sesh():
    """look for next sesh and log it"""
    global lines

    search = []
    for i in range(len(courses)):
        search.append(lines.find(courses[i]))

    for i in range(len(search)):
        if search[i] < 0:
            search[i] = 100000

    if (sum(search)/len(search)) == 100000:
        return 1
    nextcourse = courses[search.index(min(search))]

    # partition after next course title
    lines = lines.partition(nextcourse)
    sesh.append(lines[1])
    lines = lines[1] + lines[2]

sesh_date_time()
next_loc()

nh = 0
while nh < 100:
    if next_sesh() == 1:
        break
    sesh_date_time()
    next_loc()
    nh = nh + 1


# file creation
output_file = open(output_path + output_filename, 'w')

output_file.write("Current Time: " + current_time +
                  "\nCurrent Date:  " + current_date + "\n")

# next session
w1 = 0
w3 = len(date)

# test for weekday
try:
    w2 = date.index(current_date)  # yes is weekday
    for i in range(w2, len(date)):
        if current_date == date[i]:
            w1 = w1 + 1
        else:
            pass

# handling for next-session text output
    for i in range(w1):
        next_session_text = "\nNext session is {} at {} in {}\n\n"
        weekend_text = "\nHave a good weekend!\n\n"

        if current_time < stime[i + w2]:
            output_file.write(next_session_text.format(
                        sesh[i + w2], stime[i + w2], loc[i + w2]))
            break
        else:
            if w2 + i == w3 - 1:
                output_file.write(weekend_text)
                break
            else:
                if i == w1 - 1:
                    i = i + 1
                    output_file.write(next_session_text.format(
                            sesh[i + w2], stime[i + w2], loc[i + w2]))
                    break
                pass

except ValueError:  # no, is weekend
    output_file.write("\nEnjoy your weekend. Have you downloaded the new timetable?\n\n")

# date header
for i in range(len(sesh)):
    try:
        if date[i] != date[i - 1]:
            output_file.write(str(str(date[i]) + '\n'))
    except IndexError:
        pass

# session + times
    output_file.write(str('\\s/ ' + str(sesh[i]) +
                      ' \\t/ ' + str(stime[i]) + ' - ' + str(etime[i]) +
                          ' \\l/ ' + str(loc[i]) + '\n'))

# new day line break
    try:
        if date[i] != date[i + 1]:
            output_file.write('\n')
    except IndexError:
        pass

output_file.close()

