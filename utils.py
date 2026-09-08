import colorsys

def generateRainbow(size):
    res = []
    for i in range(size):
        r, g, b = colorsys.hls_to_rgb(i / size, 0.4, 0.65)
        res.append((int(r * 255), int(g * 255), int(b * 255)))
    return res