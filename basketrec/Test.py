from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/login')
def login():
    resp = make_response("Giriş başarılı!")
    resp.set_cookie('token', 'abc12', httponly=True, samesite='Strict')
    return resp

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if token == 'abc123':
        return "Hoşgeldin, yetkilisin!"
    else:
        return "Yetkisiz erişim!", 401

if __name__ == '__main__':
    app.run(debug=True)