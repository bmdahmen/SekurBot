#!/usr/bin/python2
import re
import sys,os,xmpp,time,select, socket
import socket, subprocess
import ConfigParser
from xmpp import *

cf = ConfigParser.ConfigParser()
cf.read('CONFIG')
server_ip = str(cf.get("Server","server_ip"))
server_port = str(cf.get("Server","server_port"))
master_jid = str(cf.get("Master","jid"))
bot1_jid = str(cf.get("Slave","jid1"))
bot1_pass = str(cf.get("Slave","password"))

class Bot:
    def __init__(self,jabber,remotejid, masterjid):
        self.jabber = jabber
        self.remotejid = remotejid
        self.masterjid = masterjid

    def register_handlers(self):
        self.jabber.RegisterHandler('message',self.xmpp_message)
        self.jabber.RegisterHandler('iq', self.iqHandler)

    def send(self, username, value):
        with open('data/' + username + '.txt', 'w') as file:
            file.write(value)

    def retrieve(self, username):
        with open('data/' + username + '.txt', 'r') as file:
            data = file.read()
        return data

    def iqHandler(self, conn,iq_node):
        """ Handler for processing some "get" query from custom namespace"""
        print('in iq handler')
        reply=iq_node.buildReply('result')
        cmd = iq_node.getQueryPayload()
        print cmd
        # ... put some content into reply node
        if not cmd:
            reply.addChild(name="data", namespace=xmpp.NS_DATA, payload=['p'])
        #getting around the list of nodes that the bot receives as the first message
        #shit workaround
        elif len(cmd) > 2:
            reply.addChild(name="data", namespace=xmpp.NS_DATA, payload=['p'])
        else:
            number_split = cmd[0].split(':')
            print number_split[0]
            if str(number_split[0]) == 's':
                number = number_split[1].strip()
                username = number_split[3].strip()
                self.send(username, number)
                reply.addChild(name="data", namespace=xmpp.NS_DATA, payload=['s'])
            else:
                username = number_split[1].strip()
                number = self.retrieve(username)
                reply.addChild(name="data", namespace=xmpp.NS_DATA, payload=number)

        conn.send(reply)
        raise xmpp.NodeProcessed  # This stanza is fully processed

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        print(type)
        if type in ['message', 'chat', 'get', 'iq', None]:
            #here's where you recieve a message
            if event.getBody() is not None:
                message = event.getBody()
                message_list = message.split(':')
                type = str(message_list[0]).strip()
                print("type: " + str(type))
                if type.lower() == 's':
                    username = str(message_list[1]).strip()
                    value = str(message_list[2]).strip()
                    print("username: " + str(username))
                    print("value: " + str(value))
                    self.send(username, value)
                elif type.lower() == 'r':
                    username = str(message_list[1]).strip()
                    data = self.retrieve(username)
                    print("username: " + str(username))
                    print("Data retrieved: " + data)
                    self.stdio_message(con, event, data)
                elif type.lower() == 'p':
                    print("Presence check request")
                    self.stdio_message(con, event, 'p')

    def stdio_message(self, con, event, message):
        #I believe this is for sending files over xmpp
        #m = xmpp.protocol.Message(to=self.masterjid,body=message,typ='chat')
        m = event.buildReply('result')
        print(str(m))
        self.jabber.send(m)
        raise xmpp.NodeProcessed
        pass

    def xmpp_connect(self):
        con=self.jabber.connect(server=(server_ip,server_port))
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'], resource='test')
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
        self.register_handlers()
        return con

if __name__ == '__main__':
    jidparams={'jid': bot1_jid, 'password': bot1_pass}
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client(server_ip,debug=[])

    bot=Bot(cl,bot1_jid, master_jid)
    if not bot.xmpp_connect():

        sys.stderr.write("Could not connect to server, or password mismatch!\n")
        sys.exit(1)
    socketlist = {cl.Connection._sock:'xmpp',sys.stdin:'stdio'}
    print 'here3'
    cl.sendInitPresence()
    print 'here2', master_jid
    myRoster =  cl.getRoster()
    print 'here', master_jid
    sys.stderr.write(master_jid)
    myRoster.Subscribe(master_jid)
    #Register yourself so you can talk to your master... not necessary every time you run, but necessary the first time you run
    #Each side of the conversation needs to "friend" each other. Subscribe makes it so the bot "friend requests" you.
    #Authorize makes it so the Bot "accepts your friend request"
    online = 1
    auth=False
    while online:
        (i , o, e) = select.select(socketlist.keys(),[],[],1)
        if(auth is False):
            thing = myRoster.Authorize(master_jid)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
