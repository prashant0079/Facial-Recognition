'''Multithreading Bottle server adapter.'''

import bottle
import mtwsgi



class MTServer(bottle.ServerAdapter):
    def run(self, handler):
        thread_count = self.options.pop('thread_count', None)
        server = mtwsgi.make_server(self.host, self.port, handler, thread_count, **self.options)
        server.serve_forever()



if __name__ == '__main__':
    from datetime import datetime
    import bottle
    from bottle import template,route,BaseTemplate,response,request,redirect, static_file, get
    import time
    import cv2
    import sqlite3
    import os
    import glob
    from TrainModel import TrainModel
    import face_recognition
    import imutils
    from ConnectToCamera import ConnectToCamera
    #from VideoCamera import VideoCamera
    import vlc
    import pickle
    from datetime import timedelta
    
    global dynamic_dict
    global button_clicked    
    button_clicked = 1
    #customroot=''
    customroot='/home/phoenix/facialrecognition/facialrecognition'
    #global default
    """default = {'pm!':'/dataset/pm!/aligned5.jpg',
               'prashant':'/dataset/prashant/aligned3.jpg',
               'tommy':'/dataset/tommy/download.jpeg',
               'shahrukh':'/dataset/shahrukh/681135.jpg',
               'Unknown':''}"""
    path_data = glob.glob('dataset/*')

    dynamic_dict = { glob.glob(each+'/*')[0].split('/')[1]:glob.glob(each+'/*')[0] for each in path_data}
    
    app = bottle.default_app()
    BaseTemplate.defaults['get_url'] = app.get_url  # reference to function
    
    #vc = cv2.VideoCapture(0)        
    
    def gen():
        global button_clicked
        data = pickle.loads(open("encodings.pickle", "rb").read())
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        player = vlc.MediaPlayer("rtsp://192.168.42.1/live")
        player.play()
        time.sleep(1)
        #vc = cv2.VideoCapture("rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov")
        #vc = cv2.VideoCapture(0)        
        """Video streaming generator function."""
        while button_clicked==0:
            #print(button_clicked)
            #print('Inside While')
            #rval, frame = vc.read()
            #cv2.imwrite('t.jpg', frame)
            #frame = vc.get_frame('encodings.pickle')
            #cv2.imwrite('t.jpg', frame)
            #yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
            #if button_clicked == 1:
            #    print("If, button_clicked==1: ", button_clicked)
            #    vc.release()
            #    cv2.destroyAllWindows()
            #    break
            
            player.video_take_snapshot(0, 'tmp.jpg', 0, 0)
            frame = cv2.imread('tmp.jpg')
            frame = imutils.resize(frame, width=500)
            
            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
            # detect faces in the grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                minNeighbors=5, minSize=(30, 30))
        
            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                    encoding)
                name = "Unknown"
        
                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
        
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
        
                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)
                
                # update the list of names
                names.append(name)
            
                #database            
                conn = sqlite3.connect('notification.db')
                for name in names:
                    if name != "Unknown":
                        c = conn.cursor()
                        d = timedelta(minutes = 5)
                        print(d)
                        c.execute("SELECT * FROM notif where name = ? AND time > ? ", (str(name), str(datetime.now()-d)))
                        print(str(datetime.now()-d))
                        result = c.fetchall()
                        c.close()
                        if len(result) < 1:
                            conn.execute("INSERT INTO notif (name, time, read, image) VALUES (?, ?, ?, ?)", (name, datetime.now(), 0, dynamic_dict[name]))
                            conn.commit()
                        
                conn.close()
        
            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 0, 255), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)
        
            # display the image to our screen
            cv2.imwrite("temp.jpg", frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('temp.jpg', 'rb').read() + b'\r\n')
            if button_clicked == 1:
                print("If, button_clicked==1: ", button_clicked)
                player.stop()
                #vc.release()
                #cv2.destroyAllWindows()
                break
            
            #player.stop()
#    def gen():
#        global button_clicked
#        #vc = cv2.VideoCapture("rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov")
#        #vc = cv2.VideoCapture(0)        
#        """Video streaming generator function."""
#        print("gen, button_clicked: ",button_clicked)
#        while button_clicked==0:
#            print("While, button_clicked==0: ",button_clicked)
#            print('Inside While')
#            rval, frame = vc.read()
#            cv2.imwrite('t.jpg', frame)
#            frame = vc.get_frame('encodings.pickle')
#            cv2.imwrite('t.jpg', frame)
#            yield (b'--frame\r\n'
#                   b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
#            if button_clicked == 1:
#                print("If, button_clicked==1: ", button_clicked)
#                vc.release()
#                cv2.destroyAllWindows()
#                break
    
    def database(names):
        #database            
        conn = sqlite3.connect('notification.db')
        for name in names:
            c = conn.cursor()
            d = timedelta(minutes = 5)
            print(d)
            c.execute("SELECT * FROM notif where name = ? AND time > ? ", (str(name), str(datetime.now()-d)))
            print(str(datetime.now()-d))
            result = c.fetchall()
            print(result)
            c.close()
            if len(result) < 1:
                conn.execute("INSERT INTO notif (name,time,read,image) VALUES (?, ?, ?, ?)", (name, datetime.now(),0, dynamic_dict[name]))
                print("In If len")
                conn.commit()
        
        conn.close()
    
    
    @route('/', name='video_feed')
    def video_feed():
        response.content_type = 'multipart/x-mixed-replace; boundary=frame'
        print("video_feed called")
        if button_clicked == 0:
            return gen()
        else:
            pass
    
    @route('/notificationCount')
    def notificationCount():        
        print("notificationCount called")
        conn = sqlite3.connect('notification.db')
        c = conn.cursor()
        c.execute("SELECT * FROM notif where read = ?", (False,))
        result = c.fetchall()
        print(result)
        print(len(result))
        c.close()
        return {str(len(result))}
    
    @route('/checkNotification')
    def checkNotification():        
        print("checkNotification called")
        conn = sqlite3.connect('notification.db')
        c = conn.cursor()
        d = timedelta(seconds = 20)
        print(d)
        c.execute("SELECT * FROM notif where time > ? ", (str(datetime.now()-d),))
        print(str(datetime.now()-d))
        result = c.fetchall()
        print(result)
        return {str(len(result))}
    
    @route('/stop', method='POST')
    def stop():
        global button_clicked        
        stop = request.forms.get('Stop')
        print("Stop Method: ",stop)
        start = request.forms.get('Start')
        print("Stop Method: ",start)
        connection = request.forms.get('Connect')
        print("Stop Method: ",connection)
        #7/14 
        notificationH = request.forms.get('NotificationH')
        print("Stop Method: ",notificationH)
        notificationP = request.forms.get('NotificationP')
        print("Stop Method: ",notificationP)
        namesH = ['Himanshu']
        namesP = ['PM']
        if stop == 'Stop':
            button_clicked = 1
        elif start == 'Start':
            button_clicked = 0
        elif connection == 'Connect':
            obj = ConnectToCamera()
            obj.wait_for_internet_connection('192.168.42.1')
            obj.connect('192.168.42.1', 7878)            
        elif notificationH == 'NotificationH':
            print("NotificationH")
            database(namesH)
        elif notificationP == 'NotificationP':
            print("NotificationP")
            database(namesP)
            
        print("Stop Method: ",button_clicked)
        redirect('/livestream')
        
        #return 'Stop Clicked'
#    @route('/index')
#    def load_index():
#        conn = sqlite3.connect('todo.db')
#        c = conn.cursor()
#        c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
#        result = c.fetchall()
#        c.close()
#        insertdata = template('landing_page_insertdata')
#        output = template('landing_page', template=insertdata)
#        return output
    
    @route('/<filename:path>', name='static')
    def serve_static(filename):
        return static_file(filename, root=customroot)
    
    
    @route('/image')
    @route('/index')
    def upload_image():
        directory = glob.glob('dataset/*')
        #print(directory)
        path = []
        for d in directory:
            path.append(glob.glob(d+'/*'))
        print(path)
        #dynamic_dict = { glob.glob(each+'/*')[0].split('/')[1]:glob.glob(each+'/*')[0] for each in path}
    
        #return template("gallery", image_names=images)
        #info = {'image_info': path}
        
        insertdata = template('image_page_insertdata', image_info=path)
        output = template('landing_page', template=insertdata)
        #output = template('landing_page', template=template('complete.tpl'))
        return output
    
    @route('/livestream')
    def load_image():
        insertdata = template('livestream_page_insertdata')
        output = template('landing_page', template=insertdata)
        return output
    
    @route('/notification')
    def load_notification():
        conn = sqlite3.connect('notification.db')
        c = conn.cursor()
        c.execute("SELECT name,time,image FROM notif ORDER BY time DESC")
        result = c.fetchall()
        print(result)
        print(len(result))
        c.close()
        insertdata = template('notification_page_insertdata',data=result)
        output = template('landing_page', template=insertdata)
        return output
    
    @route('/upload', method='POST')
    def do_upload():
        uname = request.forms.get('name')
        upload = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png', '.jpg', '.jpeg'):
            return "File extension not allowed."
    
        save_path = "dataset/{uname}".format(uname=uname)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    
        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path)
        #return "File successfully saved to '{0}'.".format(save_path)
        redirect('/image')
        #return "File successfully saved to '{0}'.".format(save_path)
        
    @route('/train', method='POST')
    def train():
        x = TrainModel()
        x.generate_pickle_file()
        return "stopped"
        
    @route('/connect', method='POST')
    def connect():
        obj = ConnectToCamera()
        obj.wait_for_internet_connection('192.168.42.1')
        obj.connect('192.168.42.1', 7878)
        return "connected"
        
    
        
    
    
    @get("/static/css/<filepath:re:.*\.css>")
    def css(filepath):
        return static_file(filepath, root="static/css")
    
    @get("/static/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
    def font(filepath):
        return static_file(filepath, root="static/fonts")
    
    @get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
    def img(filepath):
        return static_file(filepath, root="static/img")
    
    @get("/static/js/<filepath:re:.*\.js>")
    def js(filepath):
        return static_file(filepath, root="static/js")
        
        

    app.run(server=MTServer, host='0.0.0.0', port=8080, thread_count=10)
    #increase thread count

    # or:
    # httpd = mtwsgi.make_server('0.0.0.0', 8080, app, 3)
    # httpd.serve_forever()

