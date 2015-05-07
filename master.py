import xmpp
import sys
import ConfigParser
import shamir
import time

# cf = ConfigParser.ConfigParser()
# cf.read('CONFIG')
# server_ip = str(cf.get("Server","server_ip"))
# server_port = str(cf.get("Server","server_port"))
# master_jid = str(cf.get("Master","jid"))
# master_pass = str(cf.get("Master","password"))

class Master:
    def __init__(self, client, my_jid, server_ip, server_port, jidparams, jid):
        self.my_jid = my_jid
        self.jabber = client
        self.xmpp_connect(server_ip, server_port, jidparams, jid)
        self.bot_jids = None
        self.get_bot_jids()

    def xmpp_connect(self, server_ip, server_port, jidparams, jid):
        con=self.jabber.connect(server=(server_ip,server_port))
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        auth=self.jabber.auth(jid.getNode(),jidparams['password'])
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        self.register_handlers()
        return con

    def get_bot_jids(self):
        bot_jids = []
        for peer in self.jabber.getRoster().keys():
            bot_jids.append(peer)

        self.bot_jids = bot_jids

    def register_handlers(self):
        self.jabber.RegisterHandler('message', self.xmpp_message)

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat' 'result', None]:
            #here's where you recieve a message
            if event.getBody() is not None:
                message = event.getBody()

    def stdio_message(self, bot_jid, message):
        #I believe this is for sending files over xmpp
        m = xmpp.protocol.Message(to=bot_jid,body=message,typ='chat')
        self.jabber.send(m)
        pass

    def check_bot_prescence(self):
        botCount = 0
        bots = []
        for peer in self.bot_jids:
            if 'bot' in peer:
                print("Checking prescence for: " + str(peer))
                #mess = xmpp.protocol.Message(to=peer,body="p:p",typ='chat')
                m = xmpp.protocol.Iq(typ='get', to=peer + '/test', frm=self.my_jid, xmlns="jabber:client")
                m.setQueryNS(xmpp.NS_VERSION)
                reply = self.jabber.SendAndWaitForResponse(m,timeout=2)
                if(reply is not None):
                    resp=None
                    try:
                        resp = reply.getPayload()[1].data[0]
                    except:
                        print("Couldn't reach bot, maybe credential error")
                        continue
                    if resp=='p':
                        bots.append(peer)
                        botCount+=1
        return botCount, bots

    def share_secret(self, username, num_array):
        #print shares[0][1]
        payload="s:"+str(num_array[0])+":u:"+username
        print(payload)
        i = 0
        for peer in self.bot_jids:
            m = xmpp.protocol.Iq(typ='get', to=peer + '/test', frm=self.my_jid, xmlns="jabber:client", payload="s:"+"q"+":u:"+username)
            i+=1
            m.setQueryNS(xmpp.NS_VERSION)
            print(m)
            reply = self.jabber.SendAndWaitForResponse(m, timeout=2)
            if(reply is not None):
                resp=None
                try:
                    resp = reply.getPayload()[1].data[0]
                except:
                    print "error with the bot"
                    continue
                if resp=='s':
                    print "it was shared"

    def retrieve_secret(self, username, the_botcount, the_bots):
        i = 0
        numbers = []
        for peer in the_bots:
            m = xmpp.protocol.Iq(typ='get', to=peer + '/test', frm=self.my_jid, xmlns="jabber:client", payload="u:"+username)
            i+=1
            m.setQueryNS(xmpp.NS_VERSION)
            reply = self.jabber.SendAndWaitForResponse(m, timeout=2)
            if(reply is not None):
                resp=None
                try:
                    resp = reply.getPayload()[1].data[0]
                except:
                    print "error with the bot"
                    continue
                numbers.append(resp)
        numbers_as_tuples = []
        k = 1
        for num in numbers:
            numbers_as_tuples.append((k, int(num)))
            k+=1
        print numbers_as_tuples
        secret = shamir.joinSecret(numbers_as_tuples)
        return secret

# if __name__ == '__main__':
#     jidparams={'jid': master_jid, 'password': master_pass}
#     jid=xmpp.protocol.JID(jidparams['jid'])
#     cl=xmpp.Client(server_ip,debug=[])
#     master = Master(cl, jid)
#     (botcount, bots) = master.check_bot_prescence()
#     master.share_secret(13237, 5, botcount, bots, 'testname2')
#     time.sleep(2)
#     print master.retrieve_secret('testname2', botcount, bots)

