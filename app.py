#Import library
from flask import Flask, render_template, request
import requests
import qrcode

# get API key and google search engine id
# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "AIzaSyBO46vbX34nyUcqAf_TfRJ2vx-ZpqlyD0I"
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "016940891277536788034:lj9t9m_cwti"


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def search_request():
    if request.method =="POST":
        query = request.form["input"]
        items = search(query)
        img = toqr(items)
        img.save('static/QR.png')
    return render_template('results.html', items=items)

#Convert link to QRcode function
def toqr(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=15,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

#Search from google engine function
def search(query):

    start =  1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data = requests.get(url).json()
    search_items = data.get("items")

    for i, search_item in enumerate(search_items, start=1):
        link = search_item.get("link")
        print("URL:", link, "\n")
    return link



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)