import json
from bs4 import BeautifulSoup
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask import Flask, send_file
import requests
import io
from PIL import Image

app = Flask(__name__)
api = Api(app)
CORS(app)

class Home(Resource):
    def get(self):
        return "To use this image microservice, send a GET request to " \
               "'https://www.lamjenni-image.herokuapp.com/query,width,height' where query is the image string " \
               "keyword and width/height are integers"

class Images(Resource):
    def get(self, query, width, height):

        # using Bing to scrape images
        bing_url = "http://www.bing.com/images/search?q="
        user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.81 Safari/537.36'
        }
        query_url = bing_url + query + "&FORM=HDRSC2"
        response = requests.get(query_url, headers=user_agent)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # some urls didn't work so this list will keep at least 3
        lst_images = []
        try:
            # sometimes Bing uses this HTML structure for images, tag "m" with "murl" attribute
            images = soup.findAll("a", {"class": "iusc"})
            for image in images:
                m = json.loads(image["m"])
                murl = m["murl"]
                lst_images.append(murl)
                if len(lst_images) == 3:
                    break
        except KeyError:
            # other times Bing uses this HTML structure instead, tag "img" with "src" attribute
            images = soup.findAll("img", {"alt": f"Image result for {query}".format(query)})
            for image in images:
                src = image["src"]
                lst_images.append(src)
                if len(lst_images) == 3:
                    break

        # if one url doesn't work then go through the other ones
        for url in lst_images:
            try:
                # resize image without having to save it
                response = requests.get(url)
                image = io.BytesIO()
                image.write(response.content)
                image.seek(0)
                resized_image = Image.open(image)
                resized_image = resized_image.resize((width, height))
                image.seek(0)
                resized_image.save(image, 'png')
                image.seek(0)
                return send_file(image, mimetype='image/png')
            except:
                continue


# how to call the API
api.add_resource(Images, "/<query>,<int:width>,<int:height>")
api.add_resource(Home, "/")

if __name__ == '__main__':
    app.run()
