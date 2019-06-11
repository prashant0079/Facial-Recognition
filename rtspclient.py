#! /usr/bin/env python
# encoding: windows-1250
#
# Res Andy

import os, re, sys, time, socket, urllib2
camaddr = '192.168.42.1';
camport = 7878;

def wait_for_internet_connection():
  while True:
    try:
      response = urllib2.urlopen('http://%s' % camaddr,timeout=1)
      return
    except urllib2.URLError:
      pass

def main():
  srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  srv.connect((camaddr, camport))
 
  token = ''         
  while token == '':   
    time.sleep(1)
    print "Send"
    srv.send('{"msg_id":257,"token":0}')
    data = srv.recv(512)
    print "Receive: %s" % data
    if "rval" in data: 
      if len(re.findall('"param": (.+) }',data)) > 0:
        token = re.findall('"param": (.+) }',data)[0]
      else:
        token = ''
    else:
        data = srv.recv(512)
        if "rval" in data:
            token = re.findall('"param": (.+) }',data)[0]   
 
  if token != '':
    tosend = '{"msg_id":259,"token":%s,"param":"none_force"}' %token
    srv.send(tosend)
    srv.recv(512)
    print "Live webcam stream is now available."
    print 'Run VLC, select "Media"->"Open network stream" and open'
    print 'rtsp://%s/live' %camaddr
    print
    print "Press CTRL+C to end this streamer"
    
    while 1:
        time.sleep(1)

wait_for_internet_connection()
main()
