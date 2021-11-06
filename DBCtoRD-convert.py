#DBC to RealDash XML Converter

import cantools
from pprint import pprint
path = 'C:/pathtodbc'
file = 'dbcfilename-noextension'
extension = '.dbc'
db = cantools.database.load_file(path + file + extension)

with open(path + file +'-converted.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write('\n')
    f.write('<RealDashCAN>')
    f.write('\n')
    f.write('<frames>')
    f.write('\n')

    for canmessage in db.messages:
        frameheader = '<frame canId="' + str(hex(canmessage.frame_id)) + '" endianess="little">  <!--' + canmessage.name + '-->'
        f.write(frameheader)
        f.write('\n')      
        print (frameheader)
        
        for cansignal in canmessage.signals:
            rd_name = 'name="' + str(canmessage.name) + "_" + cansignal.name + '"'
            rd_bits = 'units="bit"'
            rd_comment = str(cansignal.comment)
            if cansignal.length == 1:
                rd_offset = 'offset="' +str(cansignal.start // 8) +'"'
            else:
                rd_offset = 'offset="' +str(cansignal.start // cansignal.length) + '"'
            if cansignal.byte_order == 'little_endian':
                rd_endianness= 'endianess="little"'
            else:
                rd_endianness= 'endianess="big"'           
            if cansignal.length == 1:
                rd_length =  'length="1"'
            else:
                rd_length =  'length="' + str(int(cansignal.length / 8)) + '"'
            rd_unit = 'units="' + str(cansignal.unit) + '"'
            if cansignal.length ==1:
                rd_conversion = 'conversion="V>>' + str(cansignal.start % 8) + '"'
            else:
                if  cansignal.scale == 1:
                    rd_conversion = 'conversion="V"'
                elif cansignal.scale == 0.1:
                    rd_conversion = 'conversion="V/10"'
                elif cansignal.scale == 0.01:
                    rd_conversion = 'conversion="V/100"'
            if cansignal.is_signed == 1:
                rd_signed = 'signed="true"'
            else:
                rd_signed = 'signed="false"'

            
            if cansignal.length == 1: #bit map signal
                #check ok to do V>>0 
                line = "<value " + rd_name + " " + rd_bits + " " + rd_offset + " " + rd_length + " " + rd_conversion + "></value><!--Comment=" + rd_comment + "-->"
                print(line)
                f.write(line)
                f.write('\n')
            else: #byte(s) signal
                line = "<value " + rd_name + " " + rd_offset + " " + rd_length + " " + rd_unit + " " + rd_endianness + " " + rd_signed + " " + rd_conversion + "></value><!--Comment=" + rd_comment + "-->"
                print(line)
                f.write(line)
                f.write('\n')
            
        f.write("</frame>")
        f.write('\n')
    f.write("</frames>")
    f.write('\n')
    f.write("</RealDashCAN>")
    f.write('\n')

    #         # classcantools.database.can.Signal(name, start, length, byte_order='little_endian', is_signed=False, initial=None, scale=1, offset=0, minimum=None, maximum=None, unit=None, choices=None, dbc_specifics=None, comment=None, receivers=None, is_multiplexer=False, multiplexer_ids=None, multiplexer_signal=None, is_float=False, decimal=None)[source]
