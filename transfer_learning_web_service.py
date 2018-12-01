import os
from bottle import route, request, static_file, run
import classify_web_service as cws
import classify_multi_model_web_service as cmmws
@route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./js/')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css/')

@route('/images/<filename>')
def server_static(filename):
    return static_file(filename, root='./images/')

@route('/lib/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./lib/css/')

@route('/lib/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./lib/js/')

@route('/')
def root():
    return static_file('index.html', root='.')

@route('/index.html', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    
    if ext not in ('.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "C:/Users/Administrator/Desktop/clientDemoTransferLearning/AgroApple/upload/".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path,True)
    return cmmws.classify(file_path) #cws.classify(file_path)

if __name__ == '__main__':
    run(host='0.0.0.0', port=3003)

