import xmpp
import sys
import ConfigParser
import shamir
import time
import file_controller

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

    def share_file(self, username, num_array, online_bots):
        payload="s:"+str(num_array[0])+":u:"+username
        i = 0
        for peer in online_bots:
            m = xmpp.protocol.Iq(typ='get', to=peer + '/test', frm=self.my_jid, xmlns="jabber:client", payload="s:"+str(num_array[i])+":u:"+username)
            i+=1
            m.setQueryNS(xmpp.NS_VERSION)
            reply = self.jabber.SendAndWaitForResponse(m, timeout=4)
            if(reply is not None):
                resp=None
                try:
                    resp = reply.getPayload()[1].data[0]
                except:
                    print "error with the bot"
                    continue
                if resp=='s':
                    print "Successfully shared file with " + str(peer)

    def get_file(self, username, the_botcount, the_bots):
        i = 0
        numbers = []
        values = []
        magic_numbers = []
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

                resp_list = resp.split(",")
                resp_list = resp_list[1:]
                if values == []:
                    for num in resp_list:
                        values.append([int(num)])
                else:
                    x = 0
                    for num in resp_list:
                        values[x].append(int(num))
                        x += 1

        for parts in values:
            k = 1
            numbers_as_tuples = []
            for part in parts:
                numbers_as_tuples.append((k, int(part)))
                k += 1
            magic_numbers.append(shamir.joinSecret(numbers_as_tuples))

        file_controller.get_file(magic_numbers,username)
        return magic_numbers