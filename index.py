from flask import Flask,render_template,redirect,url_for,request,jsonify
import json
import requests

app=Flask(__name__)

@app.route('/')
def home():
    return "Deepanshu"

@app.route('/summary',methods=['POST'])
def summarise():
    if request.method=="POST":
        data=request.form.get("data")
        word_count=int(request.form.get("word_count"))

    combine=[]
    headers = {"Authorization": "Bearer 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"}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    def query(payload):
        para = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=para)
        return json.loads(response.content.decode("utf-8"))
    output = query({
    "inputs": data,
    "parameters": {"do_sample": False,"min_length":int(word_count)+10,"max_length":int(word_count)+30},
    })
    combine.append(output[0]["summary_text"])


    API_URL2 = "https://api-inference.huggingface.co/models/google/pegasus-xsum"
    def query2(payload):
        response = requests.post(API_URL2, headers=headers, json=payload)
        return response.json()
    
    output2 = query2({
    "inputs":data
    })
    combine.append(output2[0]["summary_text"])
    return jsonify(combine)

if __name__=='__main__':
    app.run(debug=True)