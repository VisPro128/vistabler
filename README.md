# Vistabler
This repo contains associated files for the Vistabler project, which attempts to pull timetable information from a University of Southampton timetable and display it on an Android device in some kind of useful way without having to use the mySouthampton app.

vistabler_html2txt_2.py
^this code interprets the manually downloaded timetable html file for the current week and exports a txt with formatted timetable information.

My.Timetable.html
^is the file from which the timetable information wants to be read. Needs to be manually updated every week.

# Using this for yourself
Make a fork for yourself.
The Tasker task will make a folder called Vistabler in your SD card/main directory.

You'll need:

-Tasker
-Read_Timetable_ino.tsk.xml Tasker file
-SL4A (found in the associated files folder)
-PythonForAndroid ("")


Install SL4A, PythonForAndroid, Tasker and then the tast in that order.

There are some things to change too.

*Tasker edits*
-Action 9, HTTP Get: The path needs to be changed from master to whatever the name of your fork is, so you get your timetable instead of mine.
-Action 11, HTTP Get: Same deal as above.

*Code edits*
-Path Variables: Output path/input file may be an issue on some devices as it specifies 'sdcard' in the path. If this doesn't work, use a folder or address that does.
-Courses: You need to put your courses in manually sadly.
