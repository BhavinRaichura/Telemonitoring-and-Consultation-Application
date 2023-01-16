from crypt import methods
from functools import wraps
from urllib import response
from flask import redirect, render_template, url_for, request,session,Response,jsonify
from flask_socketio import join_room, leave_room, emit, send,rooms
from application import app, socketio, socket_prog, db
from application.forms import LoginForm, RegisterForm
import uuid
from hashids import Hashids
from flask_login import login_user, logout_user, login_required,LoginManager
import pandas as pd


app.config['SECRET_KEY'] = 'as$$Gnz5H1H2bWvBbMnZ5A^XCcDsakjd54641254645449$^*efkjlksdmn&K$xz#@3205V@4#98yt4q23wqo!ADei'
hashids = Hashids( salt="as$$Gnz5H1H2bWvBbMnZ5A^XCcD&K$xz@3205V@4#98yt4qwertyuiopasdfghjklzxcvbnmMJQRT@#YU#IOPASDFGHJKLZXCVBNM1234567890q23wqo!ADei", min_length=10, alphabet="1234567890zxcvbnmASDFGHJKLPOIUYqwterQWERMZX")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'USER_ID' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap





@app.route('/')
def home():
    info={}
    info['USER_NAME'] = session.get('USER_ID')
    print(session.get('USER_ID'))
    return render_template('index.html',info = info )


@app.route('/create-meeting',methods=['get','post'])
def create_meeting():
    if session.get('USER_ID') is not None:
        USER_ID = str(session.get('USER_ID'))
        ROOM_ID = str(uuid.uuid4())
        PEER_ID = request.args.get('peer')
        print("\n\n\n-------\n\n{}".format(PEER_ID))
        
        room ={}
        room["ROOM_ID"]=f"{ROOM_ID}"
        room["USER_ID"]=f"{USER_ID}"
        room["PATIENT_ID"]=None
        room["PATIENT_NAME"]=None
        room["STATUS"]=0
        room["PEER_ID"]=PEER_ID
        
        meet = db.meets.insert_one(room)
        room.pop('_id')
        #3f1e8301-4f78-4650-b85e-b0a826af3127

        return jsonify(room)
    
    return redirect(url_for('home'))
    
    
    
@app.route('/patient',methods=('GET','POST'))
def patient():
    if request.method =='POST' and session.get('USER_ID')is not None:
        ROOM_ID = request.form['meetingId']
        
        datas = db.meets.find_one({'ROOM_ID':ROOM_ID})
        
        found = len([i for i in datas])
        
        if found == 0:
            return redirect(url_for('home'))
        
        if(datas['STATUS']==0 and datas['USER_ID'] != session.get('USER_ID')):
            return redirect(url_for('home'))
            
        """
        for i in datas:
            print("\n\n-------------------------------------------------------------")
            print(i)
            if ROOM_ID !=i['ROOM_ID'] or (i['PATIENT']!=None and i['PATIENT']!=session.get('USER_ID')):
                return redirect(url_for('home'))
            """
        ROOM_DETAILS = {}
        ROOM_DETAILS['USER_ID']=str(session.get('USER_ID'))
        ROOM_DETAILS['USER_NAME']=str(session.get('USER_NAME'))
        ROOM_DETAILS['ROOM_ID']=str(ROOM_ID)
        ROOM_DETAILS['IS_PATIENT'] =True 
        ROOM_DETAILS['PEER_ID'] = datas['PEER_ID'] 
        if datas['USER_ID'] == session.get('USER_ID'):
            ROOM_DETAILS['IS_ADMIN']= True
            if datas['STATUS']==0:
                datas['STATUS']==1
                db.meets.update_one({'ROOM_ID':ROOM_ID},{"$set":{"STATUS":1}}, upsert=True)
        else:
            ROOM_DETAILS['IS_ADMIN']= False
        print(f"admin--------------{ROOM_DETAILS['IS_ADMIN']}")
        
        return render_template('new_patient.html', ROOM_DETAILS = ROOM_DETAILS )
    
    return redirect(url_for('home'))

   


@app.route('/doctor', methods=('GET', 'POST'))
#@is_authenticated
def doctor():
    
    if request.method =='POST' and session.get('USER_ID')is not None:
        ROOM_ID = request.form['meetingId']
        
        datas = db.meets.find_one({'ROOM_ID':ROOM_ID})
        print("\n\n\n\n\nn\n")
        print(datas)
        if(datas['STATUS']==0 and datas['USER_ID'] != session.get('USER_ID')):
            return redirect(url_for('home'))
        
        ROOM_DETAILS = {}
        ROOM_DETAILS['USER_ID']=str(session.get('USER_ID'))
        ROOM_DETAILS['USER_NAME']=str(session.get('USER_NAME'))
        ROOM_DETAILS['ROOM_ID']=str(ROOM_ID)
        ROOM_DETAILS['IS_PATIENT'] =False
        ROOM_DETAILS['PEER_ID'] = str(datas['PEER_ID']) 
        if datas['USER_ID'] == session.get('USER_ID'):
            ROOM_DETAILS['IS_ADMIN']= True
            if datas['STATUS']==0:
                datas['STATUS']==1
                db.meets.update_one({'ROOM_ID':ROOM_ID},{"$set":{"STATUS":1}}, upsert=True)
        else:
            ROOM_DETAILS['IS_ADMIN']= False
        print(f"admin--------------{ROOM_DETAILS['IS_ADMIN']}")
        
        return render_template('new_doctor.html', ROOM_DETAILS = ROOM_DETAILS )
    
    return redirect(url_for('home'))
        

## user login / logout

@app.route('/logout')
def logout():
    session.pop('USER_ID',None)
    session.pop('USER_NAME',None)
    
    return redirect(url_for('home',msg='logout'))


@app.route('/login',methods=['POST','GET'])
def login():
    
    login_form = LoginForm()
    reg_form = RegisterForm()
    
    if session.get('username'):
        return redirect(url_for('home',msg='already login'))
    
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        
        db_user_info = db.user.find_one({'EMAIL':email})
        
        print(db_user_info)
        
        if db_user_info is not None and email == db_user_info['EMAIL'] and password == db_user_info['PASSWORD']:
            session['USER_ID']=db_user_info['USER_ID']
            session['USER_NAME']=db_user_info['USER_NAME']
            
            
            return redirect(url_for('home',msg='successfully login'))
            
    return render_template('child/login.html',reg_form=reg_form,login_form =login_form)


@app.route('/signup',methods=['POST','GET'])
def signup():
    
    reg_form = RegisterForm()
    login_form = LoginForm()
    
    if session.get('USER_NAME'):
        return redirect(url_for('home',msg='already login'))
    
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        
        check_user_excitance = db.user.find_one({'EMAIL':email})
        
        if check_user_excitance == None:
            count_user=int(db.command("collstats", "user")['count'])+1
            
            USER_ID = hashids.encode(count_user)
            
            db.user.insert_one({'USER_ID':USER_ID,'USER_NAME':username,'EMAIL':email,'PASSWORD':password})
            
            session['USER_ID']=USER_ID
            session['USER_NAME']=username
            
            return redirect(url_for('home',msg='New account successfully created'))
        
        return redirect(url_for('home',msg='Already have account'))
    
    return render_template('child/login.html',reg_form=reg_form,login_form =login_form)


############################################################################################################
# medical history

@app.route('/form/medical-history')
def form_medical_history():
    if(session.get('USER_ID') is not None):
        ques_df = pd.read_json('/home/bhavin/Desktop/tmcs (copy)/application/static/ques_data.json')
        ques_json = ques_df.to_dict()
        return render_template('form-medical-history.html', ques_json = ques_json, size = len(ques_json))
    return redirect(url_for('login'))
    



@app.route('/get-medical-history',methods=['GET','POST'])
def get_medical_history():
    
    if(session.get('USER_ID') is not None):
        patient_history = request.args.getlist
        print(f"\n----------form data---------\n{type(patient_history)}\n\n")
        print(patient_history)
        return redirect(url_for('home'))
    return redirect(url_for('login'))
    


@app.route('/show-patient-history/<string:USER_ID>')
def show_patient_history(USER_ID):
    check_user_excitance = db.user.find_one({'USER_ID':USER_ID})
    
    if check_user_excitance is not None:
        patient_med_history = db.medical_data.find_one({'USER_ID':USER_ID})
        
        if patient_med_history is not None:
            return jsonify(patient_med_history)
        
        pass
    # 
    #   
    pass


@app.route('/check-login-status')
@login_required
def check_login_status():
    return """<h1>called</h1>"""
