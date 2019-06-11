# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 00:40:34 2018

@author: hmagg
"""
import threading
import glob
import sqlite3
import bottle
from bottle import route, run, debug, template, static_file, get, request, response, BaseTemplate, redirect
import os
app = bottle.default_app()
BaseTemplate.defaults['get_url'] = app.get_url
from TrainModel import TrainModel
import cv2
from queue import Queue, Empty

button_pressed = Queue()

#global stop_variable
#stop_variable =  False
vc = cv2.VideoCapture(0)

"""if __name__ == '__main__':
    threading.Thread(target=run, kwargs=dict(host='localhost', port=8080)).start()"""
    

def gen():
    """Video streaming generator function.
    global stop_variable
    #stop_variable = ""
    while (True):
        #print('Inside While')
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        print(stop_variable)
        if stop_variable:
            vc.close()
            break"""
    running = True
    while running:
        try:
            button_pressed.get_nowait()
            running = False
            vc.release()
            
            
        except Empty:
            #print('Inside While')
            rval, frame = vc.read()
            cv2.imwrite('t.jpg', frame)
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        
        
@route('/stop', method='POST')
def stop():
    #global stop_variable
    #stop_variable = request.forms.get('submit')
    #stop_variable = True
    #print(stop_variable)
    button_pressed.put(1)
    print(button_pressed)
    return "stopped"

        
@route('/', name='video_feed')
def video_feed():
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    return gen()
    #global stop_variable
    #stop_variable = False
    

#if __name__ == '__main__':
@route('/index')
def load_index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    insertdata = template('landing_page_insertdata')
    output = template('landing_page', template=insertdata)
    return output

@route('/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='/home/phoenix/facialrecognition/')


@route('/image')
def upload_image():
    directory = glob.glob('dataset/*')
    #print(directory)
    path = []
    for d in directory:
        path.append(glob.glob(d+'/*'))
    print(path)    

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
def load_image():
    insertdata = template('notification_page_insertdata')
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

#debug(True)
#run(reloader=True)
#run()



if __name__ == '__main__':
    threading.Thread(target=run, kwargs=dict(host='localhost', port=8080)).start()
    threading.Thread(target = gen).start()