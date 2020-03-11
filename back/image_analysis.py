from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_adverage_color(self):
        rgb = [0]*3
        for r,g,b in self.get_pixle_colors():
            rgb[0]+=r
            rgb[1]+=g
            rgb[2]+=b
        return tuple(map(lambda color:int(color/self._pixle_numb()),rgb))

    def get_pixle_colors(self):
        pixles = []
        for x in range(self._get_width()):
            for y in range(self._get_height()):
                pixles.append(self.get_pixle(x,y))
        return pixles

    def get_pixle(self,x,y):
        return self.image.load()[y,x]

    def _get_height(self):
        return self.image.height
    
    def _get_width(self):
        return self.image.width
    
    def _pixle_numb(self):
        return self._get_width()*self._get_height()