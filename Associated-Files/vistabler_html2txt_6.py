# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 10:44:30 2016

@author: Patrik Toobe

Function Wishlist:
-
-
-
"""
import time
"""###############~~~~Path Variables~~~~###############"""
# your timetable html file location and file name
input_file = "/sdcard/Vistabler/mytimetable.html"
# input_file = "/Users/Pat/GitHub/vistabler/My.Timetable.html"

# the path you want your file to export to
output_path = "/sdcard/Vistabler/"
# output_path = "/Users/Pat/Desktop/"

# the filename and extension you want to export with
output_filename = "myTimetable.txt"
"""###############~~~~~~~~~~~~~~~~~~~~~~###############"""

year = time.strftime("/%Y")
current_date = time.strftime("%d/%m/%Y")
current_yday = (list(time.strptime(current_date, "%d/%m/%Y")))[7]
current_time = time.strftime("%H:%M")

# import offline timetable
timetable = open(input_file, 'r')
global lines
lines = timetable.readlines()
lines = lines.__str__()

# define data arrays
sesh = []
stype = []
date = []
stime = []
etime = []
loc = []

# define text filter
comber = "class=\"hide-on-paper\"><a"


def comber_function():
    """Session data comber"""
    try:
        x = 1
        while x >= 0:
            x = lines.index(comber, x)  # find class class

            yc1 = lines.index("\">", x + 25)  # find course title start
            yc2 = lines.index(" ", yc1)  # find course title end (short)
            zc = lines[yc1+2:yc2]
            sesh.append(zc)  # add course to sesh list

            x = lines.index(comber[0:-2], yc2)  # find sesh type
            yt1 = lines.index("\">", x)  # find type start
            yt2 = lines.index(" ", yt1)  # find type end
            zt = lines[yt1+2:yt2]
            if zt.__contains__("Lab"):  # make lab destinction
                sesh[-1] = sesh[-1] + (" (L)")
            stype.append(zt)  # add sesh type to list

            x = lines.index("<td>", yt2)  # find sesh date
            yd1 = x + 4  # find sesh date start
            yd2 = lines.index(" ", yd1)  # find sesh date end
            zd = lines[yd1:yd2]
            date.append(zd)  # add date to list

            ys1 = yd2 + 1
            ys2 = lines.index("</td>", ys1)
            zs = lines[ys1:ys2]
            stime.append(zs)  # add stime to list

            x = lines.index("<td>", ys2)  # find etime
            ye1 = lines.index(" ", x)  # find etime start
            ye2 = lines.index("</td>", ye1)  # find etime end
            ze = lines[ye1 + 1:ye2]
            etime.append(ze)  # add etime to list

            x = lines.index("<td>", ye2)  # find loc
            yL1 = (lines.index(" ", x)) + 2  # find loc start
            yL2 = lines.index("\\", yL1)  # find loc end
            zL = lines[yL1:yL2]
            if len(zL) == 0:
                zL = "(No location given)"
            if zL.startswith("BOL"):
                zL = zL[13:]  # + " (BLDW)"
            loc.append(zL)  # add loc to list

    except ValueError:
        x = -1


comber_function()


def date2yday(date):
    """converts calendar date into workable year day"""
    t = list(time.strptime(date, "%d/%m/%Y"))
    return t[7]


def ptc(hourmin):
    """converts readable time into coded minutes of the day"""
    if len(hourmin) > 5:
        hourmin = hourmin[:-3]
    t = list(time.strptime(hourmin, "%H:%M"))
    t = (t[3] * 100) + t[4]
    return t


"""########################### FILE CREATION ###########################"""
output_file = open(output_path + output_filename, 'w+')

output_file.write("Current Time: " + current_time +
                  "\nCurrent Date: " + current_date + "\n")

# LOGIC

next_session_text = "\nNext session is {} at {} in {}\n\n"
tmrrw_session_text = "\nNext session is {} tomorrow at {} in {}\n\n"
current_session_text = "\nCurrent session is {} at {} in {}\n\n"
weekend_text = "\nHave a good weekend!\n\n"
enjoy_weekend_text = "\nEnjoy your weekend!\n\n"
no_lectures = "\nNo lectures today, sweet!\n\n"
day_off = "\nEnjoy your day off!\n\n"

skip = 0

while skip == 0:
    # check for weekend
    if current_yday < date2yday(date[0]) or current_yday > date2yday(date[-1]):
        output_file.write(enjoy_weekend_text)
        skip = 1
        break

    # check starting date index for day
    try:
        w1 = date.index(current_date)  # w1 is starting date index
        L = 1
        w2 = 0                      # w2 is how many sessions that day
        while L == 1:
            try:
                if current_yday == date2yday(date[w1 + w2]):
                    w2 += 1
                else:
                    L = 0
            except IndexError:
                L = 0
    except ValueError:  # week day of no lectures goes here
        output_file.write(no_lectures)
        skip = 1
        break

    w3 = w2 - 1 + w1  # w3 is the index of the last session that day
    w4a = stime[w1:w1 + w2]  # stimes of all sessions that day
    w4b = stime[w1:w1 + w2]
    w4b.insert(0, '0')
    w4b.append('0')
    w4c = sesh[w1:w1 + w2]  # sessions that day

    for w0 in range(len(w4a)):
        if ptc(w4a[w0]) > ptc(current_time):  # stime[w0] > ctime
            if w4b[w0].isdigit():               # -> First session?
                output_file.write(next_session_text.format(
                        sesh[w0 + w1], stime[w0 + w1], loc[w0 + w1]))
                break
            else:                               # -> before next session
                output_file.write(next_session_text.format(
                        sesh[w0 + w1], stime[w0 + w1], loc[w0 + w1]))
                break
        elif ptc(w4a[w0][:3] + "05") >= ptc(current_time) >= ptc(w4a[w0]):
            output_file.write(current_session_text.format(
                        sesh[w0 + w1], stime[w0 + w1], loc[w0 + w1]))
            break
        elif ptc(current_time) > ptc(w4a[-1][:3] + "05"):  # after last?
            w5 = w1 + w2
            try:
                if (date2yday(current_date) + 1) == date2yday(date[w1+w2]):
                    output_file.write(tmrrw_session_text.format(  # next day
                                        sesh[w5], stime[w5], loc[w5]))
                    break
                else:
                    output_file.write(day_off)
                    break
            except IndexError:
                output_file.write(weekend_text)
                break
    break


# FORMATTING

# date header
for i in range(len(sesh)):
    try:
        if date2yday(date[i]) != date2yday(date[i - 1]):
            output_file.write(str(str(date[i]) + '\n'))
    except IndexError:
        pass

# session + times
    output_file.write(str('\\s/ ' + str(sesh[i]) +
                      ' \\t/ ' + str(stime[i]) + ' - ' + str(etime[i]) +
                          ' \\l/ ' + str(loc[i]) + '\n'))

# new day line break
    try:
        if date2yday(date[i]) != date2yday(date[i + 1]):
            output_file.write('\n')
    except IndexError:
        pass

output_file.close()

# verification
"""
fresh_press = open("/Users/JT/Desktop/myTimetable.txt", 'r')
nline = fresh_press.readlines()
print(nline[3])
print(nline[5])
fresh_press.close()"""
