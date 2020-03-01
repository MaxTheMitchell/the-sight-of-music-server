import spotify,image_analysis,json,pygame
# print(
#     image_analysis.ImageAnalyser(
#         spotify.Search().get_album("Untrue").get_cover64()
#     ).get_pixle_colors()
# )
image = image_analysis.ImageAnalyser(spotify.Search().get_album("Over the Sea").get_cover64())
pixle_size = 10
width = image._get_width()
height = image._get_height()
window = pygame.display.set_mode((width*pixle_size, height*pixle_size))


def translate_to_pygame():
        for i,pixle in enumerate(image.get_pixle_colors()):
            pygame.draw.rect(
                window,
                pixle,
                pygame.Rect(
                    pixle_size*((i)%width),
                    pixle_size*int(i/width)
                    ,pixle_size,
                    pixle_size)
                )
        pygame.display.update()

while True:
    translate_to_pygame()

