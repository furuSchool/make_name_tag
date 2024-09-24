from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd
import os
from pdf2image import convert_from_path
from makePDFCard import draw_introduce_card

# poppler というツールが必要みたいです。mac なら brew install でできます。windowsなら、調べてダウンロード。

# Poppler path (Windowsのみで必要。macOS/Linuxでは不要)
# poppler_path = r'C:\path\to\poppler\bin'

# 結構時間がかかります。
def generate_self_introduction_cards_pmg(output_folder_path, data, bg_image_path):
    # サイズの指定
    width, height = (1920, 1080)
    # フォント読み込み
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))
    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)

    for i, row in data.iterrows():
        # Create a PDF for each card
        pdf_path = f"{output_folder_path}/introduce_{i+1}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=(1920, 1080))
        draw_introduce_card(c, row, bg_image, width, height)
        c.save()

        # Convert the PDF to an image
        images = convert_from_path(pdf_path)
        # images = convert_from_path(pdf_path, poppler_path=poppler_path if os.name == 'nt' else None) # windowsなら必要
        
        # Save the first page of the PDF as a PNG image
        if images:
            images[0].save(f"{output_folder_path}/introduce_{i+1}.png", "PNG")
        # Delete the PDF file after conversion
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


data = pd.read_csv('introduce_data.csv')
generate_self_introduction_cards_pmg("PngCards", data, "introduce.png")
