from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd

from function import fit_text_to_width_height, fit_text_to_width_height_ver2


def draw_introduce_card(c, row_data, bg_image, canvas_width, canvas_height):
    # 背景画像を描く。
    c.drawImage(bg_image, 0, 0, canvas_width, canvas_height)

    # テキストの色を設定
    c.setFillColor(colors.black)

    # あとは、情報を配置していく。気合い。
    # 左下が原点で、文字の配置も左端を基準にしている。フォントとそのサイズ -> 文章作成の繰り返し
    c.setFont("ipaexm", 30)
    c.drawString(1175, 1000, 'チーム')
    c.setFont("ipaexm", 40)
    c.drawString(150, 200, '出身地')
    c.setFont("ipaexm", 45)
    c.drawString(720, 790, '興味のある分野')
    c.drawString(1200, 790, '趣味・特技')
    c.setFont("ipaexm", 43)
    c.drawString(1500, 790, 'サークル・バイト')
    c.setFont("ipaexm", 45)
    c.drawString(800, 410, '将来やりたいこと')
    c.drawString(1500, 410, '意気込み')

    # 次は、個人で固有の情報を入れていく。
    # 幅だけを指定して一文で文字を入れる場合は　fit_text_to_width_height() を利用する。
    # fit_text_to_width_height_ver2(canvas, 文章, x, y, 長方形の幅, 長方形の高さ, font_name, max_font_size)を利用すれば、
    # ある長方形の中に文章を適切に入れてくれる。
    # 長方形の大きさは c.rect(x, y, 長方形の幅, 長方形の高さ)で確認できる。
    # データは、csvの列名で指定。

    # c.rect(1190,910,80,80) # 確認用
    fit_text_to_width_height_ver2(c, row_data['学部'], 100, 330, 300, 100,
                                  "ipaexm", 80)
    fit_text_to_width_height_ver2(c, row_data['出身地'], 150, 80, 350, 100,
                                  "ipaexm", 80)
    fit_text_to_width_height_ver2(c, row_data['名前'], 670, 900, 430, 100,
                                  "ipaexm", 100)
    fit_text_to_width_height(c, row_data['ふりがな'], 700, 1000, 370, "ipaexm", 50)
    fit_text_to_width_height(c, row_data['所属チーム'], 1190, 910, 80, "ipaexm",
                             100)
    fit_text_to_width_height_ver2(c, row_data['趣味または特技'], 1190, 510, 240, 240,
                                  "ipaexm", 100)
    fit_text_to_width_height_ver2(c, row_data['興味のある分野'], 720, 510, 350, 240,
                                  "ipaexm", 80)
    fit_text_to_width_height_ver2(c, row_data['サークル'], 1550, 510, 240, 240,
                                  "ipaexm", 80)
    fit_text_to_width_height_ver2(c, row_data['やりたいこと'], 720, 100, 500, 240,
                                  "ipaexm", 80)
    fit_text_to_width_height_ver2(c, row_data['意気込み'], 1420, 100, 350, 240,
                                  "ipaexm", 80)


def generate_self_introduction_cards(output_pdf, data, bg_image_path):
    # サイズの指定
    width, height = (1920, 1080)
    c = canvas.Canvas(output_pdf, pagesize=(1920, 1080))
    # フォント読み込み
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))
    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)

    for i, row in data.iterrows():
        draw_introduce_card(c, row, bg_image, width, height)
        c.showPage()

    # PDFを保存
    c.save()


data = pd.read_csv('introduce_data.csv')
generate_self_introduction_cards("introduce.pdf", data, "introduce.png")
