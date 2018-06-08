andrew = {
	'username': 'Andrew',
	'password': 'federals',
	'email': 'tiddandrew@gmail.com',
}

def get_credentials(name):
  if name is not None:
    return eval(name)