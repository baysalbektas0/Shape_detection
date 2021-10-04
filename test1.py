# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 18:44:32 2021

@author: BektasBaysal

"""
import cv2
import math
# fileName = input("file:")
fileName = "Circle.jpg"
# fileName = "Triangle.jpg"
image = cv2.imread(fileName)
image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cimg = image2.copy()

ret, thresh = cv2.threshold(cimg, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
"""threshold kullanılırken otsu methodu iyi bir sonuç verildiği araştırmalar sonucunda görülmüştür.
    kaynak: https://docs.opencv.org/3.1.0/d7/d4d/tutorial_py_thresholding.html"""
contours1, hierarchy1 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

"""keanrları tespit etmek için opencv kütüphanesinin findContours fonksiyonu kullanılmıştır."""
""" Kaynak: https://docs.opencv.org/4.5.1/d4/d73/tutorial_py_contours_begin.html"""
"""RETR_TREE:  tüm çevre koordiantlarını alır ve iç içe koordinatların tam bir hiyerarşisini yeniden oluşturur."""
"""CHAIN_APPROX_NONE: Tüm çevre noktalarını saklar  """
"""kaynak: https://docs.opencv.org/4.5.1/d3/dc0/group__imgproc__shape.html#gga4303f45752694956374734a03c54d5ffaf7d9a3582d021d5dadcb0e37201a62f8"""
for cnt in contours1:
    epsilon = 0.01* cv2.arcLength(cnt,True ) # approx başarımı veriyor, 0.01 değeri sayının %10 unu alınıyor demek, arcLength contour çevresini veriyor.
    approx = cv2.approxPolyDP(cnt,epsilon , True) 
    """kaynak: https://docs.opencv.org/4.5.1/d3/dc0/group__imgproc__shape.html#gga4303f45752694956374734a03c54d5ffaf7d9a3582d021d5dadcb0e37201a62f8"""
    if len(approx) == 3:
        w, h = thresh.shape[:2]
        print("üçgen")
        print(approx)
        """approx ile üçgenin köşe koordinatları alındı"""
        a = round((math.sqrt((approx[0][0][0]-approx[1][0][0] )**2+(approx[0][0][1]-approx[1][0][1])**2))*5/w)
        b = round(( math.sqrt((approx[0][0][0]-approx[2][0][0] )**2+(approx[0][0][1]-approx[2][0][1])**2))*5/w)
        c = round((math.sqrt((approx[1][0][0]-approx[2][0][0] )**2+(approx[1][0][1]-approx[2][0][1])**2))*5/w)
        UcgeninCevresi = a + b + c
        Text = "Ucgen, Cevresi {} metre".format(UcgeninCevresi)
        cv2.putText(cimg, Text, (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
        
        
    else:
        print("yuvarlak")
        
        """Yuvarlak için ağırlık merkezini hesaplama işlemi
           Kaynak: https://docs.opencv.org/4.5.1/dd/d49/tutorial_py_contour_features.html """
        M = cv2.moments(cnt)        
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00']) 
        
        w, h = thresh.shape[:2]
        
        for i in range(0,w):
            for j in range(0,h):
                if thresh[i,j] == 255:
                   YariCapX = i
                   YariCapY = j
                   """255 değere sahip yuvarlağı oluşturan son pixelin koordinatları alınıyor. 
                   Çünkü yarıçap yuvarlağın kenarını oluşturan pixellerin hepsine aynı uzaklıkta olması gerekmetedir"""
                   break
               
                
        """Yarıçap formulü uygulandı => (x-xa)^2 +(y-ya)^2 = r^2"""  
        """Yarıçap uzunluğuna denk gelen pixel sayısı bulunur"""  
        
        YariCapPixelSayısı = round(math.sqrt((cx-YariCapX)**2+(cy-YariCapY)**2),2)
        print("Yuvarlığın yarıçapına denk gelen matris sayısı: {}".format(YariCapPixelSayısı))
        
        """Bu kısımda resim çerçevesi 5m X 5m uzunluğunda verilmiştir. 1 pixel kaç metreye tekabul ettiği 5m/640 ile bulunup
        pixel sayısıyla çarpılıp yarıçapın metre cinsinden değeri bulunmuştur."""
        
        YariCapMetre = round(YariCapPixelSayısı*5/w,2)
        print("Yarı çapın metre birimde uzunluğu: {}".format(YariCapMetre))
        
        """Çevre 2*pi*r formulüyle bulunmuştur"""
        
        Cevre = round(2*3.14*YariCapMetre,2)
        print("Yuvarlağın çevresi {} metre".format(Cevre))
        
        
        Text = "Yuvarlak, Cevresi {} metre".format(Cevre)
        cv2.putText(cimg, Text, (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
        
cv2.imshow("image",cimg)
cv2.imwrite("sonuc2.jpg", cimg)

cv2.waitKey(0)
cv2.destroyAllWindows()





    

            
            
    