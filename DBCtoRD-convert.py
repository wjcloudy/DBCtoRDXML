#DBC to RealDash XML Converter by wjcloudy

import cantools
import sys
import argparse
from pprint import pprint
parser = argparse.ArgumentParser("DBCtoRD-convert")
parser.add_argument("path", help="The path for the DBC ie: c:/this/path/", type=str)
parser.add_argument("filename", help="The filename for conversion ie: demo.dbc", type=str)
args = parser.parse_args()
print("Converting file at: " + args.path + args.filename)

db = cantools.database.load_file(args.path + args.filename,strict=False)
messagecount = 0
signalcount = 0
outputfile = args.path + args.filename +'-converted.xml'
with open(outputfile, 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write('\n')
    f.write('<!-- File created by DBCtoRDXML Converter https://github.com/wjcloudy/DBCtoRDXML -->')
    f.write('\n')
    f.write('<RealDashCAN version="2">')
    f.write('\n')
    f.write('\t<frames>')
    f.write('\n')

    for canmessage in db.messages:
        frameheader = '\t\t<frame canId="' + str(hex(canmessage.frame_id)) + '" endianess="little">  <!--' + canmessage.name + '-->'
        f.write(frameheader)
        f.write('\n')      
        messagecount += 1
        for cansignal in canmessage.signals:

            signalcount += 1
            rd_name = 'name="' + str(canmessage.name) + "_" + cansignal.name + '"'
            rd_nameenum = 'name="' + str(canmessage.name) + "_" + cansignal.name + '_enum"'
            rd_bits = 'units="bit"'
            rd_comment = str(cansignal.comment)
            rd_rangeMin = 'rangeMin="' + str(cansignal.minimum) + '"'
            rd_rangeMax = 'rangeMax="' + str(cansignal.maximum) + '"'
            rd_offset = 'offset="' +str(cansignal.start // 8) + '"'
            rd_startbit = 'startbit="' + str(cansignal.start) + '"'
            rd_bitcount = 'bitcount="' + str(cansignal.length) + '"'
            rd_conversion = "" #null out conversion value
            if cansignal.byte_order == 'little_endian':
                rd_endianness= 'endianess="little"'
            else:
                rd_endianness= 'endianess="big"'           
            if cansignal.length == 1:
                rd_length =  'length="1"'
            else:
                rd_length =  'length="' + str(int(cansignal.length / 8)) + '"'
            rd_unit = 'units="' + str(cansignal.unit) + '"'
            if cansignal.offset > 0:
                rd_bias =  "+" + str(cansignal.offset)
            elif cansignal.offset < 0:
                rd_bias =  str(cansignal.offset)
            else:
                rd_bias = ""
            if  cansignal.scale == 1 and cansignal.offset != 0:
                rd_conversion = 'conversion="V' +  rd_bias + '"'
            elif cansignal.scale < 1:
                rd_conversion = 'conversion="V/' + str(1/cansignal.scale) +  rd_bias + '"'
            elif cansignal.scale > 1:
                rd_conversion = 'conversion="V*' + str(cansignal.scale) +  rd_bias + '"'
            if cansignal.is_signed == 1:
                rd_signed = 'signed="true"'
            else:
                rd_signed = 'signed="false"'    
            if cansignal.choices is not None:
                rd_enum = 'enum="'
                for k in cansignal.choices:
                    rd_enum = rd_enum + str(k) + ":" + str(cansignal.choices[k]) + ","
                rd_enum = rd_enum + '#:err"'        
            if cansignal.length == 1: #bit map signal
                #check ok to do V>>0 
                line = "\t\t\t<value " + rd_name + " " + rd_bits + " " + rd_startbit + " " + rd_bitcount + "></value><!--Comment=" + rd_comment + "-->"
                f.write(line)
                f.write('\n')
                if cansignal.choices is not None: #Add text version of signal if lookup exists
                    line = "\t\t\t<value " + rd_nameenum + " " + rd_bits + " " + rd_startbit + " " + rd_bitcount + " " + rd_enum + "></value><!--Comment=" + rd_comment + "-->"
                    f.write(line)
                    f.write('\n')
            else: #byte(s) signal
                line = "\t\t\t<value " + rd_name + " " + rd_startbit + " " + rd_bitcount + " " + rd_unit + " " + rd_endianness + " " + rd_signed + " "  + rd_rangeMin + " " + rd_rangeMax + " "+ rd_conversion + "></value><!--Comment=" + rd_comment + "-->"
                f.write(line)
                f.write('\n')
                if cansignal.choices is not None: #Add text version of signal if lookup exists
                    line = "\t\t\t<value " + rd_nameenum + " " + rd_startbit + " " + rd_bitcount + " " + rd_unit + " " + rd_endianness + " " + rd_signed + " "  + rd_rangeMin + " " + rd_rangeMax + " "+ rd_conversion + " " + rd_enum + "></value><!--Comment=" + rd_comment + "-->"
                    f.write(line)
                    f.write('\n')
            
        f.write("\t\t</frame>")
        f.write('\n')
    f.write("\t</frames>")
    f.write('\n')
    f.write("</RealDashCAN>")
    f.write('\n')
print("Saved " + str(messagecount) + " messages (" +  str(signalcount) +" signals) to " + outputfile)
    #         # classcantools.database.can.Signal(name, start, length, byte_order='little_endian', is_signed=False, initial=None, scale=1, offset=0, minimum=None, maximum=None, unit=None, choices=None, dbc_specifics=None, comment=None, receivers=None, is_multiplexer=False, multiplexer_ids=None, multiplexer_signal=None, is_float=False, decimal=None)[source]
