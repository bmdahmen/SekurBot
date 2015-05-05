# SekurBot
SekurBot is a botnet framework that allows a master to store a 'secret' on slave-hosts, such that no bot has the original secret, and not neccesarily every bot is neccesary in order to retrieve that secret. To accomplish this feat, SekurBot utilizes a cryptographic algorithm known as [Shamir's Secret Sharing ](http://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing), where a secret is divided into parts, giving each participant its own unique part, where some of or all of the parts are needed to reconstruct the secret.

# Applications
The applications extend far beyond sharing 'secrets'(in the form of a 4-5 digit number). For example, a binary file could be decomposed into a stream of sufficiently large numbers and sent to each host. Intercepting a single bot's secret-stream would not be helpful towards reconstructing the secret. Later on, when the master wants to retrieve the secret, he doesn't need to rely on all the bots to be present in order for the original file to be reconstructed. 

# Usage
./sekur sharesecret key secret k

This will give you a dialogue telling you how many bots on your master account are available to send data to. With this information in hand, you can intelligently select k, the number of bots that are neccesary to be present when you recreate your secret. 

After your secret is stored on the bot machines, to retrieve your secret at any time:

./sekur retrievesecret key

This will iterate through the bots and recreate your secret with the first k bots that respond. If less than k bots are available, you will be told your retrieval failed

# Install instructions.
python-dns is neccesary on the master (sudo apt-get install python-dns)

