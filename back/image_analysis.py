from PIL import Image
import requests

class ImageAnalyser:

    def __init__(self,url):
        self.image = Image.open(requests.get(url, stream=True).raw)

    def get_html_askii_display(self,resolution):
        html = '<table align="center">'
        img = self._alter_resolution(self.image,int(resolution))
        for x in range(int(resolution)):
            html += "<tr>"
            for y in range(int(resolution)):
                html += '<td style="color:rgb{}" size="1">@</td>'.format(self._get_pixle(img,x,y))
            html += "</tr>"
        return bytes(html + "</table>",'utf-8')

    def get_adverage_color(self):
        return self.get_adverage_colors(1)

    def get_half_reversed_subsection_of_pixles(self,amount,start,end):
        return self.get_half_reversed_pixles(amount)[start:end]

    def get_subsection_of_pixles(self,amount,start,end,format565 = False):
        pixels = self.get_pixles(amount)[start:end]
        if format565:
            return self._format_to_565(pixels)
        return pixels

    def get_half_reversed_pixles(self,side_length):
        pixles = self.get_pixles(side_length)
        for i in range(side_length):
            if i%2 == 0:
                pixles[i*side_length:(i+1)*side_length] = list(reversed(pixles[i*side_length:(i+1)*side_length]))
        return pixles

    def get_pixles(self,side_length=64):
        return self._reduce_size(
            self._check_for_monotone(
                self._get_pixle_colors(
                    self._alter_resolution(self.image,side_length)
                    )
                ),
                side_length**2
            )
    def _format_to_565(self,pixels):
        return [(((rgb[0] & 0b11111000)<<8) + ((rgb[2] & 0b11111100)<<3) + (rgb[1]>>3)) for rgb in pixels]

    def _reduce_size(self,pixels,expected_size):
        i = 0
        while len(pixels) > expected_size:
            pixels[i] = tuple(int(sum(colors)/2) for colors in zip(pixels[i],pixels[i+1]))
            pixels.pop(i+1)
            i += 1
            if i >= len(pixels)-1:
                i=0
        return pixels

    def _check_for_monotone(self,pixels):
        if isinstance(pixels[0],int):
            return [(pix,pix,pix) for pix in pixels]
        return pixels
    
    def get_pixle(self,resolution,pixle):
        img = self._alter_resolution(self.image,resolution)
        return self._get_pixle(
            img,
            pixle%self._get_width(img),
            int(pixle/self._get_height(img))
            )

    def _alter_resolution(self,image,resolution):
        return image.resize((resolution,resolution))

    def _get_pixle_colors(self,image):
        return list(image.getdata())

    def _get_pixle(self,image,x,y):
        return image.load()[y,x]

    def _get_height(self,image):
        return image.height
    
    def _get_width(self,image):
        return image.width
    
    def _pixle_numb(self):
        return self._get_width()*self._get_height()