# -*- coding: utf-8 -*-
from random import randint, choice
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw
from django.http import HttpResponse, Http404

snippets = (
    ("%s << %s", lambda x, y: x << y, lambda: randint(0, 100), lambda: randint(0, 5)),
    ("%s >> %s", lambda x, y: x >> y, lambda: randint(0, 256), lambda: randint(0, 8)),
    ("%s / %s", lambda x, y: x / y,
     lambda: randint(-1000, 1000), lambda: choice((randint(-1000, -1), randint(1, 1000)))),
    ("%s + %s", lambda x, y: x + y, lambda: randint(-1000, 1000), lambda: randint(-1000, 1000)),
    ("%s - %s", lambda x, y: x - y, lambda: randint(-1000, 1000), lambda: randint(-1000, 1000)),
    ("%s * %s", lambda x, y: x * y, lambda: randint(-100, 100), lambda: randint(-100, 100))
)

MAX_WIDTH = 300
MAX_HEIGHT = 300

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 25
DEFAULT_FONT_SIZE = 11
DEFAULT_CAPTURE_ID = 'capture'
DEFAULT_BACKGROUND = '#fff'
DEFAULT_FOREGROUND = '#000'


def generate_capture(request):
    """
    You can visit the view with GET params like k, b, f to custom the capture.
    b indicates background color, and f foreground color.
    The value of color should be an integer, which will be convert to a hex color value. That is to say the value
     of a color should not be less than 0 or larger than 16777215.
    k indicates the key of the capture. It should exist in session before this view is visited, otherwise A 404 error
    will be throw out.
    And once the view is visited, the answer of the capture will be set a key in session which k indicates.
    """
    keyName, bcolor, fcolor = DEFAULT_CAPTURE_ID, DEFAULT_BACKGROUND, DEFAULT_FOREGROUND
    if 'k' in request.GET:
        if request.GET['k'] in request.session:
            keyName = request.GET['k']
        else:
            raise Http404()
    try:
        if 'b' in request.GET:
            bcolor = '#{:0>6.6s}'.format('%x' % max(min(int(request.GET['b']), 16777215), 0))
        if 'f' in request.GET:
            fcolor = '#{:0>6.6s}'.format('%x' % max(min(int(request.GET['f']), 16777215), 0))
    except:
        raise Http404()
    ver_fun = snippets[randint(0, len(snippets) - 1)]
    x, y = ver_fun[2](), ver_fun[3]()
    request.session[keyName] = '%r' % ver_fun[1](x, y)
    img = Image.new("RGB", (DEFAULT_WIDTH, DEFAULT_HEIGHT), bcolor)
    draw = Draw(img)
    font = ImageFont.truetype('font/SourceCodePro-Regular.ttf', DEFAULT_FONT_SIZE)
    for i in xrange(0, 3):
        draw.line([(0, randint(0, DEFAULT_HEIGHT)), (DEFAULT_WIDTH, randint(1, DEFAULT_HEIGHT))],
                  fill='#{:0>6.6s}'.format('%x' % randint(0, 16777215)))
    if x < 0:
        x = '(%s)' % x
    if y < 0:
        y = '(%s)' % y
    text = ver_fun[0] % (x, y)
    x, y = font.getsize(text)
    draw.text((DEFAULT_WIDTH / 2 - x / 2, DEFAULT_HEIGHT / 2 - y / 2), text, font=font, fill=fcolor)
    response = HttpResponse(mimetype='image/png')
    img.save(response, 'PNG')
    return response
