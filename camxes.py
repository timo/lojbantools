#!/bin/env python
import os
import subprocess

__CAMXES_MD5SUM__ = "ce50b7c62ce94d46b073232b00afcfdc"
__CAMXES_URL__ = ("http://www.digitalkingdom.org/~rlpowell/hobbies/lojban/"
                  "grammar/rats/lojban_peg_parser.jar")

# uncomment the following line to turn off camxes md5
# checking (this might be dangerous)
# __CAMXES_MD5SUM__ = ""

# if you have a camxes lying around somewhere, you can put the path to it here.
camxespath = ""


class CouldNotFindCamxesError(Exception):
    pass


def download_camxes(url=None):
    if not url:
        url = __CAMXES_URL__

    try:
        import md5
        import urllib2

        download = urllib2.urlopen(__CAMXES_URL__)
        digest = md5.new()

        camxesdata = download.read()
        digest.update(camxesdata)

        if (digest.hexdigest() != __CAMXES_MD5SUM__ and
               __CAMXES_MD5SUM__):
            print ("downloaded camxes from the website, "
                  "but the md5 did not match.")
            raise

        lojbanfolder = os.path.expanduser("~/lojban")
        if not os.path.exists(lojbanfolder):
            os.mkdir(lojbanfolder)

        camxespath = os.path.join(lojbanfolder,
                                  "lojban_peg_parser.jar")
        open(camxespath, "w").write(camxesdata)
        return camxespath
    except:
        pass
    
    return None


def locate_camxes():
    locate = subprocess.Popen(["locate", "lojban_peg_parser.jar"],
                              stdout=subprocess.PIPE)
    
    valids = []
    
    for found in locate.stdout.readlines():
        try:
            open(found.strip(), "r").close()
        except IOError:
            continue
        valids.append(found.strip())

    if not valids:
        raise CouldNotFindCamxesError()

    camxespath = valids[0]
    return camxespath


def find_camxes():
    global camxespath
    if camxespath:
        return camxespath
    
    try:
        camxespath = locate_camxes()
        if camxespath:
            return camxespath

    except (OSError, CouldNotFindCamxesError):
        try:
            # see if the file has already been downloaded.
            camxespath = os.path.expanduser("~/lojban/lojban_peg_parser.jar")
            open(camxespath, "r")

            # if the open succeeded, we can use this path
            return camxespath

        except IOError:
            camxespath = download_camxes()
            if camxespath:
                return camxespath

    print "could not find camxes by using locate, looking into",
    print os.path.expanduser("~/lojban/lojban_peg_parser.jar"),
    print "nor by downloading it from", __CAMXES_URL__
    print "please get camxes by yourself."

    raise CouldNotFindCamxesError()


def find_vlatai():
    return "vlatai"


camxesinstances = {}


def call_camxes(text, *arguments):
    global camxesinstances
    if not isinstance(arguments, tuple):
        arguments = tuple(arguments)

    if arguments in camxesinstances:
        instance = camxesinstances[arguments]

    else:
        camxesPath = find_camxes()
        instance = subprocess.Popen(["java", "-jar", camxesPath] + list(arguments),
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # eat the "hello" line for each of the arguments
        for _ in arguments:
            a = instance.stdout.readline()
        camxesinstances[arguments] = instance

    instance.stdin.write(text + "\n")

    result = ""

    # if camxes is started with -t, it will not print two newlines at the end
    if "-t" in arguments:
        delim = "\n"
    else:
        delim = "\n\n"
    while not result.endswith(delim):
        result += instance.stdout.read(1)

    return result.strip()


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
    makfa = subprocess.Popen(["makfa", "selmaho", text],
                             stdout=subprocess.PIPE)
    res = makfa.stdout.read().strip().split()
    word = res[0]
    selmaho_res = res[2]
    if "..." in selmaho_res:
        selmaho_res = selmaho_res.split("...")
    else:
        selmaho_res = [selmaho_res]
    links = res[3:]
    return (word, selmaho_res, links)
