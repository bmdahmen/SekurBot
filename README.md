# SekurBot
SekurBot is a botnet framework that allows a master to store files on a bot-network, such that no bot has the original file, and not every bot is neccesary in order to retrieve the file. To accomplish this feat, SekurBot utilizes a cryptographic algorithm known as [Shamir's Secret Sharing ](http://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing), where a secret (in the form of a number) is divided into parts, giving each participant its own unique part(number), where some of or all of the parts are needed to reconstruct the secret.  

For example, if I would input the number 169 to Shamir's Algorithm requesting to split the number 6 ways such that only 4 are neccesary to recreate the number, Shamir might return the following 6 numbers:  
shamer_split(num=169,split=6,retrieve_num=4) = [153,3852,1502,45,295,2456]  

Later, in order to retrieve the number 169, Shamir only requires any combination of 4  out of the original six numbers:   
shamir_retrieve([1502,45,295,2456]) = 169  
shamir_retrieve([153,3852,2456,295]) = 169  
shamir_retrieve([45,2456,153,1502]) = 169  

# Applications
In order to extend this secret sharing beyond simply sharing numbers, we have decomposed files (16 bits at a time) into a stream numbers between 0 and (2^16) representing their binary value. We then pass this stream of numbers into shamir's splitting function one number at a time. Every bot that was online at the time of the request to share the file, gets their own unique number stream to store on disk along with a key to associate with that number stream (the file name). Since we do not require all of the number streams in order to recreate the original file (in the above example we only require 4/6), we do not require all the original bots to respond in order for us to recreate to file.  

This solves one of the biggest problems with distrubted file storage: availability. The master has fine-tuned control over the delicate balance between privacy and availability (If you only require two patries to recreate the file, it is easy to recreate if two of your bots are compromised and the shared prime between the master and the bots is known).  

# Usage
To begin, add the neccesary information to the CONFIG file for all the bots you are using. On the bot's machine (after you have ensured the bot appears on the master's roster) simply run ./xmpp_bot.py. This will start a listener that will wait for requests from your master machine.  

On the master, in order to share a file named "filename.txt" from the current directory. Here is some example output for this master, who has four bots on his roster  
$ ./sekur.py sharefile filename.txt  
Checking prescence for: bot1@54.191.94.255  
Checking prescence for: bot2@54.191.94.255  
Checking prescence for: bot3@54.191.94.255  
Checking prescence for: bot4@54.191.94.255  
You have 3 bots online.  
bot1@54.191.94.255 was online  
bot2@54.191.94.255 was online  
bot3@54.191.94.255 was online  
How many bots do you want to require to recreate your file?  
Note: must be less than or equal to 3  
$ 2  
Successfully shared with bot1@54.191.94.255  
Successfully shared with bot2@54.191.94.255  
Successfully shared with bot3@54.191.94.255  

Now, the file was stored on the bots machine. To view the shamir-distorted number stream on the bots machine, see data/filename.txt.   

At a later data the master can retrieve the file from the bots (if the minimum number of bots neccesary are online) by simply supplying the filename the secret was shared with  

$ ./sekur.py getfile filename.txt  
Checking prescence for: bot1@54.191.94.255  
Checking prescence for: bot2@54.191.94.255  
Checking prescence for: bot3@54.191.94.255  
Checking prescence for: bot4@54.191.94.255  
File written to data/filename.txt  

Go to data/filename.txt and if the minimum number of bots neccesary were online, your file should be waiting for you!  

# Install instructions.
python-dns - (sudo apt-get install python-dns)  
python-xmpp - (sudo apt-get install python-xmpp)   

# Troubleshooting

File "/usr/lib/python2.7/dist-packages/xmpp/simplexml.py", line 96, in _str_  
    if a: s = s + a._str_(fancy and fancy+1)  
TypeError: expected 0 arguments, got 1  

If you see this error while trying to share a secret (or retrieve a secret), open the listed file (in this case /usr/lib/python2.7/dist-packages/xmpp/simplexml.py)
and change the listed line (line: 96) to   
	if a: s = s + a._str_().  

This should fix the problem (if you can figure out what 'fancy' is doing here, I'd love to hear about it. Had little luck contacting xmppy team)  

# Contributors
Brian Dahmen - dahmen2  
Andrew Kowalski  - akkowal2  
Dan Zebrowski - dzebro2  
