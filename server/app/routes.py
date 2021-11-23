from app import app

@app.route('/')
@app.route('/chat')
def chat():
    return "Hey sp!"


# @app.route('/login')
# def login():
    