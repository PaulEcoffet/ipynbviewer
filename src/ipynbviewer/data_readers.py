import base64
import io
import timg
from timg.methods import Ansi24HblockMethod
from markdownify import markdownify as md
from typing import Union
import re
import pygments
from pygments.lexers import PythonLexer, MarkdownLexer
from pygments.formatters import TerminalFormatter


class IncompatibleDataReaderException(Exception):
    pass


def png_data_reader(data: Union[str, bytes]):
    """
    Takes a base64 png and outputs it in an ansi-terminal text with a max width of 70
    :param data:
    :return: a human readable string of the image (ansi terminal coded)
    """
    try:
        imgdata = "".join(data)
    except ValueError:
        imgdata = data
    decode = base64.b64decode(imgdata)
    imgfile = io.BytesIO(decode)
    renderer = timg.Renderer()
    renderer.load_image_from_file(imgfile)
    if renderer.image.width >= 70:
        renderer.resize(w=70)
    output = Ansi24HblockMethod(renderer.image).to_string()
    return output


def text_data_reader(data: Union[str, bytes, list]):
    """
    Returns the text data in a human readable string

    :param data: the string
    :return: a human readable string
    """
    try:
        return "".join(data)
    except ValueError:
        return data


def _img_match_to_timg(match: re.Match, lbound="", rbound=""):
    return lbound + png_data_reader(match.group(1)) + rbound


def html_data_reader(data: Union[str, bytes, list]):
    try:
        htmldata = "".join(data)
    except ValueError:
        htmldata = data

    # mardownify do not support table yet (will come soon)
    if "<table" in htmldata:
        raise IncompatibleDataReaderException()

    # transform to markdown
    mdoutput = md(htmldata)

    # split base64 encoded image and capture them
    mdoutputlist = re.split(r"(!\[]\(data:image/png;base64,.*?\))", mdoutput)

    alloutputs = []
    for curout in mdoutputlist:
        capture = re.match(r"!\[]\(data:image/png;base64,(.*?)\)", curout)
        if capture:  # if image
            alloutputs.append(_img_match_to_timg(capture))
        else:  # else parse markdown
            alloutputs.append(pygments.highlight(curout, PythonLexer(), TerminalFormatter()))
    return "\n".join(alloutputs)



data_readers = {
    "image/png": png_data_reader,
    "text/html": html_data_reader,
    "text/plain": text_data_reader
}