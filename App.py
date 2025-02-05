from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_direct_link(terabox_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(terabox_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        direct_link = soup.find('a', {'id': 'download_button_id'})['href']
        return direct_link
    else:
        return None

@app.route('/get_link', methods=['POST'])
def get_link():
    data = request.get_json()
    url = data.get('url')
    
    if url:
        direct_link = get_direct_link(url)
        if direct_link:
            return jsonify({"direct_link": direct_link}), 200
        else:
            return jsonify({"error": "Unable to fetch direct link"}), 500
    else:
        return jsonify({"error": "No URL provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
