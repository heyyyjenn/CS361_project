import json
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask, send_file
import requests
import io
from PIL import Image

app = Flask(__name__)
api = Api(app)
CORS(app)

class Home(Resource):
    def get_home(self):
        """
        A GET method that serves as the homepage to the image microservice which has some detail on how to use the
        microservice
        """
        return "To use this image microservice, send a GET request to " \
               "'https://www.lamjenni-image.herokuapp.com/query,width,height' where query is the image string " \
               "keyword and width/height are integers"

class Images(Resource):
    def scrape_image(self, query, width, height):
        """
        A GET method that serves as an image scraper and resizer. It calls the methods get_three_images() and
        resize_image() to return an image of the specified keyword of the specified width and height of the user
        """
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

        lst_images = self.get_three_images(soup, query)
        return self.resize_image(lst_images, width, height)

    def get_three_images(self, images, query):
        """
        A method called by get_image() which takes the parsed HTML from a Bing scraper and keeps a list of three images.
        This is because some URLs didn't work so we keep at least 3 to use in case 1 doesn't work.
        """

        lst_images = []
        try:
            # sometimes Bing uses this HTML structure for images, tag "m" with "murl" attribute
            images = images.findAll("a", {"class": "iusc"})
            for image in images:
                m = json.loads(image["m"])
                murl = m["murl"]
                lst_images.append(murl)
                if len(lst_images) == 3:
                    break
        except KeyError:
            # other times Bing uses this HTML structure instead, tag "img" with "src" attribute
            images = images.findAll("img", {"alt": f"Image result for {query}".format(query)})
            for image in images:
                src = image["src"]
                lst_images.append(src)
                if len(lst_images) == 3:
                    break

        return lst_images

    def resize_image(self, lst_images, width, height):
        """
        A method called by scrape_image() to resize and return an image to the specified width and height
        """

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
