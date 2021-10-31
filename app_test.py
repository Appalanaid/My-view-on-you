from flask import Flask, render_template, redirect, url_for, Response, request, session
from camera import VideoCamera, LoginCamera
from flask_sqlalchemy import SQLAlchemy
import os, glob, shutil
from flask_session import Session

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///facereco.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
global st

class FaceReco(db.Model):
    faceid=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(200),nullable=False)
    lname=db.Column(db.String(200),nullable=False)
    mailid=db.Column(db.String(200),nullable=False)
    passcode=db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f" {self.faceid} - {self.mailid}"

@app.route('/')
def index_():
    if os.path.isfile('./logged.txt'):
        os.remove("./logged.txt")
    return render_template('home.html')
# @app.route('/home',methods=['GET','POST'])
# def home():
#         global st
#         ret=request.args.get('ret')
#         print("ret",ret)
#         file_list = glob.glob('test.png')
#         st=st+".png"
#         if len(file_list) > 0:
#            os.rename('test.png', st)
#            shutil.move(st, "faces");
#         # os.remove(st)
#         return render_template('home.html')

@app.route('/index')
def index():
    # al=FaceReco.query.all()
    return render_template('index.html')

@app.route('/show',methods=['GET','POST'])
# def show():
#     ret=0
#     res=request.args.get('query')
#     ret=str(res)
#     if ret=='0':
#         return render_template('show.html',qry=ret)
#         # return("User Not Found")vitvittanala2002@gmail.comtanala2002@gmail.com
#     elif ret=='1':
#         global st
#         # print("ret",ret)
#         file_list = glob.glob('test.png')
#         st=st+".png"
#         if len(file_list) > 0:
#            os.rename('test.png', st)
#            shutil.move(st, "faces");
#         return render_template('show.html',qry=ret)
#         # return("Registered Successfully")
#     elif ret=='3':
#         return render_template('show.html',qry=ret)
#         # return("User Already Registered")
#     elif ret=='2':
#         os.remove("userdetails.txt")
#         return render_template('show.html',qry=ret)
#         # return render_template('show.html')
#     return render_template('show.html',qry=ret)
def show():
    res=request.args.get('query')
    file_list = glob.glob('test.png')
    st=session["mailid"]
    st=st+".png"
    p=os.getcwd()
    c=os.path.join(p,"faces")
    if st not in os.listdir(c) and len(file_list)>0:
        c=os.getcwd()
        shutil.move("test.png", "faces");
        c=os.path.join(c,"faces")
        os.chdir(c)
        os.rename('test.png', st)
        os.chdir(p)
    return render_template('show.html',qry=res)


def gen(cam):
    while True:
        try:
            frame = cam.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if os.path.isfile('logged.txt'):
                return render_template('show?query=2')
        except Exception as e:
            return render_template('show?query=2')        


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/login_feed')
def login_feed():
    return Response(gen(LoginCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/register', methods=['GET','POST'])
def about_page():
    global st
    if request.method== 'POST':
        name1=request.form['fname']
        name2=request.form['lname']
        mail=request.form['email']
        password=request.form['passcode']
        al=FaceReco.query.filter_by(mailid=mail).first()
        if (type(al).__name__ != "NoneType"):
            return redirect('show?query=3')
        reco=FaceReco(fname=name1,lname=name2,mailid=mail,passcode=password)
        db.session.add(reco)
        db.session.commit()
        # al=FaceReco.query.filter_by(mailid=mail).first()
        session["mailid"]=mail
    return render_template('register-cam.html')




@app.route('/login',methods=['GET','POST'])
def home_page():
    if request.method== 'POST':
        file1 = open("userdetails.txt","w")
        mail=request.form['namail']
        password=request.form['napasscode']
        al=FaceReco.query.filter_by(mailid=mail, passcode=password).first() 
        # print("al",al)
        # print("al",type(al))
        if (type(al).__name__ == "NoneType"):
            return redirect('show?query=4')
        file1.write(str(al.mailid)+"_")
        file1.write(str(al.fname)+" "+str(al.lname))
        file1.close()
        # print("got this",mail,password)
    return render_template('login-cam.html')



if __name__ == "__main__":
    app.run(debug=1)