 # Python Messenger
 A messenger program written in Python that allows two users to send messages to one another.
 One user must run the script as the server with a port number and the other connects using port and IP address.
 <code>messenger.py</code> only allows for text messages to be sent and <code>messenger_with_files.py</code> allows sending messages or files.
 
  ## Usage for Messenger
  Server: <code>python messenger.py -l \<port number></code><br>
  Client: <code>python messenger.py \<port number> [\<server address>]</code>
  
  ## Usage for Messenger with Files
  Server: <code>python messenger_with_files.py -l \<listening port number></code><br>
  Client: <code>python messenger_with_files.py -l \<listening port number> -p \<connect server port> [-s] [connect server address]</code>
