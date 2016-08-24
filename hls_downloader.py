import sys
import os
from urlparse import urlparse
from urlparse import urljoin
import urllib2
import commands

args = sys.argv
print args
m3u8UrlString = args[1]
outputFile = args[2]

# make work directory
tmpDir = "tmp" + outputFile + "/"
if not os.path.exists(tmpDir):
    os.mkdir(tmpDir)

def extractFilename(url):
    path = urlparse(url).path
    return os.path.basename(path)

parts = []
request = urllib2.urlopen(m3u8UrlString)
for m3u8Line in request:
    if m3u8Line == "" or m3u8Line.startswith("#"):
        # skip
        continue
    targetUrl = urljoin(m3u8UrlString, m3u8Line)
    print ("part of ts: %s" % targetUrl)

    partNameOfTs = extractFilename(targetUrl)

    with open(tmpDir + partNameOfTs, "w") as out:
        ts = urllib2.urlopen(targetUrl)
        out.write(ts.read())

    print "wrote to " + tmpDir + partNameOfTs
    parts.append(partNameOfTs)

if 0 < len(parts):
    command = ("cd %s;cat %s > ../%s" % (tmpDir, " ".join(parts), outputFile))
    print command
    commands.getstatusoutput(command)

rmcommand = ("rm -rf %s" % (tmpDir))
print rmcommand
commands.getstatusoutput(rmcommand)