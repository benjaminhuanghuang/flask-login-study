https://flask-login.readthedocs.io/en/latest/

When session protection is active, each request, it generates an identifier for the user’s computer (basically, 
a secure hash of the IP address and user agent). If the session does not have an associated identifier, the one 
generated will be stored. If it has an identifier, and it matches the one generated, then the request is OK.