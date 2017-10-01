# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 10:44:30 2016

@author: Patrik Toobe

Function Wishlist:
-
-
-
"""
from ics import Calendar, Event

"""###############~~~~Path Variables~~~~###############"""
# your timetable html file location and file name
# input_file = "/sdcard/Vistabler/mytimetable.html"
input_file = "/Users/Pat/Desktop/vistabler/My.Timetable.html"

# the path you want your file to export to
# output_path = "/sdcard/Vistabler/"
output_path = "/Users/Pat/Desktop/"

# the filename and extension you want to export with
output_filename = "myTimetable.ics"
"""###############~~~~~~~~~~~~~~~~~~~~~~###############"""

# import offline week timetable
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

# define text filter for HTML parsing
comber = "class=\"hide-on-paper\"><a"


# MAGIC, DON'T TOUCH
def comber_function():
    """Session data comber"""
    try:
        x = 1
        while x >= 0:
            x = lines.index(comber, x)  # find class class

            """
            # y = lines.index("title=\"", x)  # find course title start
            y = lines.index("\">", x)  # find course title start
            # y2 = lines.index("\">", y)  # find course title end (long)
            y2 = lines.index(" ", y)  # find course title end (short)
            z = lines[y + 7:y2]
            sesh.append(z)  # add course to sesh list
            """

            y = lines.index("false\">", x)  # find course title start
            y2 = lines.index(" ", y)  # find course title end (short)
            z = lines[y+7:y2]
            sesh.append(z)  # add course to sesh list

            # x = lines.index(comber[0:-2], y2)  # find sesh type
            x = lines.index("</td><td>", y2)
            y = lines.index("</td><td>", x + 2)  # find type start
            y2 = lines.index("<", y + 7)  # find type end
            z = lines[y + 9:y2]
            if z.__contains__("Lab"):  # make lab destinction
                sesh[-1] = sesh[-1] + (" (L)")
            stype.append(z)  # add sesh type to list

            x = lines.index("<td>", y2)  # find sesh date
            y = x  # find date start
            y2 = lines.index(" ", y)  # find date end
            z = lines[y + 4:y2]
            date.append(z)  # add date to list

            y = y2  # find stime start
            y2 = lines.index("</td>", y)  # find stime end
            z = lines[y + 1:y2]
            stime.append(z)  # add stime to list

            x = lines.index("<td>", y2)  # find etime
            y = lines.index(" ", x)  # find etime start
            y2 = lines.index("</td>", y)  # find etime end
            z = lines[y + 1:y2]
            etime.append(z)  # add etime to list

            x = lines.index("<td>", y2)  # find loc
            y = x + 4  # find loc start
            y2 = lines.index("</td>", y)  # find loc end
            z = lines[y:y2]
            if len(z) == 0:
                z = "(No location given)"
            if z.startswith("BOL"):
                z = z[13:]  # + " (BLDW)"
            loc.append(z)  # add loc to list

    except ValueError:
        x = -1


comber_function()

# style dates in ical format
for i in range(len(date)):
    date[i] = date[i].split("/")
    date[i].reverse()
    w = ''.join(date[i])
    date[i] = w

# style times in ical format
for i in range(len(stime)):
    stime[i] = stime[i].replace(":", "") + "00"


for i in range(len(etime)):
    etime[i] = etime[i].replace(":", "") + "00"


"""########################### FILE CREATION ###########################"""
output_file = open(output_path + output_filename, 'w+')

# LOGIC

c = Calendar()
e = Event()

# ics library stuff, generates the ics format
for i in range(len(sesh)):
    e = Event()
    e.name = str(sesh[i])
    e.description = stype[i]
    e.begin = date[i] + "T" + stime[i] + "+0100"  # "20170906T140000"
    e.end = date[i] + "T" + etime[i] + "+0100"  # "20170906T15000"
    e.location = loc[i]
    c.events.append(e)

output_file.writelines(c)

output_file.close()
