#!/usr/bin/python
import sys, datetime, uuid
import ConfigParser
import xmpp
import master

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
    print ("\tsharesecret [username] [secret] [k]")
    print ("\tretrievesecret [username]")

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

def share_secret(username, secret, k, the_master):
    print("Sharing is caring")
    (botcount, bots) = the_master.check_bot_prescence()
    print(botcount)
    #the_master.share_secret(int(secret), int(k), botcount, bots, username)

def retrieve_secret(username, the_master):
    print("go get it son")
    (botcount, bots) = the_master.check_bot_prescence()
    print the_master.retrieve_secret(username, botcount, bots)

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
    elif command == 'sharesecret':
        if (len(sys.argv) == 5):
            master = init()
            share_secret(sys.argv[2], sys.argv[3], sys.argv[4], master)
        else:
            print_help()
    elif command == 'retrievesecret':
        if (len(sys.argv)==3):
            master = init()
            retrieve_secret(sys.argv[2], master)
        else:
            print_help()
    else:
        print_help()

if __name__ == '__main__':
   process_command(sys.argv)
