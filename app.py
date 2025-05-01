from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)  # 모든 origin 허용
nlp = spacy.load("en_core_web_sm")

pos_kor = {
    "PRON": "대명사", "NOUN": "명사", "VERB": "동사", "ADJ": "형용사",
    "ADV": "부사", "DET": "관사", "AUX": "조동사", "INTJ": "감탄사",
    "SCONJ": "접속사", "ADP": "전치사"
}

dep_kor = {
    "nsubj": "주어", "ROOT": "동사", "attr": "보어", "dobj": "목적어",
    "prep": "전치사구", "advmod": "부사어", "amod": "형용어", "det": "관형어"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    sentence = request.json.get("sentence")
    doc = nlp(sentence)
    result = []
    for token in doc:
        result.append({
            "text": token.text,
            "pos": pos_kor.get(token.pos_, token.pos_),
            "dep": dep_kor.get(token.dep_, token.dep_)
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)