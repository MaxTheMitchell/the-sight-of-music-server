from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_color_composition(self):
        return self.image.load()[0,0]

    def get_pixle_colors(self):
        pixles = []
        for x in range(self._get_width()):
            for y in range(self._get_height()):
                pixles.append(self.get_pixle(x,y))
        return pixles

    def get_pixle(self,x,y):
        return self.image.load()[x,y]

    def _get_height(self):
        return self.image.height
    
    def _get_width(self):
        return self.image.width