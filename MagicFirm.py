#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#python 3.8.x max for free PDF library
# https://www.thepythoncode.com/article/sign-pdf-files-in-python
# https://github.com/PDFTron/pdftron-sign-app
# 2022/09/16

print ("---------------------------------------------------------------------------------------")
print (" /$$      /$$                     /$$           /$$$$$$$$ /$$                          ")
print ("| $$$    /$$$                    |__/          | $$_____/|__/                          ")
print ("| $$$$  /$$$$  /$$$$$$   /$$$$$$  /$$  /$$$$$$$| $$       /$$  /$$$$$$  /$$$$$$/$$$$   ")
print ("| $$ $$/$$ $$ |____  $$ /$$__  $$| $$ /$$_____/| $$$$$   | $$ /$$__  $$| $$_  $$_  $$  ")
print ("| $$  $$$| $$  /$$$$$$$| $$  \ $$| $$| $$      | $$__/   | $$| $$  \__/| $$ \ $$ \ $$  ")
print ("| $$\  $ | $$ /$$__  $$| $$  | $$| $$| $$      | $$      | $$| $$      | $$ | $$ | $$  ")
print ("| $$ \/  | $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$| $$      | $$| $$      | $$ | $$ | $$  ")
print ("|__/     |__/ \_______/ \____  $$|__/ \_______/|__/      |__/|__/      |__/ |__/ |__/  ")
print ("                        /$$  \ $$                                                      ")
print ("  @tiizss              |  $$$$$$/                                                      ")
print ("  @tisasia              \______/                                    2022 by TiiZss     ")
print ("---------------------------------------------------------------------------------------")

import sys
import os
from datetime import datetime, time

def is_valid_path(path):
    """Validates the path inputted and checks whether it is a file path or a folder path"""
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")

vnow = datetime.now()

time_tuple_vnow = (vnow.year,  # Year
                    vnow.month,  # Month
                    vnow.day,  # Day
                    vnow.hour,  # Hour
                    vnow.minute,  # Minute
                    vnow.second,  # Second
                    0,  # Millisecond
                    )
#print ("Fecha y hora actual:", vnow)
vnargs = len(sys.argv)
#print ("Número de parámetros:", len(sys.argv))
#print ("Lista de argumentos:", sys.argv)

import argparse

parser = argparse.ArgumentParser(description='Sign the document with the date and time of your choice. ',
                                 epilog="And that's how you'd foo a sign in a file")
#parser.add_argument("-V", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-F", "--file", help="File to sign (At this time Only PDF)")
parser.add_argument("-D", "--date", help="Sign date YYYY/MM/DD")
parser.add_argument("-T", "--time", help="Sign time HH:MM:SS")
parser.add_argument('-l', '--load', dest='load', action="store_true",help="Load the required configurations and create the certificate")
parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path, help="Enter the path of the file or the folder to process (At this time Not working)")
parser.add_argument('-s', '--signatureID', dest='signatureID', type=str, help="Enter the ID of the signature (At this time Not working)")
parser.add_argument('-p', '--pages', dest='pages', type=tuple, help="Enter the pages to consider e.g.: [1,3] (At this time Not working)")
parser.add_argument('-x', '--x_coordinate', dest='x_coordinate', type=int, help="Enter the x coordinate.")
parser.add_argument('-y', '--y_coordinate', dest='y_coordinate',  type=int, help="Enter the y coordinate.")
path = parser.parse_known_args()[0].input_path
if path and os.path.isfile(path):
    parser.add_argument('-o', '--output_file', dest='output_file', type=str, help="Enter a valid output file (At this time Not working)")
if path and os.path.isdir(path):
    parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
        str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively (At this time Not working)")
args = vars(parser.parse_args())
parser.format_help
args = parser.parse_args()
 
# Aquí procesamos lo que se tiene que hacer con cada argumento
if vnargs < 2:
    parser.print_help()
else:
    #if args.verbose:
    #    print ("depuración activada!!!")
    
    if args.file:
        print ("The filename to process is: ", args.file)
        if os.path.splitext(os.path.basename(args.file))[1].lower() != '.pdf':
            print ("PDF File needed!. Try Again.")
            sys.exit()
    else:
        print ("Without a file, I don't know what you want me to sign, honey.")
        sys.exit()

    if args.date:
        print ("The date of the sign and the file will be: ", args.date)
        vdate = args.date.split("/")
        time_tuple = (int(vdate[0]),  # Year
                        int(vdate[1]),  # Month
                        int(vdate[2]),  # Day
                        vnow.hour,  # Hour
                        vnow.minute,  # Minute
                        vnow.second,  # Second
                        0,  # Millisecond
                        )

    if args.time:
        print ("The time of the sign and the file will be: ", args.time)
        vtime = args.time.split(":")
        time_tuple = (vnow.year,  # Year
                    vnow.month,  # Month
                    vnow.day,  # Day
                    int(vtime[0]),  # Hour
                    int(vtime[1]),  # Minute
                    int(vtime[2]),  # Second
                    0,  # Millisecond
                    )

    if args.date and args.time:
        time_tuple = (int(vdate[0]),  # Year
                        int(vdate[1]),  # Month
                        int(vdate[2]),  # Day
                        int(vtime[0]),  # Hour
                        int(vtime[1]),  # Minute
                        int(vtime[2]),  # Second
                        0,  # Millisecond
                        )
    
    if not args.x_coordinate:
        args.x_coordinate = 0
    
    if not args.y_coordinate:
        args.y_coordinate = 0
    
    if not args.signatureID:
        args.signatureID = "FirmaTiiZss"

    def _printfile(file: str):
        # Image file
        sign_filename = os.path.dirname(os.path.abspath(__file__)) + file
        #os.path.abspath(__file__)) + "\static\signature.jpg"
        print (sign_filename)
        f = open(sign_filename, 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()

    def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset
    
    def utc2local(utc):
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
        return utc + offset

    def _win_set_time(time_tuple):
        import win32api
        dayOfWeek = datetime(*time_tuple).isocalendar()[2]
        t = time_tuple[:2] + (dayOfWeek,) + time_tuple[2:]
        win32api.SetSystemTime(*t)
    
    def _win_get_localtime():
        import win32api
        time_tuple = win32api.GetLocalTime()
        return time_tuple

    def _win_get_time():
        import win32api
        time_tuple = win32api.GetSystemTime()
        return time_tuple

    def _linux_set_time(time_tuple):
        import subprocess
        import shlex
        time_string = datetime(*time_tuple).isoformat()
        subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
        subprocess.call(shlex.split("sudo hwclock -w"))


    if sys.platform == 'linux2' or sys.platform == 'linux':
        if args.load:
            cadena = 'python FirmaPDF_Gen.py -l'
        else: 
            _linux_set_time(time_tuple)
            cadena = 'python FirmaPDF_Gen.py -i "%s" -s "%s" -x %s -y %s'%(args.file, args.signatureID, args.x_coordinate, args.y_coordinate)
            os.system (cadena)
            os.system("timedatectl set-timezone \"Europe/Madrid\" >/dev/null 2>&1");

    elif sys.platform == 'win32':
        _win_set_time(time_tuple)
        ##print("FIRMAMOS EL DOCUMENTO:", args.file)
        #cadena = 'python FirmaPDF_Gen.py -i "%s" -s "%s" -x %s -y %s'%(args.file, args.signatureID, args.x_coordinate, args.y_coordinate)
        if args.load:
            cadena = 'python FirmaPDF_Gen.py -l'
        else:    
            #cadena = 'python FirmaPDF2.py -i "%s" -s "%s" -x %s -y %s'%(args.file, args.signatureID, args.x_coordinate, args.y_coordinate)
            #cadena = 'python FirmaPDF3.py -i "%s" -s "%s" -x %s -y %s'%(args.file, args.signatureID, args.x_coordinate, args.y_coordinate)
            cadena = 'python FirmaPDF_Gen.py -i "%s" -s "%s" -x %s -y %s'%(args.file, args.signatureID, args.x_coordinate, args.y_coordinate)
            os.system (cadena)
            os.system ("w32tm /resync >NUL")