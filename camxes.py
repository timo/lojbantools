#!/bin/env python
import os
import subprocess

__CAMXES_MD5SUM__ = "ce50b7c62ce94d46b073232b00afcfdc"
__CAMXES_URL__ = "http://www.digitalkingdom.org/~rlpowell/hobbies/lojban/grammar/rats/lojban_peg_parser.jar"

# uncomment the following line to turn off camxes md5 checking (this might be dangerous)
# __CAMXES_MD5SUM__ = ""

# if you have a camxes lying around somewhere, you can put the path to it here.
camxespath = ""

def find_camxes():
  global camxespath
  if camxespath:
    return camxespath
  valids = []
  try:
    locate = subprocess.Popen(["locate", "lojban_peg_parser.jar"], stdout=subprocess.PIPE)
    for found in locate.stdout.readlines():
      try:
        open(found.strip(), "r").close()
      except IOError:
        continue
      valids.append(found.strip())

    camxespath = valids[0]
    return camxespath
  except OSError:
    try:
      # see if the file has already been downloaded.
      camxespath = os.path.expanduser("~/lojban/lojban_peg_parser.jar")
      open(camxespath, "r")

      # if the open succeeded, we can use this path
      return camxespath
  
    except IOError:
      try:
        # try to download the file
        import md5
        import urllib2
      
        dl = urllib2.urlopen(__CAMXES_URL__)
        digest = md5.new()
      
        camxesdata = dl.read()
        digest.update(camxesdata)
      
        if digest.hexdigest != __CAMXES_MD5SUM__ and __CAMXES_MD5SUM__:
          print "downloaded camxes from the website, but the md5 did not match."
          raise

        lojbanfolder = os.path.expanduser("~/lojban")
        if not os.path.exists(lojbanfolder):
          os.mkdir(lojbanfolder)

        camxespath = os.path.join(lojbanfolder, "lojban_peg_parser.jar")
        open(camxespath, "w").write(dldata)
        return camxespath
      except:
        pass

  print "could not find camxes by using locate, looking into", os.path.expanduser("~/lojban/lojban_peg_parser.jar"), "nor by downloading it from", __CAMXES_URL__
  print "please get camxes by yourself."

def find_vlatai():
  return "vlatai"

camxesinstances = {}

def call_camxes(text, arguments=()):
  global camxesinstances
  arguments = tuple(arguments)
  if arguments in camxesinstances:
    sp = camxesinstances[arguments]
  else:
    camxesPath = find_camxes()
    sp = subprocess.Popen(["java", "-jar", camxesPath] + list(arguments),
                          stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    # eat the "hello" line for each of the arguments
    for arg in arguments:
      a = sp.stdout.readline()
    camxesinstances[arguments] = sp
  sp.stdin.write(text)
  sp.stdin.write("\n")
  a = sp.stdout.readline()
  #newline = sp.stdout.readline()
  return a

def call_vlatai(text):
  vp = find_vlatai()
  vi = subprocess.Popen([vp], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  vi.stdin.write(text)
  vi.stdin.write("\n")
  vi.stdin.close()
  res = vi.stdout.readline()
  data = [txt.strip() for txt in res.split(":")]
  return data

def selmaho(text):
  makfa = subprocess.Popen(["makfa", "selmaho", text], stdout=subprocess.PIPE)
  res = makfa.stdout.read().strip().split()
  word = res[0]
  selmaho = res[2]
  if "..." in selmaho:
      selmaho = selmaho.split("...")
  else:
      selmaho = [selmaho]
  links = res[3:]
  return (word, selmaho, links)
