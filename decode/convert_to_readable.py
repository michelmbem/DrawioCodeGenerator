import re

from base64 import b64decode
from zlib import decompress
from urllib.parse import unquote
from bs4 import BeautifulSoup as bs


class DecodeAndDecompress:

    @staticmethod
    def convert(drawio_filepath):
        """
        References:
          https://drawio-app.com/extracting-the-xml-from-mxfiles/
          https://github.com/pzl/drawio-read/blob/master/read.py

        Convert the DrawIO file to raw XML

        Parameters:
          drawio_filepath: file path to the .drawio file

        Returns:
          decoded_xml: decoded and decompressed xml
        """

        try:
            with open(drawio_filepath, "r") as f:
                drawio_document = bs(f.read(), "lxml")

            diagram_tag = drawio_document.find("diagram")
            diagram_tag_text = DecodeAndDecompress.get_tag_text(diagram_tag)

            if DecodeAndDecompress.is_base64(diagram_tag_text):
                decoded_xml = unquote(decompress(b64decode(diagram_tag_text), -15).decode('utf8'))
            else:
                decoded_xml = diagram_tag_text.replace("\n", "")

            return decoded_xml

        except Exception as e:
            print(f"DecodeAndDecompress.convert ERROR: {e}")
            return False

    @staticmethod
    def is_base64(s):
        return len(s) % 4 == 0 and re.match('^[A-Za-z0-9+/]*={0,2}$', s)

    @staticmethod
    def get_tag_text(tag):
        tag_text = str(tag)
        start = tag_text.find(">") + 1
        end = tag_text.rfind("<")
        return tag_text[start:end].strip()
