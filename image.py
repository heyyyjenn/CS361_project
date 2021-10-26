import json
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask
import requests

app = Flask(__name__)
api = Api(app)
CORS(app)


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

        return lst_images


# how to call the API
api.add_resource(Images, "/<query>,<int:width>,<int:height>")

if __name__ == '__main__':
    app.run()
