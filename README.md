# ネームタグ作成
`generate_business_cards(output_pdf, data, bg_image_path)`

csv形式のデータから、ネームタグを作る。A4サイズで8枚できる。

`python makeNameTag.py`で実行できる

- `name_tag.csv` がデータで、「役職, 名前, ふりがな」
- `name_tag.png` が、ネームタグの背景
- 役職は、`fit_text_to_width_height_2()`を利用
- あまりにも長すぎる名前は対応不可能
- ネームタグに合わせて、`draw_business_card()`のコードを変更する
- A4 の８分割より小さいサイズに対応している
- 苗字と名前はあらかじめスペースを空けておくこと推奨
- あらかじめ、「様」「先生」などは入れておく必要あり。

# ネームプレート作成
`generate_name_plate(output_pdf, data)`

csv形式のデータから、A4サイズのネームプレートを作る。

`python makeNamePlate.py`で実行できる

- `name_plate.csv` がデータで、「役職, 名前, ふりがな」
- 役職は、`fit_text_to_width_height_2()`を利用
- あまりにも長すぎる名前は対応不可能
- 苗字と名前はあらかじめスペースを空けておくこと推奨
- あらかじめ、「様」「先生」などは入れておく必要あり

# ネーム幕作成
`generate_name_curtain(output_pdf, data, bg_image_path)`

csv形式データから、A4サイズのネーム幕を作る。

`python makeNameCurtain.py`で実行できる

- `name_curtain.csv` がデータで、「役職, 名前, ふりがな」
- `name_curtain.png` が、ネーム幕の背景
- 役職は、`fit_text_to_width_height_2()`を利用
- あまりにも長すぎる名前は対応不可能
- 苗字と名前はあらかじめスペースを空けておくこと推奨
- あらかじめ、「様」「先生」などは入れておく必要あり
- 無理やり縦書きにしているため、アルファベットや句読点、「ー」などは違和感あり

# 自己紹介カード作成
`generate_self_introduction_cards(output_pdf, data, bg_image_path)`

csv形式のデータから、自己紹介カードを作る。1人あたり1ページを想定。

`python makePDFCard.py`で実行できる

- `introduce_data.csv` がデータで、デフォルトは、名前,ふりがな,所属チーム,出身地,学部,趣味または特技,興味のある分野,サークル,やりたいこと,意気込み, がカラム名になっている
- `introduce.png`が自己紹介カードの背景
- 自己紹介の内容に合わせて、`draw_introduce_card()`のコードを変更する

`generate_self_introduction_cards_pmg(output_folder_path, data, bg_image_path)`

- pdfファイルではなくpngファイルで出力するためのもの
- `PngCards`というフォルダの中にpngを作成
- 結構時間がかかる
- poppler というツールが必要。mac なら `brew install poppler` でできる。windowsなら、調べてダウンロード
- I LOVE PDF などを使って、pdfデータをpngデータにするのが吉かも

# 名刺作成
`generate_business_card(output_dir, data, bg_image_path)`

csv形式のデータから、名刺を作る。

`python makeBusinessCard.py`で実行できる

- `business_card.csv` がデータで、デフォルトは、役職, 大学, 名前, ふりがな, 電話番号, メアド, 
がカラム名になっている
- `business_card.png` が、名刺の背景
- あまりにも長すぎる名前は対応不可能
- 苗字と名前はあらかじめスペースを空けておくこと推奨
- 1点ネームタグと異なる点として、名刺ごとに別々のPDFとして `output_dir` というフォルダ内に格納する様にしてある。
そのため、あらかじめフォルダを作っておく必要がある。
- デフォルトでは、機密情報を github 上に上げない様に、別ファイルに機密情報を書いている。

# その他関数
`fit_text_to_width(c, text, x, y, max_width, font_name, max_font_size, alignment='left')`

ある幅に合うように文字サイズを変更してくれる関数。ただし、1文限定である。
そのため、幅に対して文字数が長すぎると、とんでもなく文字サイズが小さくなる場合がある。

また、任意で `alignment`に 'center' か 'right' を設定することで、
中央揃え、右揃えができる。

`fit_text_to_width_height(c, text, x, y, max_width, max_height, font_name, max_font_size, alignment='left')`

ある長方形の中に文章を適切に入れてくれる。
- 左揃え、中揃えである
- 文字サイズの最大値以下で、長方形に収まってかつ文字サイズが最も大きくなるように文章を配置する。
- 句読点の位置や文字の切れ目は考慮しない。必要ならデータ時点で改行などをする必要がある。
- 長方形の大きさは `c.rect(x, y, 長方形の幅, 長方形の高さ)` で確認すれば良い。
- `alignment`に 'center' を設定することで、中央揃えができる。

`fit_text_to_width_height_2(c, text, x, y, max_width, max_height, font_name, max_font_size, alignment='left')`
- 基本的には上記と同じだが、少しだけ挙動が違う。
- より求めている挙動をする方を使う。
- `alignment`に 'center' を設定することで、中央揃えができる。

`ttc_to_ttf(ttc_file_path, output_dir)`
- `ttc_file_path` にある .ttc ファイルを分割して、
`output_dir` 内に .ttf ファイルを作成する関数
- 様々な日本語フォントを使いたい時などに利用する

`make_face_img(image_path, output_path, size, shape, padding)`
- 画像から顔の切り抜きができる
- `dlib`、`cv2`、`numpy`を必要に応じてインストールする
- `shape = 'rect' or 'circle'` 顔の位置や写真の大きさを考慮しつつ、適切に長方形か円に切り取ってくれる
- `'rect'` なら `size = [width, height]`、 `'circle'` なら `size = r（半径）`
- `padding`：[上,右,下,左] にパディングを付与する割合。デフォルトは `[1,1,1,1]`
    - 切り取った顔そのままだと、とても顔がデカくなるため
- 返り値は、作成した画像のパス
- 顔写真が必要な場合に利用する。具体的なコードは `makePDFCard.py` 参照


# 環境
- python が使えて、各種ライブラリがインストールできれば大丈夫。`pip install -r requirements.txt` でインストールしてください
- `opencv-python`、`poppler`、`fonttools`、`face_recognition_models`、`face_recognition`、`np` のインストールは必要に応じて行ってください
- フォントデータは、デフォルトでは無料で使える`ipaexm.ttf`を同じディレクトリに入れて利用しています（[参考](https://qiita.com/programing_diy_kanrinin/items/898634074c6ac36c3bf1)）
- `./csv` に csv ファイル, `./png` に png ファイル, `./pdf` に作成した pdf ファイルをそれぞれ格納していいます
