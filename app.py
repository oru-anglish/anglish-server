from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")

pos_kor = {
    "PRON": "대명사", "NOUN": "명사", "VERB": "동사", "ADJ": "형용사",
    "ADV": "부사", "DET": "관사", "AUX": "조동사", "INTJ": "감탄사",
    "SCONJ": "접속사", "ADP": "전치사", "PROPN": "고유명사", "PART": "부정사"
}

dep_kor = {
    "nsubj": "주어", "ROOT": "동사", "attr": "보어", "dobj": "목적어",
    "prep": "전치사구", "advmod": "부사어", "amod": "형용어", "det": "관형어",
    "compound": "형용어", "pobj": "전치사 목적어", "cc": "접속사", "conj": "병치",
    "mark": "접속사", "advcl": "부사절", "xcomp": "보어", "aux": "조동사"
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
        if token.pos_ in ["PUNCT", "SPACE"]:
            continue
        result.append({
            "text": token.text,
            "pos": pos_kor.get(token.pos_, token.pos_),
            "dep": dep_kor.get(token.dep_, token.dep_)
        })

    try:
        translated = GoogleTranslator(source='auto', target='ko').translate(sentence)
    except Exception:
        translated = "(번역 실패)"

    return jsonify({"tokens": result, "translation": translated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
