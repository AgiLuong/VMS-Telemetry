# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


'''
USE NPY FILES
PLEASE

'''
from digi.xbee.devices import XBeeDevice
import os
from datetime import datetime
import binascii
'''
f = open('txt.txt', 'a', os.O_NONBLOCK)
while 1:
        f.write('asd')
        f.flush()
'''

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM7"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600


def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    if(os.path.isfile("log.txt")):
        os.remove("log.txt")
    f = open('log.txt', 'a')    

    try:
        device.open()

        def data_receive_callback(xbee_message):
            '''
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
            '''
            
            #m = xbee_message.data.decode()
            #m_s = m.split(" ")

            #time_stamp = datetime.fromtimestamp(float(m_s[-1]))
            #print(time_stamp.second,time_stamp.microsecond,m_s[1:2],m_s[3:-2])

            #f = open('log.txt', 'a', os.O_NONBLOCK)
            #print(m)
            #f.write(m+"\n")
            #f.write("\n")
            f.flush()
                            

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
