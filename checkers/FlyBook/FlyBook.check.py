#!/usr/bin/env python2
import sys
import requests
import random
from bs4 import BeautifulSoup
from PIL import Image
import os

OK = 101
NO_FLAG = 102
INVALID_PROTOCOL = 103
DOWN = 104
FATAL_ERROR = 110

PORT = 80

GROUP_EXISTS = 150
TIMEOUT = 30

def registration(login, password, realName, imageFile):
  sys.stderr.write('Attempting to create user %s:%s, name %s, photo %s\n' % (login, password, realName, imageFile))
  host = address.split('.')[-1]
  sys.stderr.write('Correctify profile photo %s to %s\n' % (imageFile, imageFile + "." + host + ".png"))
  os.system('./correctify.py %s %s' % (imageFile, host))
  imageFile = imageFile + "." + host + ".png"
  r = requests.post('http://%s/registration.php' % address, data={'login': login, 'password': password, 'name': realName}, files={'photo': open(imageFile, 'rb')}, timeout = TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'login.php?registration=1':
    sys.stderr.write('Status code %d, url %s, headers %s\n' % (r.status_code, r.url, r.headers))
    print "Can't create new user"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')

  try:
    f = open("data/logins.%s.txt" % address, 'a')
    f.write("%s::%s::%s\n" % (login, password, realName))
    f.close()
  except:
    pass
  return OK

def signin(login, password):
  sys.stderr.write('Attempting to login %s:%s\n' % (login, password))
  r = requests.post('http://%s/login.php' % address, data={'login': login, 'password': password}, timeout=TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'profile.php' or r.cookies['session'] == '':
    sys.stderr.write('Status code %d, headers %s\n' % (r.status_code, r.headers))
    print "Can't login"
    return (INVALID_PROTOCOL, None)
  sys.stderr.write('Success!\n')
  session = r.cookies['session']
  sys.stderr.write('Session %s\n' % session)
  return (OK, session)

def editProfile(login, password, session, params):
  sys.stderr.write('Attempting to edit profile on session %s, params %s\n' % (session, params))
  data = {'name': params['name'], 'loved_companies': params['loved_companies'], 'loved_airplanes': params['loved_airplanes']}
  if params['isopen'] == True:
    data.update({'isopen': '1'})
  r = requests.post('http://%s/edit.php' % address, data=data, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'profile.php':
    sys.stderr.write('Status code %d, headers %s\n' % (r.status_code, r.headers))
    print "Can't edit profile"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')
  try:
    f = open("data/private.%s.txt" % address, 'a')
    f.write("%s::%s::%s\n" % (login, password, params['name']))
    f.close()
  except:
    pass
  return OK

def createGroup(session, id, name, description, isopen):
  sys.stderr.write('Attempting to create group on session %s, id %s, name %s, description %s, isopen %s\n' % (session, id, name, description, isopen))
  data = {'id': id, 'name': name, 'description': description}
  if isopen:
    data.update({'isopen': 1})
  r = requests.post('http://%s/profile.php' % address, data=data, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 200:
    sys.stderr.write('Status code %d\n' % r.status_code)
    print "Can't create group"
    return INVALID_PROTOCOL
  soup = BeautifulSoup(r.content)
  if len(soup.findAll(True, {'class': "text-error"})) != 0:
    error = soup.findAll(True, {'class': 'text-error'})[0]
    if error.find("Group with same id already exists") != -1:
      return GROUP_EXISTS
    sys.stderr.write('Found %s\n' % soup.findAll(True, {'class': 'text-error'}))
    print "Can't create group"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')

  if isopen:
    try:
      f = open("data/groups.%s.txt" % address, 'a')
      f.write("%s::%s\n" % (id, name))
      f.close()
    except:
      pass
  return OK

def postToProfile(session, login, post):
  sys.stderr.write('Attempting to post to profile %s on session %s, post %s\n' % (login, session, post))
  r = requests.post('http://%s/profile.php?login=%s' % (address, login), data={'post': post}, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'profile.php?login=%s' % login:
    sys.stderr.write('Status code %d, headers %s\n' % (r.status_code, r.headers))
    print "Can't post message to wall"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')
  return OK

def postToGroup(session, id, post):
  sys.stderr.write('Attempting to post to group %s on session %s, post %s\n' % (id, session, post))
  r = requests.post('http://%s/group.php?id=%s' % (address, id), data={'post': post}, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'group.php?id=%s' % id:
    sys.stderr.write('Status code %d, headers %s\n' % (r.status_code, r.headers))
    print "Can't post message to group"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')
  return OK

def generateLogin(name = None):
  if name == None:
    len = random.randint(8, 10)
    result = ''
    for i in xrange(len):
      result += chr(random.randint(ord('a'), ord('z')))
    return result
  else:
    (name, surname) = name.split()
    return name.lower() + '.' + surname.lower() + str(random.randint(1, 10))

def generatePassword():
  len = random.randint(10, 15)
  result = ''
  for i in xrange(len):
    result += chr(random.randint(ord('a'), ord('z')) if random.randint(1, 2) == 1 else random.randint(ord('0'), ord('9')))
  return result

def generateName():
  names = map(str.rstrip, open('names').readlines())
  name = random.choice(names)
  surnames = map(str.rstrip, open('surnames').readlines())
  surname = random.choice(surnames)
  return name + ' ' + surname

def generateUser():
  password = generatePassword()
  name = generateName()
  login = generateLogin(name)
  allPhotos = os.listdir("images")
  allPhotos = filter(lambda x: x.count(".") == 1, allPhotos)
  photo = 'images/' + random.choice(allPhotos)
  return (login, password, name, photo)

def generateGroup():
  type = random.randint(1, 1)
  if type == 1:
    airline = random.choice(open('airlines').readlines()).rstrip()
    airline = ' '.join(airline.split(' ')[:3])
    id = airline.lower().replace(' ', '.').replace('_', '.').replace('(', '').replace(')', '').replace('..', '.') + '.' + str(random.randint(1, 99))
    description = "Fanclub of %s. Join to our group!" % airline
    return (id, airline, description)

def generatePostToGroup(id, name):
  messages = [ 'Welcome to our group "%s"!' % name,
               'Hey girls! I love %s too :)' % name,
               "Let's be friends! How are you?"
             ]
  return random.choice(messages)

def generateLovedCompanies():
  airlines = open('airlines').readlines()
  count = random.randint(1, 5)
  result = [random.choice(airlines).rstrip() for i in xrange(count)]
  return ", ".join(list(set(result)))

def generateLovedAirplanes():
  airplanes = ['Tu-154', 'Boeing A320', 'Boeing B737', 'Boeing A340', 'Airbus', 'F-22', 'Tu-214', 'Il-2', 'Saab 91', 'MiG 1.44', 'Yac-42', 'Bumblebee-1']
  count = random.randint(1, 3)
  result = [random.choice(airplanes).rstrip() for i in xrange(count)]
  return ", ".join(list(set(result)))

def generateMessageToProfile(fromName, toLogin):
  messages = [ "Hi %s! I am %s. We saw at Tu-154. Are you remember me? How are you?" % (toLogin, fromName),
               "Wonderful day! How are you, %s?" % toLogin,
               "Call me, friend! Md5 of my number is ade56413e18cac955f84fbfabeca7743",
               "Will you be at our party, %s? I will wait you" % toLogin, 
               "Do you love Vim-avia airlines? Join to my group!" ]
  return random.choice(messages)

def getOldLoginPassword():
  try:
    all = open("data/logins.%s.txt" % address).readlines()
    private = open("data/private.%s.txt" % address).readlines()
  except:
    return None
  all = list(set(all) - set(private))
  if len(all) == 0:
    return None
  return random.choice(all).rstrip().split("::")

def sendMessage(login1, session, login2, message):
  sys.stderr.write('Attempting to send message %s on session %s, from %s, to %s\n' % (message, session, login1, login2))
  r = requests.post('http://%s/messages.php' % address, data={'to': login2, 'message': message}, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 302 or r.headers['location'] != 'messages.php':
    sys.stderr.write('Status code %d, headers %s\n' % (r.status_code, r.headers))
    print "Can't post message to another user"
    return INVALID_PROTOCOL
  sys.stderr.write('Success!\n')
  return OK 

def getPostsInGroup(session, groupId):
  sys.stderr.write('Attempting to get posts in group %s on session %s\n' % (groupId, session))
  r = requests.get('http://%s/group.php?id=%s' % (address, groupId), cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 200:
    sys.stderr.write('Status code %d' % r.status_code)
    print "Can't get posts in the group"
    return INVALID_PROTOCOL
  soup = BeautifulSoup(r.content)
  posts = soup.findAll(True, {'class': "wall-message"})
  return posts

def getMessages(session):
  sys.stderr.write('Attempting to get messages on session %s\n' % session)
  r = requests.get('http://%s/messages.php' % address, cookies={'session': session}, timeout=TIMEOUT)
  if r.status_code != 200:
    sys.stderr.write('Status code %d' % r.status_code)
    print "Can't get messages"
    return INVALID_PROTOCOL
  soup = BeautifulSoup(r.content)
  messages = soup.findAll(True, {'class': 'message'})
  return messages

def getOldLoginPasswordOrCreate():
  old = getOldLoginPassword()
  if old == None:
    login, password, name, photo = generateUser()
    reg = registration(login, password, name, photo)
    if reg != OK: return reg
  else:
    login, password, name = old
  return (login, password, name)

def getOldGroup():
  try:
    all = open("data/groups.%s.txt" % address).readlines()
  except:
    return None
  all = list(set(all))
  if len(all) == 0:
    return None
  return random.choice(all).rstrip().split("::")
 

def check():
  type = random.randint(1, 5)
  if type == 1:
    login, password, name, photo = generateUser()
    reg = registration(login, password, name, photo)
    if reg != OK: return reg
    return OK

  old = getOldLoginPasswordOrCreate()
  if old == INVALID_PROTOCOL: return old
  login, password, name = old
  log, session = signin(login, password)
  if log != OK: return log
 
  if type == 2:
    editParams = {'name': name, 'loved_companies': generateLovedCompanies(), 'loved_airplanes': generateLovedAirplanes(), 'isopen': True}
    edit = editProfile(login, password, session, editParams)
    if edit != OK: return edit

  if type == 3:
    while True:
      groupId, groupName, groupDescription = generateGroup()
      create = createGroup(session, groupId, groupName, groupDescription, True)
      if create != OK and create != GROUP_EXISTS: return create
      if create == OK:
        break

  if type == 4:
    old = getOldLoginPassword()
    if old != None:
      login, _, _ = old
      post = postToProfile(session, login, generateMessageToProfile(name, login))
      if post != OK: return post

    old = getOldGroup()
    if old != None:
      groupId, groupName = old
      postGroup = postToGroup(session, groupId, generatePostToGroup(groupId, groupName))
      if postGroup != OK: return postGroup

  return OK

def put(id, flag):
  type = random.randint(1, 3)
  if type == 1:
    (login, password, name, photo) = generateUser()
    reg = registration(login, password, name, photo)
    if reg != OK: return reg
    (log, session) = signin(login, password)
    if log != OK: return log

    while True:
      (id, groupName, description) = generateGroup()
      group = createGroup(session, id, groupName, description, False)
      if group != OK and group != GROUP_EXISTS: return group
      if group == OK:
        break

    postMessage = generatePostToGroup(id, groupName)
    post = postToGroup(session, id, postMessage)
    if post != OK: return post
    post = postToGroup(session, id, flag)
    if post != OK: return post
    print "1::%s::%s::%s" % (login, password, id)
  if type == 2:
    login, password, name, photo = generateUser()
    login = flag
    reg = registration(login, password, name, photo)
    if reg != OK: return reg
    (log, session) = signin(login, password)
    if log != OK: return log           
    editParams = {'name': name, 'loved_companies': generateLovedCompanies(), 'loved_airplanes': generateLovedAirplanes(), 'isopen': False}
    edit = editProfile(login, password, session, editParams)
    if edit != OK: return edit
    print "2::%s::%s" % (login, password)
  if type == 3:
    login, password, name, photo = generateUser()
    old = getOldLoginPassword()
    if old == None:
      login2, password2, name2, photo2 = generateUser()
      reg = registration(login2, password2, name2, photo2)
      if reg != OK: return reg
    else:
      login2, password2, name2 = old

    reg = registration(login, password, name, photo)
    if reg != OK: return reg
    log, session = signin(login, password)
    if log != OK: return log

    sendMessage(login, session, login2, flag)
    print "3::%s::%s" % (login, password)
  return OK

def get(id, flag):
  params = id.split("::")
  type = params[0]
  sys.stderr.write("Get flag %s\n" % id)
  if type == "1":
    login, password, groupId = params[1:]
    log, session = signin(login, password)
    if log != OK: return log
    posts = getPostsInGroup(session, groupId)
    if posts == INVALID_PROTOCOL: return NO_FLAG
    sys.stderr.write("Posts: %s\n" % posts)
    for post in posts:
      if str(post).find(flag) != -1:
        sys.stderr.write("Found at %s\n" % post)
        return OK
    return NO_FLAG
  if type == "2":
    login, password = params[1:]
    log, session = signin(login, password)
    if log != OK: return NO_FLAG
    return OK
  if type == "3":
    login, password = params[1:]
    log, session = signin(login, password)
    if log != OK: return NO_FLAG
    messages = getMessages(session)
    if messages == INVALID_PROTOCOL: return NO_FLAG      
    sys.stderr.write("Messages: %s\n" % messages)
    for message in messages:
      if str(message).find(flag) != -1:
        sys.stderr.write("Found at %s\n" % message)
        return OK
    return NO_FLAG

if len(sys.argv) < 2:
  sys.exit(FATAL_ERROR);
(mode, address) = sys.argv[1:3]

try:
  if mode == "check":
    sys.exit(check())
  if mode == "put":
    if len(sys.argv) != 5:
      sys.exit(FATAL_ERROR)
    sys.exit(put(sys.argv[3], sys.argv[4]))
  if mode == "get":
    if len(sys.argv) != 5:
      sys.exit(FATAL_ERROR)
    sys.exit(get(sys.argv[3], sys.argv[4]))
except requests.exceptions.ConnectionError:
  print "Host seems down"
  sys.exit(DOWN)
except requests.exceptions.Timeout:
  print "Host seems down"
  sys.exit(DOWN)
