import pytesseract
from PIL import Image
import re
import os
import colorsys
import PIL.Image as Image
#识别健康码主要颜色以判断是否为绿码
def get_dominant_color(image):
    max_score = 0.0001
    dominant_color = None
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        # 转为HSV标准
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)

        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color


pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(Image.open('./2EF3E0360DE3DFE9193FABD6D1A5A496.jpg'), lang='chi_sim')

textall = text.replace(" 年 ", "-").replace(" 月 ", "-").replace(" 日", " ").replace("/", "-").strip()
text = textall.split("\n")


for line in text:
    time = re.compile(r'\d{2}:\d{2}:\d{2}')
    timeres = time.findall(line)
    if timeres:
        now_time = line.split(' ')

    hsdays = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
    hsres = hsdays.findall(line)
    if hsres:
        hsresend = hsres[0]

print("现在时间:",now_time[0],now_time[-1])
print("核酸时间:",hsresend)
if "阴" in textall:
    print("核酸结果:阴性")
else:
    print("核酸结果:阳性")
a = get_dominant_color(Image.open('./2EF3E0360DE3DFE9193FABD6D1A5A496.jpg'))
if a[1] > a[0] and a[1] > a[2]:
    print("码色：绿码")
else:
    print("码色：黄红码")


# file_fold = './hesuans'
# allpersonlist = os.listdir(file_fold)
# with open('./result.txt', 'a') as f:
#     for one in allpersonlist:
#         aim_person_path = os.path.join(file_fold, one)
#         text = pytesseract.image_to_string(Image.open(aim_person_path), lang='chi_sim')
#
#         timeoft = 0
#         lines = text.split('\n\n')
#         for i in lines:
#             string = str(i)
#             time = re.compile(r'\d{2}:\d{2}:\d{2}')
#             timeres = time.findall(string)
#
#             if timeres:
#                 timeoft+=1
#                 timeres = timeres[0]
#                 days = re.compile(r'\d{4}-\d{2}-\d{2}')
#                 daysres = days.findall(string)[0]
#
#
#                 place = re.compile(r'(?<=构)\D*\n')
#                 placeres = place.findall(string)
#                 placeres = placeres[0].replace(' ', '')
#                 try:
#                     placeres_s = placeres.split('\n')[0].split(':')[1]
#                     placeres = placeres_s
#                 except:
#                     pass
#
#
#
#                 person = re.compile(r'(?<=人)\D*')
#                 personpres = person.findall(string)
#                 personpres = personpres[0].replace(' ', '')
#                 try:
#                     person2 = re.compile(r'(?<=\b)\D*')
#                     personpres2 = person2.findall(personpres)[0]
#                     personpres = personpres2
#                 except:
#                     pass
#
#
#
#                 res_sen = '检测人:{}  第{}次检测： 时间:{} {}  地点:{}'.format(personpres,timeoft,daysres, timeres, placeres)
#
#                 print(res_sen)
#
#
#                 f.write(res_sen+'\n')
#
#         print("=========")
#         f.write("\n")
