import spotify
import time
import functools

import spotify,image_analysis

with open("album_colors.txt","w") as txt:
    txt.write(
        functools.reduce(lambda total,color :total+str(color),
            image_analysis.ImageAnalyser(
                spotify.CurrentlyPlaying().get_album().get_cover64()
            ).get_adverage_colors(16),
        "").replace('(',',CHSV(')
    )
    
