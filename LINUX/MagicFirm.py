#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#python 3.8.x max for free PDF library
# https://www.thepythoncode.com/article/sign-pdf-files-in-python
# 2022/09/16


#######################################################################################################
###                                                                                                   #
###    Este no es el archivo original creado por @tiizss, sino una modificacion hecha por @focab0r    #
###                                                                                                   #
###    Es objetivo de este Script es para fines educativos y didacticos. Tanto el autor del Script,   #
###    como el de la modificacion, declinan toda responsabilidad por cualquier uso indebido o         #
###    fraudulento que pueda deribar de este Software.                                                #
###                                                                                                   #
###                                                          Version de la modificacion: 1.1          #
###                                                                                                   #
#######################################################################################################



# 2022/09/16
# Import Libraries
import OpenSSL
import time
import argparse
from PDFNetPython3.PDFNetPython import *
from typing import Tuple
from getpass import getpass
import sys
import os
from datetime import datetime

def createKeyPair(type, bits):
    """
    Create a public/private key pair
    Arguments: Type - Key Type, must be one of TYPE_RSA and TYPE_DSA
               bits - Number of bits to use in the key (1024 or 2048 or 4096)
    Returns: The public/private key pair in a PKey object
    """
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey


def create_self_signed_cert(pKey, named: str):
    """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
    # Create a self signed certificate
    cert = OpenSSL.crypto.X509()
    # Common Name (e.g. server FQDN or Your Name)
    cert.get_subject().CN = named
    cert.set_serial_number(int(time.time() * 10))
    # Not Before
    cert.gmtime_adj_notBefore(0)  # Not before
    # Not After (Expire after 10 years)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    # Identify issue
    cert.set_issuer((cert.get_subject()))
    cert.set_pubkey(pKey)
    cert.sign(pKey, 'md5')  # or cert.sign(pKey, 'sha256')
    return cert


def load(name: str):
    """Generate the certificate"""
    summary = {}
    summary['OpenSSL Version'] = OpenSSL.__version__
    # Generating a Private Key...
    key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
    # PEM encoded
    with open('./static/RSA_private_key.pem', 'wb') as pk:
        pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
        pk.write(pk_str)
        summary['Private Key'] = pk_str
    # Done - Generating a private key...
    # Generating a self-signed client certification...
    cert = create_self_signed_cert(pKey=key, named=name)
    with open('./static/Certificate.cer', 'wb') as cer:
        cer_str = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        cer.write(cer_str)
        summary['Self Signed Certificate'] = cer_str
    # Done - Generating a self-signed client certification...
    # Generating the public key...
    with open('./static/Public_key.pem', 'wb') as pub_key:
        pub_key_str = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
        #print("Public key = ",pub_key_str)
        pub_key.write(pub_key_str)
        summary['Public Key'] = pub_key_str
    # Done - Generating the public key...
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    open('./static/Container.pfx', 'wb').write(p12.export())
    # You may convert a PKSC12 file (.pfx) to a PEM format
    # Done - Generating a container file of the private key and the certificate...
    # To Display A Summary
    print("## Initialization Summary ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("############################################################################")
    return True


def sign_file2(input_file: str, signatureID: str, x_coordinate: int, 
            y_coordinate: int, pages: Tuple = None, output_file: str = None
              ):
    """Sign a PDF file"""
    # An output file is automatically generated with the word signed added at its end
    if not output_file:
        output_file = (os.path.splitext(input_file)[0]) + "_signed.pdf"
    # Initialize the library
    PDFNet.Initialize("demo:3443243432:322cf4b5b556c67b48855c44325c45c43543543545c666545c6545245")                                 ##### KEY ##### KEY ##### KEY ##### KEY ##### KEY ##### KEY ##### KEY ##### KEY ##### KEY #####
    doc = PDFDoc(input_file)
    # Create a signature field
    sigField = SignatureWidget.Create(doc, Rect(
        x_coordinate, y_coordinate, x_coordinate+100, y_coordinate+50), signatureID)
    # Iterate throughout document pages
    for page in range(1, (doc.GetPageCount() + 1)):
        # If required for specific pages
        if pages:
            if str(page) not in pages:
                continue
        pg = doc.GetPage(page)
        # Create a signature text field and push it on the page
        pg.AnnotPushBack(sigField)
    # Signature image
    sign_filename = os.path.dirname(
        os.path.abspath(__file__)) + "/static/star.jpg"        ##### IMAGE ##### IMAGE ##### IMAGE ##### IMAGE ##### IMAGE ##### IMAGE ##### IMAGE #####
    # Choosing certificate
    #pk_filename = os.path.dirname(
    #    os.path.abspath(__file__)) + "\static\Container.pfx"
    pk_filename = os.path.dirname(os.path.abspath(__file__)) + "/static/Container.pfx"
    # Retrieve the signature field.
    approval_field = doc.GetField(signatureID)
    approval_signature_digsig_field = DigitalSignatureField(approval_field)
    # Add appearance to the signature field.
    img = Image.Create(doc.GetSDFDoc(), sign_filename)
    found_approval_signature_widget = SignatureWidget(
        approval_field.GetSDFObj())
    found_approval_signature_widget.CreateSignatureAppearance(img)
    # Prepare the signature and signature handler for signing.
    #approval_signature_digsig_field.SignOnNextSave(pk_filename, '')
    approval_signature_digsig_field.SignOnNextSave(pk_filename, getpass())
    
    # The signing will be done during the following incremental save operation.
    doc.Save(output_file, SDFDoc.e_incremental)
    # Develop a Process Summary
    summary = {
        "Input File": input_file, "Signature ID": signatureID, 
        "Output File": output_file, "Signature File": sign_filename, 
        "Certificate File": pk_filename
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True


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
print ("                                                                                       ")
print ("  Fixed by @focab0r                                                                    ")
print ("---------------------------------------------------------------------------------------")


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
parser.add_argument('-n', '--name', dest='name',  type=str, help="Enter the name (Only when using -l)")



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
    #else:
    #    print ("Without a file, I don't know what you want me to sign, honey.")
    #    sys.exit()

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
        args.signatureID = "FirmaP4r4Abr1rLaRevers3Sh3ll" #Es broma ehhhh

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

    def _linux_set_time(time_tuple):
        import subprocess
        import shlex
        time_string = datetime(*time_tuple).isoformat()
        subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
        subprocess.call(shlex.split("sudo hwclock -w"))


    if sys.platform == 'linux2' or sys.platform == 'linux':
        if args.load:
            load(args.name)
        else: 
            _linux_set_time(time_tuple)
            sign_file2(
                    input_file=args.file, signatureID=args.signatureID,
                    x_coordinate=int(args.x_coordinate), y_coordinate=int(args.y_coordinate)
            )
            os.system("timedatectl set-timezone \"Europe/Madrid\" >/dev/null 2>&1")


