#!/usr/bin/python2
import re
import sys,os,xmpp,time,select, socket
import socket
import subprocess
from xmpp import *
class Bot:
    def __init__(self,jabber,remotejid):
        self.jabber = jabber
        self.remotejid = remotejid

    def register_handlers(self):
        self.jabber.RegisterHandler('message',self.xmpp_message)

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None]:
            #here's where you recieve a message
            if event.getBody() is not None:
                print(event.getBody()) 
    def stdio_message(self, message):
        #I believe this is for sending files over xmpp
        m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
        self.jabber.send(m)
        pass

    def xmpp_connect(self):
        con=self.jabber.connect(server=('54.191.94.255','5222'))
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'],resource='crappy_script')
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
        self.register_handlers()
        return con

if __name__ == '__main__':
    jidparams={'jid': 'bot_dahmen2@54.191.94.255', 'password': 'WW1U3sZfe'}
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client('54.191.94.255',debug=[])
    bot=Bot(cl,'bot_dahmen2@54.191.94.255')

    if not bot.xmpp_connect():
        sys.stderr.write("Could not connect to server, or password mismatch!\n")
        sys.exit(1)
    socketlist = {cl.Connection._sock:'xmpp',sys.stdin:'stdio'}
    cl.sendInitPresence()
    myRoster =  cl.getRoster()

    #Register yourself so you can talk to your master... not necessary every time you run, but necessary the first time you run
    #Each side of the conversation needs to "friend" each other. Subscribe makes it so the bot "friend requests" you.
    #Authorize makes it so the Bot "accepts your friend request"
    masterAccount = sys.argv[1]
    online = 1
    auth=False
    while online:
        (i , o, e) = select.select(socketlist.keys(),[],[],1)
        if(auth is False):
            thing = myRoster.Authorize(masterAccount)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
