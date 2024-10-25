import re
import base64
import zlib
from urllib.parse import unquote
from bs4 import BeautifulSoup


def is_base64(s):
    return len(s) % 4 == 0 and re.match('^[A-Za-z0-9+/]*={0,2}$', s)


class DecodeAndDecompress:

    @staticmethod
    def convert(drawio_filepath):
        """
        References:
          https://drawio-app.com/extracting-the-xml-from-mxfiles/
          https://github.com/pzl/drawio-read/blob/master/read.py

        Convert the DrawIO file to raw XML

        Paramters:
          drawio_filepath: file path to the .drawio file

        Returns:
          decoded_xml: decode and decompressed xml
        """

        try:
            with open(drawio_filepath, "r") as f:
                content = "".join(f.readlines())

            drawio_file_raw = BeautifulSoup(content, "lxml")
            diagram_tag = drawio_file_raw.find("diagram")
            diagram_tag_text = diagram_tag.text

            if is_base64(diagram_tag_text):
                diagram_tag_text = base64.b64decode(diagram_tag_text)
                decoded_xml = unquote(zlib.decompress(diagram_tag_text, -15).decode('utf8'))
            else:
                diagram_tag_text = str(diagram_tag)
                start = diagram_tag_text.find(">") + 1
                end = diagram_tag_text.rfind("<")
                decoded_xml = diagram_tag_text[start:end].strip().replace("\n", "")

            return decoded_xml

        except Exception as e:
            print(f"DecodeAndDecompress.convert ERROR: {e}")
            return False
