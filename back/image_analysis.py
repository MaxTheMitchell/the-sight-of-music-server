from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_html_askii_display(self,resolution):
        html = '<table align="center">'
        img = self._alter_resolution(int(resolution))
        for x in range(int(resolution)):
            html += "<tr>"
            for y in range(int(resolution)):
                html += '<td style="color:rgb{}" size="1">@</td>'.format(self._get_pixle(img,x,y))
            html += "</tr>"
        return bytes(html + "</table>",'utf-8')

    def get_adverage_color(self):
        return self.get_adverage_colors(1)

    def get_pixles(self,amount=64):
        return self._get_pixle_colors(self._alter_resolution(amount))

    def _alter_resolution(self,resolution):
        self.image.draft("RGB",(resolution,resolution))
        return self.image

    def _get_pixle_colors(self,image):
        return list(self.image.getdata())

    def _get_pixle(self,image,x,y):
        return self.image.load()[y,x]

    def _get_height(self,image):
        return image.height
    
    def _get_width(self,image):
        return image.width
    
    def _pixle_numb(self):
        return self._get_width()*self._get_height()