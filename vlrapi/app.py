from flask import Flask, jsonify
from scraper import Vlr

app = Flask(__name__)

@app.route('/api')
def hello():
    return jsonify({'message': 'Hello, World!'})

vlr = Vlr()
@app.route('/latest')
def VLR_get_latest():
    return vlr.get_latest_data()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    #print(f"Running on http://{host}:{port}/")
    app.run(debug=True)
