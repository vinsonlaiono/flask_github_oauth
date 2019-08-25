from flask import Flask, render_template, redirect, request, session
import requests
import re
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def root():

    return render_template("index.html")

@app.route("/redirect/github")
def github():

    print("*"*80)
    code = request.args.get('code') 
    print("Code: " + code)
    url = "https://github.com/login/oauth/access_token?client_id=a547ada0fca47c758f57&client_secret=e817fa8f3a2c0b2eff3abee3c5bc45621f00ec14&code="+code
    r = requests.post(url)
    l = re.split(r"=", r.text, 1)
    d = re.split(r"&", l[1])
    access_token = d[0]
    print("Access Token: "+  access_token)

    headers = {
        'Authorization': 'token '+access_token,
    }
    
    v = requests.get("https://api.github.com/user", headers=headers)
    k = v.json()
  
    session['name'] = k['name']
    session['img'] = k['avatar_url']
    return redirect('/user')

@app.route('/user')
def user():

    name = session['name']
    img = session['img']
    return render_template("/profile.html", name=name, img=img)

if __name__ == "__main__":
    app.run(debug=True)