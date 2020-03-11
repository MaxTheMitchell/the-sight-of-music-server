from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_adverage_colors(self,colors_amount):
        colors = []
        pixles = self.get_pixle_colors()
        for i in range(0,self._pixle_numb(),colors_amount**2):
            colors.append(self.get_adverage_color(pixles[i:(i+colors_amount**2)]))
        return colors
        
    def get_adverage_color(self,colors = None):
        if colors == None:
            colors = self.get_pixle_colors()
        rgb = [0]*3
        for r,g,b in colors:
            rgb[0]+=r
            rgb[1]+=g
            rgb[2]+=b
        return tuple(map(lambda color:color//len(colors),rgb))

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