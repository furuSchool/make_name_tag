from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd

from function import fit_text_to_width, fit_text_to_width_height_2


def generate_name_plate(output_pdf, data):
    # キャンバスを作成
    c = canvas.Canvas(output_pdf, pagesize=A4)
    # フォントを読み込む
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))

    # 点線を書く
    width, height = A4
    # ネームプレートを作成
    for _, row in data.iterrows():
        c.setDash(3, 2)
        c.line(0, (height-100)/3, width, (height-100)/3)
        c.line(0, (height-100)/3*2, width, (height-100)/3*2)
        c.line(0, height-100, width, height-100)
        title = row['title']
        name = row['name']
        furigana = row['furigana']

        # テキストの色を設定
        c.setFillColor(colors.black)

        # ネームプレート作成
        fit_text_to_width_height_2(c, title, 50, (height-100)/3 + 160, width-100, 60, "ipaexm", 14)
        fit_text_to_width(c, name, 100, (height-100)/3 + 40, width-200, "ipaexm", 100)
        fit_text_to_width(c, furigana, 120, (height-100)/3 + 110, width-280, "ipaexm", 30)

        # 点対称に文章を書く
        c.saveState()
        c.translate(width, (height-100)/3*4)
        c.rotate(180)
        fit_text_to_width_height_2(c, title, 50, (height-100)/3 + 160, width-100, 60, "ipaexm", 14)
        fit_text_to_width(c, name, 100, (height-100)/3 + 40, width-200, "ipaexm", 100)
        fit_text_to_width(c, furigana, 120, (height-100)/3 + 110, width-280, "ipaexm", 30)
        c.restoreState()

        c.showPage()

    # PDFを保存
    c.save()

data = pd.read_csv('name_plate.csv',header=None)
data.columns = ['title', 'name', 'furigana']
generate_name_plate("name_plate.pdf", data)