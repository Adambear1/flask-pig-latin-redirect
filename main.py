import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return facts[0].getText()

def piglantize(fact):
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data={"input_text": fact}, allow_redirects=False)
    response_url = response.headers["Location"]
    body = f"<div>Your fact:<br><span><b>{fact}</b></span><br><br><span>Please click link below to read fact in piglatin:</span><br><a href={response_url} target='_blank'>{response_url}</a></div>"
    return body

@app.route('/')
def home():
    fact = get_fact()
    return piglantize(fact).encode()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

