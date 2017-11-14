# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 10:44:30 2016

@author: Patrik Toobe

Function Wishlist:
-
-
-
"""
# from ics import Calendar, Event

"""###############~~~~Path Variables~~~~###############"""
# your timetable html file location and file name
# input_file = "/sdcard/Vistabler/mytimetable.html"
input_file = "/Users/Pat/GitHub/vistabler/My.Timetable.html"

# the path you want your file to export to
# output_path = "/sdcard/Vistabler/"
output_path = "/Users/Pat/GitHub/vistabler/"

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


def add_cal_event(stamp, date, stime, etime, sesh, description, location):
    """add event in iCal format"""

    vnt = []
    vnt.append('BEGIN:VEVENT\n')
    vnt.append('DTSTAMP:' + stamp + '\n')
    vnt.append('DTSTART:' + date + 'T' + stime[:6] + 'Z' + '\n')
    vnt.append('DTEND:' + date + 'T' + etime[:6] + 'Z' + '\n')
    vnt.append('SUMMARY:' + sesh + '\n')
    vnt.append('DESCRIPTION:' + description + '\n')
    vnt.append('LOCATION:' + location + '\n')
    vnt.append('UID:' + sesh + stime + date + '\n')
    vnt.append('END:VEVENT' + '\n')

    return vnt


callines = []
DTSTAMP = date[0] + 'T' + stime[0][:6] + 'Z'

callines.append('BEGIN:VCALENDAR' + '\n')
callines.append('PRODID:PT' + '\n')
callines.append('VERSION:2.0' + '\n')

for x in range(len(sesh)):
    w1 = add_cal_event(DTSTAMP, date[x], stime[x], etime[x], sesh[x],
                       stype[x], loc[x])
    for i in range(len(w1)):
        callines.append(w1[i])

callines.append('END:VCALENDAR' + '\n')

output_file.writelines(callines)
output_file.close()

# LOGIC
"""
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

"""
# output_file.writelines(c)

# output_file.close()
