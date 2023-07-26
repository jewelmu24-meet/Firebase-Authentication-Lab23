from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config= { 
    'apiKey': "AIzaSyB5d3dYujqduAjpYulHM6lrN3F05s7UmqE",
    'authDomain': "jewels-1st-project.firebaseapp.com",
    'projectId': "jewels-1st-project",
    'storageBucket': "jewels-1st-project.appspot.com",
    'messagingSenderId': "59550051642",
    'appId': "1:59550051642:web:59c790ccad23f6a3e57403",
    'measurementId': "G-MTVLBG0ZW9",
    'databaseURL': "https://jewels-1st-project-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase= pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database() 


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=='GET':
        return render_template("signin.html")

    else:
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user']= auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))

        except:
            error ="authentication failed"
            return render_template('signup.html', e=email, p=password)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')

    else:
        email = request.form['email']
        password = request.form['password']
        fullname=request.form['fullname']
        username =request.form['username']
        bio = request.form['bio']

        user={'fullname': fullname, 'username': username, 'bio': bio, 'email':email}
        
        try:
            login_session['user']= auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))

        except:
            error ="authentication failed"
            return render_template('signup.html', e=email, p=password)


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method =='POST':
        title = request.form['title']
        text = request.form['text']
        UID = login_session['user']['localId']
        tweet = {'title': title, 'text': text, 'uid': UID}
        db.child("tweets").push(tweet)

    else:
        return render_template("add_tweet.html")

      
      
@app.route('/all_tweets') 
def alltweet():
    #if request.method =='GET':
    UID =login_session['user']['localId']
    tweet=db.child('tweets').child(UID).get().val()

    return render_template('tweets.html', tweets=tweets)  

if __name__ == '__main__':
    app.run(debug=True)


