import xmpp
import sys


class Master:
    def __init__(self, client, my_jid):
        self.my_jid = my_jid
        self.jabber = client
        self.xmpp_connect()
        self.get_bot_jids()

    def xmpp_connect(self):
        con=self.jabber.connect(server=('54.191.94.255','5222'))
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'])
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
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
        for peer in self.bot_jids:
            if 'bot' in peer:
                print("Checking prescence for: " + str(peer))
                #mess = xmpp.protocol.Message(to=peer,body="p:p",typ='chat')
                m = xmpp.protocol.Iq(typ='get', to=peer + '/test', frm=self.my_jid, xmlns="jabber:client")
                m.setQueryNS(xmpp.NS_VERSION)
                reply = self.jabber.SendAndWaitForResponse(m)
                print(str(reply))


if __name__ == '__main__':
    jidparams={'jid': 'akkowal2@54.191.94.255', 'password': 'Ewo13IWEr'}
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client('54.191.94.255',debug=[])

    master = Master(cl, jid)
    master.check_bot_prescence()

