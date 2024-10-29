from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import pandas as pd

from function import fit_text_to_width
# サンプルではプライベート情報が入っているため別ファイルに保存
from privateInformation import group_name, group_address, group_website_link, group_address_number


def draw_business_card(c, row_data, bg_image, canvas_width, canvas_height):
    # 背景画像を描く。
    c.drawImage(bg_image, 0, 0, canvas_width, canvas_height)

    # テキストの色を設定
    c.setFillColor(colors.black)

    # あとは、情報を配置していく。気合い。
    # 左下が原点で、文字の配置も左端を基準にしている。フォントとそのサイズ -> 文章作成の繰り返し
    # データは、csvの列名で指定。

    # 幅だけを指定して一文で文字を入れる場合は　fit_text_to_width() を利用する。
    # fit_text_to_width_height(canvas, 文章, x, y, 長方形の幅, 長方形の高さ, font_name, max_font_size)を利用すれば、
    # ある長方形の中に文章を適切に入れてくれる。
    # 長方形の大きさは c.rect(x, y, 長方形の幅, 長方形の高さ)で確認できる。

    c.setFont("ipaexm", 5)
    c.drawString(145, 120, group_name)
    c.drawString(145, 114, row_data['役職'])
    c.drawString(145, 108, row_data['大学'])

    # c.rect(160, 75, 80, 20)
    fit_text_to_width(c, row_data['名前'], 160, 75, 80, "ipaexm", 15)
    # c.rect(200, 65, 50, 5)
    fit_text_to_width(c, row_data['ふりがな'], 200, 65, 50, "ipaexm", 5)

    c.setFont("ipaexm", 4.5)
    c.drawString(145, 42, group_address_number)
    c.drawString(145, 35, group_address)
    c.drawString(155, 26.5, row_data['電話番号'])
    # c.rect(155, 20, 75, 5)
    fit_text_to_width(c, row_data['メアド'], 155, 20, 75, "ipaexm", 4.5)
    c.setFont("ipaexm", 4.5)
    c.drawString(155, 13.5, group_website_link)


def generate_business_card(output_dir, data, bg_image_path):
    # サイズの指定
    width, height = (91 * mm, 55 * mm)
    # フォント読み込み
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))
    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)

    for i, row in data.iterrows():
        c = canvas.Canvas(f'{output_dir}/business_card_{i+1}.pdf', pagesize=(width, height))
        draw_business_card(c, row, bg_image, width, height)
        c.save()


data = pd.read_csv('./csv/business_card.csv')
generate_business_card("BusinessCards", data, "./png/business_card.png")
