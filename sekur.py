#!/usr/bin/python
import sys, datetime, uuid
import ConfigParser
import xmpp
import master, shamir
import file_controller as fc
import numpy as np
cf = ConfigParser.ConfigParser()
cf.read('CONFIG')
master_jid = str(cf.get("Master","jid"))
master_pass = str(cf.get("Master","password"))
server_ip = str(cf.get("Server","server_ip"))
server_port = str(cf.get("Server","server_port"))

def print_help():
    """ Print usage instructions for the command-line library. """
    print ("Usage: ./sekur [command]")
    print ("./sekur help [command name] - display extended command information.\n")
    print ("Available commands:")
    print ("\t sharefile [filepath/filename]")
    print ("\t getfile [filename]")

def print_command_help(command):
    """ Display extended help information for CLI command
        :param command: SekurBot command name"""
    COMMANDS = \
        { "sharesecret": \
            "Share a secret split amongst available bots such that only k pieces are neccesary " \
            + "to retrieve the original secret" , \
          "retrievesecret": \
            "Query the bots in an attempt to recreate the secret stored under given username." \
            + " Note, only the first k available bots attached to the master account will be used"
        }
    if command in COMMANDS:
        print (COMMANDS[command])
    else:
        print ("Unknown command!")
        print_help()

def collect_k(botcount, online_bots):
    print("You have " + str(botcount)  + " bots online.")
    for bots in online_bots:
        print(str(bots) + " was online")
    mesg ="How many bots do you want to require to recreate your file?\n"
    mesg += "Note: must be less than or equal to "+str(botcount) +'\n'  
    inp = raw_input(mesg)
    return inp


def share_file(file_path, master):
    raw_bin_nums = fc.split_file(file_path)
    (botcount, online_bots) = master.check_bot_prescence()
    if(botcount==0):
        print("You do not have any bots online. Run ./xmpp_bot.py on your bot's pc with their info")
        print("Under the Slave section of the config")
        return
    k = collect_k(botcount, online_bots)
    a=[]
    for bots in range(botcount):
        a.append("")
    for orig_num in raw_bin_nums:
        splitList =shamir.splitSecret(orig_num, botcount,int(k))
        count = 0
        for nums in splitList:
            a[count] = a[count] + ","+ str(nums[1])        
            count+=1
    master.share_file(file_path,a,online_bots)


def get_file(username, the_master):
    (botcount, online_bots) = the_master.check_bot_prescence()
    the_master.get_file(username, botcount, online_bots)

def init():
    jidparams={'jid': master_jid, 'password': master_pass}
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client(server_ip,debug=[])
    master_bot = master.Master(cl, jid, server_ip, server_port, jidparams, jid)
    return master_bot
     

def process_command(command):
    """ Process a command-line command and execute the 
        resulting SekurBot action
        :param command: The command to be executed, as a sys arg array
    """
    if len(sys.argv) < 2:
        print_help()
        return
    command = sys.argv[1].lower()
    if command == 'help':
        if (len(sys.argv) == 3):
            print_command_help(sys.argv[2])
        else:
            print_help()
    elif command == 'sharefile':
        if (len(sys.argv) == 3):
            master = init()
            share_file(sys.argv[2], master)
        else:
            print_help()
    elif command == 'getfile':
        if (len(sys.argv)==3):
            master = init()
            get_file(sys.argv[2], master)
        else:
            print_help()
    else:
        print_help()

if __name__ == '__main__':
   process_command(sys.argv)
 