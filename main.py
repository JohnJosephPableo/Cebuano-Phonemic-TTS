from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Phonemic CEB-TTS is working"

@app.route('/tokenize', methods=['GET'])
def tokenize():
    return "This will tokenize by word "

@app.route('/convert-pred', methods=['GET'])
def convertpred():
    return "This will convert predictable words"

@app.route('/convert-unpred', methods=['GET'])
def convertpred():
    return "This will convert unpredictable words"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")