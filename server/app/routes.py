from app import app

@app.route('/')
@app.route('/chat')
def index():
    return "Hey sp!"