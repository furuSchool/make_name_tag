from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd

from function import fit_vertical_text_to_width_height, fit_text_to_height


def generate_name_curtain(output_pdf, data, bg_image_path):
    # キャンバスを作成
    c = canvas.Canvas(output_pdf, pagesize=A4)
    # フォントを読み込む
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))
    # 点線を書く
    width, height = A4
    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)

    # ネームプレートを作成
    for _, row in data.iterrows():
        title = row['title']
        name = row['name']
        furigana = row['furigana']

        # テキストの色を設定
        c.setFillColor(colors.black)
        c.drawImage(bg_image, 0, 0, width=width, height=height)

        # ネームプレート作成
        # c.rect(width-170, 100, 120, height-200) # 長方形確認
        fit_vertical_text_to_width_height(c, title, width-170, 100, 120, height-200, "ipaexm", 80)
        font_size = fit_text_to_height(c, name, 230, 100, height-200, "ipaexm", 100)
        fit_text_to_height(c, furigana, 230 + font_size + 10, 200, height-350, "ipaexm", 50)

        c.showPage()

    # PDFを保存
    c.save()

data = pd.read_csv('name_curtain.csv',header=None)
data.columns = ['title', 'name', 'furigana']
generate_name_curtain("name_curtain.pdf", data, 'name_curtain.png')