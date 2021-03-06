import os, re, sys, time, socket
import urllib.request
#camaddr = '192.168.42.1';
#camport = 7878;


class ConnectToCamera(object):
    def wait_for_internet_connection(self, camaddr):
        while True:
            try:
                response = urllib.request.urlopen('http://%s' % camaddr, timeout=1)
                print(response)
                return
            except urllib.error.URLError:
                pass

    def connect(self, camaddr, camport):
          srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          srv.connect((camaddr, camport))
         
          token = ''         
          while token == '':   
            time.sleep(1)
            print("Send")
            srv.send(b'{"msg_id":257,"token":0}')
            data = srv.recv(512)
            print("Receive: %s" % data)
            if b"rval" in data: 
              if len(re.findall(b'"param": (.+) }',data)) > 0:
                token = re.findall(b'"param": (.+) }',data)[0]
              else:
                token = ''
            else:
                data = srv.recv(512)
                if b"rval" in data:
                    token = re.findall(b'"param": (.+) }',data)[0]   
         
          if token != '':
            tosend = b'{"msg_id":259,"token":%s,"param":"none_force"}' %token
            srv.send(tosend)
            srv.recv(512)
            print("Live webcam stream is now available.")
            print('Run VLC, select "Media"->"Open network stream" and open')
            print('rtsp://%s/live' %camaddr)
            print
            print("Press CTRL+C to end this streamer")
            
            while 1:
                time.sleep(1)

        
