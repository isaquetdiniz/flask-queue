from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_message():
    return {
        "App": "microservice-python",
        "Status": "develop",
        "Author": "Isaque Diniz"
    }

@app.route('/methods', methods=['GET', 'POST'])
def link_products():
    if request.method == 'POST':
        data = request.get_json()
        return  {
            "message": "Post Method"
        }
    else:
        return {
            "message": "Get Method!"
        }   