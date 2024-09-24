# ネームタグ作成
`generate_business_cards(output_pdf, data, bg_image_path)`

csv形式のデータから、ネームタグを作る。A4サイズで8枚できる。

`python3 makeNameTag.py`で実行できる

- `name_tag.csv` がデータで、「役職, 名前, ふりがな」
- `name_tag.png` が、ネームタグの背景
- 役職は、30文字以内のみ対応可能（変更は容易に可能）
- あまりにも長すぎる名前は対応不可能
- ネームタグに合わせて、`draw_business_card()`のコードを変更する
- A4 の８分割より小さいサイズに対応している
- 苗字と名前はあらかじめスペースを空けておくこと推奨

# 自己紹介カード作成
`generate_self_introduction_cards(output_pdf, data, bg_image_path)`

csv形式のデータから、自己紹介カードを作る。一人あたり1ページを想定。

`python3 makeNamePlate.py`で実行できる

- `introduce_data.csv` がデータで、デフォルトは、名前,ふりがな,所属チーム,出身地,学部,趣味または特技,興味のある分野,サークル,やりたいこと,意気込み, がカラム名になっている
- `introduce.png`が自己紹介カードの背景
- 自己紹介の内容に合わせて、`draw_introduce_card()`のコードを変更する

# その他関数
`fit_text_to_width(c, text, x, y, max_width, font_name, max_font_size)`

ある幅に合うように文字サイズを変更してくれる関数。ただし、1文限定である。
そのため、幅に対して文字数が長すぎると、とんでもなく文字サイズが小さくなる場合がある。

`fit_text_to_width_height(c, text, x, y, max_width, max_height, font_name, max_font_size)`

ある長方形の中に文章を適切に入れてくれる。
- 左揃え、中揃えである
- 文字サイズの最大値以下で、長方形に収まってかつ文字サイズが最も大きくなるように文章を配置する
- 句読点の位置や文字の切れ目は考慮しない。必要ならデータ時点で改行などをする必要がある
- 長方形の大きさは `c.rect(x, y, 長方形の幅, 長方形の高さ)` で確認すれば良い。



# 環境
python が使えて、各種ライブラリがインストールできれば大丈夫。`requirements.txt`は書いてないです……。