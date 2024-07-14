import tkinter as tk
from tkinter import filedialog
from tkinter import *

import numpy as np
from PIL import ImageTk, Image
import numpy
from keras.models import load_model

#dung model da xay dung
model = load_model('traffic_sign_20207644.h5')

#cac nhan
classes = { 1:'Tốc độ tối đa cho phép (20km/h)',
            2:'Tốc độ tối đa cho phép (30km/h)',
            3:'Tốc độ tối đa cho phép (50km/h)',
            4:'Tốc độ tối đa cho phép (60km/h)',
            5:'Tốc độ tối đa cho phép (70km/h)',
            6:'Tốc độ tối đa cho phép (80km/h)',
            7:'Hết hạn chế tốc độ tối đa (80km/h)',
            8:'Tốc độ tối đa cho phép (100km/h)',
            9:'Tốc độ tối đa cho phép (120km/h)',
            10:'Cấm vượt',
            11:'Cấm ô tô tải vượt',
            12:'Giao nhau Với đường không ưu tiên',
            13:'Đường ưu tiên',
            14:'Giao nhau với đường ưu tiên',
            15:'Dừng lại',
            16:'Đường cấm',
            17:'Cấm xe tải',
            18:'Cấm đi ngược chiều',
            19:'Nguy hiểm khác',
            20:'Chỗ ngoặt nguy hiểm vòng bên trái',
            21:'Chỗ ngoặt nguy hiểm vòng bên phải',
            22:'Nhiều chỗ ngoặt nguy hiểm liên tiếp',
            23:'Đường không bằng phẳng',
            24:'Đường trơn',
            25:'Đường bị thu hẹp',
            26:'Đoạn đường đang thi công',
            27:'Giao nhau có tín hiệu đèn',
            28:'Đường nguười đi bộ cắt ngang',
            29:'Trẻ em',
            30:'Đường người đi xe đạp cắt ngang',
            31:'Beware of ice/snow',
            32:'Thú rừng vượt qua đường',
            33:'Hết mọi lệnh cấm',
            34:'Hướng đi phải theo: Chỉ được rẽ phải',
            35:'Hướng đi phải theo: Chỉ được rẽ trái',
            36:'Hướng đi phải theo: Chỉ được đi thẳng',
            37:'Hướng đi phải theo: Chỉ được đi thẳng và rẽ phải',
            38:'Hướng đi phải theo: Chỉ được đi thẳng và rẽ trái',
            39:'Hướng phải đi vòng chướng ngại vật',
            40:'Hướng trái đi vòng chướng ngại vật',
            41:'Nơi giao nhau chạy theo vòng xuyến',
            42:'Hết đoạn đường cấm vượt',
            43:'Hết đoạn đường cấm ô tô tải vượt' }

#xay dung giao dien
top=tk.Tk()
top.geometry('800x600')
top.title('Traffic sign recognition')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)
def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30,30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)
    pred_probabilities = model.predict([image])
    pred = np.argmax(pred_probabilities, axis=1)[0]
    print(pred)
    sign = classes[pred+1]
    print(sign)
    label.configure(foreground='#011638', text=sign)
def show_classify_button(file_path):
    classify_b=Button(top,text="Phân loại",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass
upload=Button(top,text="Thêm ảnh",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Phân loại biển báo giao thông",pady=20, font=('arial',20,'bold'))
heading.configure(background='#CDCDCD',foreground='#364156')
heading.pack()
top.mainloop()