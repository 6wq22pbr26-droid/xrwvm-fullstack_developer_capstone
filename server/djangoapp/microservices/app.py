import os
from pathlib import Path
import nltk
from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.path.insert(0,str(Path(__file__).parent))
app=Flask(__name__)
sia=SentimentIntensityAnalyzer()
@app.get('/')
@app.get('/health')
def health():return jsonify(status='OK',service='VADER sentiment')
@app.get('/analyze/<path:input_txt>')
def analyze(input_txt):
    scores=sia.polarity_scores(input_txt)
    compound=scores['compound']
    return jsonify(sentiment='positive' if compound>=0.05 else 'negative' if compound<=-0.05 else 'neutral',scores=scores)
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.getenv('PORT','5050')))
