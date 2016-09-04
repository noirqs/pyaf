from flask import Flask, jsonify, request #import objects from the Flask model

import WS_Backend as be;

app = Flask(__name__) #define app using Flask
backends = {};

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

def get_backend():
    backend = backends.get(request.remote_addr)
    if(backend is None):
        backend = be.cFlaskBackend();
        backends[request.remote_addr] = backend;
    return backend;



# MODELS

def jsonify_models():
    backend = get_backend();
    dict1 = backend.models
    return jsonify({'models' : [{'name': k, 'model': v.as_dict()} for k,v in dict1.items()]})    


# GET requests


@app.route('/models', methods=['GET'])
def returnAllModels():
    backend = get_backend();
    return jsonify_models();

@app.route('/model/<string:name>', methods=['GET'])
def returnOneModel(name):
    backend = get_backend();
    model = backend.get_model(name);
    if(model):
        return jsonify({'model' : model.as_dict()})
    return jsonify({})

# POST requests

@app.route('/model', methods=['POST'])
def addOneModel():
    backend = get_backend();
    print("JSON : " , request.json);
    print("JSON : " , request.__dict__);
    backend.add_model(request.json);
    return jsonify_models();

# PUT requests 


@app.route('/model/<string:name>', methods=['PUT'])
def editOneModel(name):
    backend = get_backend();
    backend.update_model(name , request.json['name']);
    model = backend.get_model(name);
    if(model):
        return jsonify({'model' : model.as_dict()})
    return jsonify({})

# DELETE requests

@app.route('/model/<string:name>', methods=['DELETE'])
def removeOneModel(name):
    backend = get_backend();
    backend.remove_model(name);
    return jsonify_models();

if __name__ == '__main__':
    app.run(host='192.168.88.88', debug=True, port=8080) #run app on port 8080 in debug mode
    