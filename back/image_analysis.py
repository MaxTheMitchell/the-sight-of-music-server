from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_html_askii_display(self,resolution):
        html = '<table align="center">'
        img = self.alter_resolution(int(resolution))
        for x in range(int(resolution)):
            html += "<tr>"
            for y in range(int(resolution)):
                html += '<td style="color:rgb{}" size="1">@</td>'.format(self._get_pixle(img,x,y))
            html += "</tr>"
        return bytes(html + "</table>",'utf-8')

    def get_adverage_color(self):
        return self.get_adverage_colors(1)

    def get_adverage_colors(self,resolution):
        return self._get_pixle_colors(self.alter_resolution(resolution))

    def alter_resolution(self,resolution):
        return self.image.resize((resolution,resolution))

    def get_pixles(self):
        return self._get_pixle_colors(self.image)

    def _get_pixle_colors(self,image):
        pixles = []
        for x in range(self._get_width(image)):
            for y in range(self._get_height(image)):
                pixles.append(self._get_pixle(image,x,y))
        return pixles

    def _get_pixle(self,image,x,y):
        return self.image.load()[y,x]

    def _get_height(self,image):
        return image.height
    
    def _get_width(self,image):
        return image.width
    
    def _pixle_numb(self):
        return self._get_width()*self._get_height()