import os
import cv2
from PIL import Image
import pyocr

gra = input("確認する画像ファイルのパスを入力してください。：")


img=cv2.imread(gra,cv2.IMREAD_COLOR)
h,w=img.shape[:2]
split_x=3
split_y=4

# OCRエンジンを取得
engines = pyocr.get_available_tools()
engine = engines[0]

# 対応言語取得
langs = engine.get_available_languages()
#print("対応言語:",langs) # ['eng', 'jpn', 'osd']

#画像の分割処理
cx=0
cy=0
x=0

word = input("検索する文字列を入力してください。：")

for j in range(split_x):
    for i in range(split_y):
        split_pic=img[cy:cy+int(h/split_y),cx:cx+int(w/split_x),:]
        imdata = 'test/split_y'+str(i)+'_x'+str(j)+'.jpg'
        cv2.imwrite(imdata,split_pic)
        cy=cy+int(h/split_y)

        # 画像の文字を読み込む
        txt = engine.image_to_string(Image.open(imdata), lang="jpn",
                                     builder=pyocr.builders.TextBuilder(tesseract_layout=6)) # レイアウト指定
        
        #いずれかの文字列を探す
        #見つかったらxに1足す
        if word in txt:
            x += 1
        else :
            x += 0

        os.remove(imdata)


    cy=0
    cx=cx+int(w/split_x)

if x > 0 :
    print("あり")
else :
    print("なし")
