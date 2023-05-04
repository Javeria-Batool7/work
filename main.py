import random
import string
from firebase_admin import db , credentials
import firebase_admin
from datetime import datetime
import numpy as np
import cv2
from werkzeug.utils import secure_filename
# from tensorflow.keras.models import load_model
import json
random_key = ''.join(random.choices(string.ascii_lowercase, k = 6))

import pyrebase

config = {
  "apiKey": "AIzaSyAlRWyTvQ7u64QUF2p4Lc-FHZipsTr4kYE",
  "authDomain": "mdd-fyp.firebaseapp.com",
  "databaseURL": "https://mdd-fyp-default-rtdb.firebaseio.com",
  "projectId": "mdd-fyp",
  "storageBucket": "mdd-fyp.appspot.com",
  "messagingSenderId": "228158034299",
  "appId": "1:228158034299:web:13753825314f684b842dde",
  "measurementId": "G-BGC3FNK5PW"
}

firebase = pyrebase.initialize_app(config)
from firebase_admin import auth as auths
dbs = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from cassandra_flask_sessions import  CassandraSessionInterface

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "secret"
CassandraSessionInterface(app)
cred = credentials.Certificate("C:/Users/Ebad/Downloads/mdd-fyp-firebase-adminsdk-rauyu-8afebf5f87.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://mdd-fyp-default-rtdb.firebaseio.com/'})

database = db.reference()


@app.route('/')
def landing_page():
    return render_template("landing_page.html")

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        type_of_form = request.form.get("typee")
        if type_of_form == "signup":
            user_name = request.form['user_name']
            sign_up_mail = request.form['usermail']
            sign_up_pass = request.form['_password']
            user = auth.create_user_with_email_and_password(sign_up_mail,sign_up_pass)
            dbs.child('Users').update({user_name: user['localId']})
        elif type_of_form == "signin":
            user_email = request.form['username_']
            user_pass = request.form['password_']
            session['username_'] = request.form.get('username_')
            user = auth.sign_in_with_email_and_password(user_email,user_pass)
            session['username_'] = user
            auth.sign_in_with_email_and_password(user_email,user_pass)

    return render_template("login.html")

@app.route('/dashboard' , methods = ['GET' , 'POST'])
def dashboard():
    if 'username_' in session:
        email = session['username_']
        uid = email['localId']
        user_mail = auths.get_user(uid)
        emails = user_mail.email
        user_ref = database.child(uid)
        keys = user_ref.get()
        up = db.reference().get()
        if up is not None:
            for j in up:
                user_find = db.reference(j + '/user').get()
                if user_find is not None:
                    for i in user_find:
                        if i == uid:
                            val = db.reference(j + '/user').get()
                            value = val[uid]
                            hide_button = "<script>var gen_button = document.getElementById('genbutton').style.display = 'none';</script>"
                            hide_label = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
                            hide_entry = "<script>var gen_button = document.getElementById('gen__button').style.display = 'none';</script>"
                            hide_sub = "<script>var gen_button = document.getElementById('btn').style.display = 'none';</script>"
                            hide_label_or = "<script>var gen_button = document.getElementById('or').style.display = 'none';</script>"
                            hide_from_user = "<script>var gen_button = document.getElementById('hide_from_user').style.display = 'none';</script>"
                            msg = "Welcome", emails
                            msg_1 = "You are already registered into a Farm"
                            return render_template('dashboard.html', hide_button_script=hide_button, msg=msg_1,
                                                   hide=hide_label, hide_en=hide_entry, sub=hide_sub , hide_label_or = hide_label_or,
                                                   hide_from_user=hide_from_user)
                    else:
                        pass
                else:
                    pass

        if keys is not None:
            if request.method == 'POST':
                if request.form['gen'] == 'gen':
                    email = session['username_']
                    user_ids = email['localId']
                    key = random_key
                    dbs.child(user_ids).child('key').child(key).set(key)
            key_1 = db.reference(uid).get()
            key_val = key_1['key']
            val = key_val
            hide_label = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
            hide_entry = "<script>var gen_button = document.getElementById('gen__button').style.display = 'none';</script>"
            hide_sub = "<script>var gen_button = document.getElementById('btn').style.display = 'none';</script>"
            hide_label_or = "<script>var gen_button = document.getElementById('or').style.display = 'none';</script>"
            msg = "Your key is ", val
            counter_farm = db.reference(uid + '/key').get()
            count_farm = 0
            total_users = 0
            users_count = db.reference(uid + '/user').get()
            if users_count is None:
                pass
            else:
                for i in users_count:
                    total_users += 1
            for i in counter_farm:
                count_farm += 1
            farms_msg = 'Total farm you have: ', count_farm
            users_msg = 'Total users you have: ', total_users
            return render_template('dashboard.html', codes=msg, count_farm=farms_msg, hide=hide_label, hide_en=hide_entry,
                                   sub=hide_sub, users_total=users_msg , hide_label_or = hide_label_or)
            # if user_find is not None:
        #     for i in user_find:
        #         if i == uid:
        #           val = db.reference(key + '/key' ).get()
        #           hide_button =  "<script>var gen_button = document.getElementById('genbutton').style.display = 'none';</script>"
        #           hide_label = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
        #           hide_entry = "<script>var gen_button = document.getElementById('gen__button').style.display = 'none';</script>"
        #           hide_sub = "<script>var gen_button = document.getElementById('btn').style.display = 'none';</script>"
        #           msg = "Your key is " , val
        #         return render_template('home.html', hide_button_script=hide_button , codes = msg, hide = hide_label , hide_en = hide_entry, sub = hide_sub)
        else:
            try:
                if request.method == 'POST':
                    if request.form['subs'] == 'subs':
                        code = request.form['entry']
                        user_mail = session['username_']
                        user_id = user_mail['localId']
                        all_parents = db.reference()
                        parent_node = []
                        keys_node = []
                        is_present = all_parents.get()
                        for key in is_present:
                            parent_node.append(key)
                            for_sec_user = db.reference(key + '/key')
                            key_data = for_sec_user.get()
                            nodes_info = next(iter(key_data))
                            for i in key_data:
                                if i == code:
                                    dbs.child(key).child('user').update({user_id: i})

                    val = db.reference(key + '/user' + user_id).get()
                    hide_button = "<script>var gen_button = document.getElementById('genbutton').style.display = 'none';</script>"
                    hide_label = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
                    hide_entry = "<script>var gen_button = document.getElementById('gen__button').style.display = 'none';</script>"
                    hide_sub = "<script>var gen_button = document.getElementById('btn').style.display = 'none';</script>"
                    hide_label_or = "<script>var gen_button = document.getElementById('or').style.display = 'none';</script>"
                    hide_from_user = "<script>var gen_button = document.getElementById('hide_from_user').style.display = 'none';</script>"
                    msg_1 = "Your key is ", emails
                    msg = "You are already registered"
                    return render_template('dashboard.html', hide_button_script=hide_button, msg=msg, hide=hide_label,
                                           hide_en=hide_entry, sub=hide_sub ,hide_label_or=  hide_label_or, hide_from_user=hide_from_user)


            except:
                if request.method == 'POST':
                    if request.form['gen'] == 'gen':
                        email = session['username_']
                        user_ids = email['localId']
                        key = random_key
                        dbs.child(user_ids).child('key').child(key).set(key)
                key_1 = db.reference(uid).get()
                key_val = key_1['key']
                val = key_val
                hide_label = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
                hide_entry = "<script>var gen_button = document.getElementById('gen__button').style.display = 'none';</script>"
                hide_label_or = "<script>var gen_button = document.getElementById('gen_button').style.display = 'none';</script>"
                hide_sub = "<script>var gen_button = document.getElementById('btn').style.display = 'none';</script>"
                msg = "Your key is ", val

                return render_template('dashboard.html', codes=msg, hide=hide_label,
                                       hide_en=hide_entry, sub=hide_sub , hide_label_or= hide_label_or)
        return render_template('dashboard.html')

    if not session.get("username_"):
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')
@app.route('/information')
def information():
    return render_template('information.html')


@app.route('/upload-page', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        files = request.files.getlist('files[]')
        specie = request.form.get("specie_name")

        print(specie)

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S-%p")
        overview = {
            'Anthracnose': 0, 'Bacterial Canker': 0, 'Black Soothy Mold': 0, 'Gall Midge': 0, 'apoderus_javanicus': 0,
            'dappula_tertia': 0, 'dialeuropora_decempuncta': 0, 'icerya_seychellarum': 0, 'mictis_longicornis': 0,
            'neomelicharia_sparsa': 0, 'normal': 0
        }
        dicfor = ""
        for file in files:
            arr = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)
            img = cv2.resize(img, (256, 256))
            #newPrediction = model.predict(np.expand_dims(img, 0))
            img_dimensions = str(img.shape)
            disease_cure = [
                "Fungicides remain the most popular and most economical way to treat mangos for anthracnose. Treating mango trees before fruit develops and prior to fruit harvest is key to keeping the disease in check, and follow-up treatments after harvest further delay the onset of the disease.",
                # "The best way to control sooty mold fungi is using preventive method by eliminating their sugary food supply. Controlling sap-feeding insects on the foliage as well as ants that tend and protect them. General-purpose fungicide may be effective on killing fungi but not removing black color. Controlling ants by using barriers or insecticide baits is another control method. Pruning to remove most of the infested plant parts is helpful. If the tree is small, sooty mold can be washed off with a strong stream of water or soap and water.",
                "Regular inspection of orchards, sanitation, and seedling certification are recommended as preventive measures against the disease. Spray of copper-based fungicides has been found effective in controlling bacterial canker.",
                "The best way to control sooty mold fungi is using preventive method by eliminating their sugary food supply. Controlling sap-feeding insects on the foliage as well as ants that tend and protect them. General-purpose fungicide may be effective on killing fungi but not removing black color. Controlling ants by using barriers or insecticide baits is another control method. Pruning to remove most of the infested plant parts is helpful.",
                "Pesticides: Spraying of 0.05 percent fenitrothion, 0.045 percent dimethoate at bud burst stage of the inflorescence can be effective in controlling the pest. Foliar application of bifenthrin (70ml/100lit) mixed with water has also given satisfactory results. Sanitation: removing and destroying any heavily infested shoots, leaves, and fruits from the tree. Cultural practices: This can include removing any overgrown branches or leaves that create a humid environment that is conducive to the growth of the insects.",
                "Pesticides can be used to control the beetles on the tree.\n Sanitation: Proper sanitation of the orchard can help to reduce the population of the beetles. This includes removing and destroying any fallen fruit and debris from the tree, which can serve as a breeding ground for the beetles. Biological control: Using predators such as ladybugs, lacewing, and parasitic wasps can help to control the population of the beetles",
                "Pesticides: Insecticides can be applied to the trunk and branches of the tree to kill larvae and adult beetles. Cultural control: Keeping trees healthy by providing adequate water, fertilizer, and pruning can help to reduce the chances of infestation.",
                "Control of Dialeurodes infestation can be done through the use of pesticides and other control measures like using natural enemies of whitefly such as lady beetles, lacewings, and parasitic wasps."
                ,
                "insecticides such as horticultural oil, and insecticidal soap can be used for prevention. It was found that paraffin oil at 1.25% was the most effective insecticide"
                , "Control measures include the use of pesticides, pruning and removing infested branches"
                ,
                "The disease can be controlled by removing infected plant parts, and by applying fungicides. Cultural practices such as proper pruning and irrigation can also help prevent the disease from spreading."
                , "none"]
            disease_list = ['Anthracnose',
                            'Bacterial Canker',
                            'Black Soothy Mold',
                            'Gall Midge',
                            'apoderus_javanicus',
                            'dappula_tertia',
                            'dialeuropora_decempuncta',
                            'icerya_seychellarum',
                            'mictis_longicornis',
                            'neomelicharia_sparsa',
                            'normal']
            # print(newPrediction[0], "-_-_")
            # newPrediction1 = max(newPrediction[0])
            # index_pred = newPrediction[0].argmax()
            newPrediction1 = str(newPrediction1)
            # print(index_pred)
            # xx = disease_list[index_pred] + "@" + str(newPrediction1) + "@" + disease_cure[index_pred]
            # x = secure_filename(file.filename)
            # overview[disease_list[index_pred]] += 1
            #print(x)
            # print(xx)
            # dicfor += x + "@" + xx + "+"
            file.seek(0)
            # storage.child("users").child(session["user"]).child(dt_string).child(x).put(file, x)
            print("done")
        newdicfor = {
            dt_string: dicfor
        }
        print(newdicfor)
        over = {
            "overview": str(overview)
        }
        speciename = specie + "1"
        database.child("users").child(session["user"]).child(specie).update(newdicfor)
        database.child("users").child(session["user"]).child(speciename).update(over)
        print(dicfor, "-----------")
        return dicfor

        #

    return render_template("upload-page.html")

@app.route('/admin_user')
def admin_user():
    if not session.get("username_"):
        return redirect(url_for('login'))
    else:
        total_farm = db.reference('farms').get()
        farms_ref = dbs.child("farms_")
        farms = farms_ref.get().val()
        admins = []
        for farm_key in farms:
            farm = farms[farm_key]
            admin = farm.get("admin")
            loc = farm.get("location")
            name = farm.get("name")
            worker = farm.get("workers")
            farm_name = farm.keys()

            if admin and loc and name:
                admin_dict = ({"loc": loc, "name": name, "admin": admin , "workers": []  })
                worker_farm = farm.get("workers")
                # if worker_farm:
                #     for worker_key, worker_data in worker_farm.items():
                #             specie = worker_data.items()
                #             species = []
                #             for item in specie:
                #                 s = item[0]
                #                 species.append(s)
                #             for i in specie:
                #                 for j in i:
                #                     print(j)
                #                 print(i)
                                # key = list(worker_data[item[0]].keys())[0]
                                # value = list(worker_data[item[0]].values())[0]
                                # print (key, value)

                            # worker_name = worker_key


                            # Add the worker information to the admin dictionary
                            # admin_dict["workers"].append({"name": worker_name , "specie": species})
                admins.append(admin_dict)


            # workers_ref = db.reference('/farms_' + farm_key).get()
            # for worker_key in workers_ref:
            #     if worker_key not in ["admin", "location", "name"]:
            #         worker = workers_ref[worker_key]
            #         worker_name = worker_key
            #         specie = worker.get("specie")

                    # print(f"\tWorker Name: {worker_name}")
                    # print(f"\tSpecie: {specie}")
            if 'username_' in session:
                email = session['username_']
                uid = email['localId']




                #Access mail through Uid
                # user_mail = auths.get_user(uid)
                # emails = user_mail.email



        return render_template('admin_user.html' , total_farm = total_farm ,  admins=admins , farm = farm)
@app.route('/report' , methods=['GET', 'POST'])
def report():
    if not session.get("username_"):
        return redirect(url_for('login'))
    else:
        id = request.args.get('id')
        farm_name = request.args.get('farm_name')
        specie_name = request.args.get('specie_name')
        farms_ref = dbs.child("farms_")
        farms = farms_ref.get().val()
        admins = []
        for farm_key in farms:
            farm = farms[farm_key]
            admin = farm.get("name")
            s = dbs.child('farms_').child(farm_key).child('workers')
            sp = s.get().val()
            if admin == farm_name:
                admins.append(sp)
            lst_rep = []
            if request.method == 'POST':
                worker = request.form.get('worker_name')
                specie = request.form.get('specie')
                date = request.form.get('date')
                print([worker,specie,date])
            lst = []
            for worker_dict in admins:
                if worker_dict != None:
                    ###worker_name extract the name while repo_info is a list species,{date:report}
                    for worker_name, report_info in worker_dict.items():
                        lst.append(worker_name)
                        ##while iterate through report_info we get the spcies and {date:report} as a value
                        for key, value in report_info.items():
                            if key != 'specie':
                                lst.append(key)
                                key = key
                                value = value
                                #then iterate to the value to get the date only
                                for i in value:
                                    lst.append(i)







        return render_template('report.html', id=id , name = farm_name  , admins=admins  )

@app.route('/user_manager')
def user_manager():
    if 'username_' in session:
        email = session['username_']
        uid = email['localId']
        user_mail = auths.get_user(uid)
        emails = user_mail.email
        user_ref = database.child(uid + '/key')
        keys = user_ref.get()
        # for key, value in keys.items():
        #     value['created_at'] = datetime.strptime(value['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        # print(type(value['created_at']))
        farm_data = sorted(keys.items())

        user = database.child(uid + '/user').get()
        if user is not None:
            user_data = sorted(user.items())
            return render_template('user_manager.html', farm_key=farm_data, user_data=user_data)
        else:
            pass

        return render_template('user_manager.html', farm_key=farm_data)



if __name__ == "__main__":
    app.run(debug=True)