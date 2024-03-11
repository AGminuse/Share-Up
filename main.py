import os,sys
from flask import Flask, flash, request, redirect, url_for,abort,send_file,render_template
import zipfile
app = Flask(__name__)

app.secret_key = 'super secret key'

UPLOAD_FOLDER = './Uploads'
if not os.path.exists("./Uploads"):
    os.mkdir("./Uploads")


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
history=[]
@app.route('/', defaults={'req_path': ''},methods=['GET', 'POST'])
@app.route('/<path:req_path>',methods=['GET', 'POST'])
def dir_listing(req_path):
    if os.path.isfile("/tmp/tmp.zip"):
        os.remove("/tmp/tmp.zip")
    if "$return$" in req_path:
        print(history.pop())
        print(history)
        
    else:
        history.append(request.full_path)

    
    if "$createzip$" in req_path:
        Zip4Ship(request.full_path)
        return send_file("/tmp/tmp.zip")  
        
         
    if request.method == 'POST':
        if 'text' in request.args:
            print("no way it worked",request.form.get('textarea') )
        print(request.files)
        if 'file'  in request.files:
            print(request.files)
            files = request.files.getlist("file")
            for file in files:
                if not file.filename =="":
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    BASE_DIR = "./"
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_file(abs_path,as_attachment=True)

    folders=[]
    files=[]
    for item in os.listdir(abs_path):
        if os.path.isfile(item):
            files.append(item)
        else:
            folders.append(item)      
    return render_template("index.html",path=abs_path, files=files,folders=folders,forword=1,returnback=1)


def Zip4Ship(path):
    print(path)
    path=path[12:-1]

    with zipfile.ZipFile('/tmp/tmp.zip', 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                            os.path.relpath(os.path.join(root, file), 
                                            os.path.join(path, '..')))
        
        


if __name__ == '__main__':  
    args=sys.argv
    PORT=3333
    ADRESS="0.0.0.0"
    for i in range(len(args)):
        match args[i]:
            case "--help":
                print("i want some help")
                break
            case "--port":
                PORT=args[i+1]
            case "--adress":
                ADRESS=args[i+1].__str__()
    print("running on "+ADRESS.__str__()+":"+PORT.__str__())
    app.run(ADRESS,PORT)
