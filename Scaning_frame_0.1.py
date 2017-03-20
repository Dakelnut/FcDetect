from PIL import Image
import cv2
from math import floor

import AdaBoost_test_01
import random
import time

# Размер картинки n на n
# Размер матрицы из AdaBoost y на y
# Размер фрейма z на z
# Причём  y < z < n
#
# Сканирую картинку фреймом z:
# —--Нахожу область где можно разместить фрейм
# —--Вырезаю её
# —--Сжимаю до размеров AdaBoost y на y
# —--Отправляю её в AdaBoost
# —--делаю отступ между фреймами
# —--Сканирую


#Используем cv2 для чтения


size = 21, 21
k=0



class Frame:

    list_of_frame_sizes = []

    size = 0

    image = []

    prev_i = 0

    prev_j = 0
    
    width = 0
    
    height = 0

    counter = 0

    copy_of_image = []

    coefficient = 5/4

    def __init__(self,image):

        self.image = image

        self.width = len(image[0])

        self.height = len(image)

        self.copy_of_image = [[0 for i in range(self.width)] for j in range(self.height)]

        if self.height <= self.width:
            self.list_of_frame_sizes = self.calculating_sizes_of_frames(self.height)
        else: self.list_of_frame_sizes = self.calculating_sizes_of_frames(self.width)
        
        print("List of frame sizes:")
        print(self.list_of_frame_sizes)
        self.list_of_frame_sizes = self.list_of_frame_sizes[0:2]
        self.list_of_frame_sizes = iter(self.list_of_frame_sizes)
        self.scaning(self.image)

    def calculating_sizes_of_frames(self,variable):

        #Geometric progression

        mas_of_results = []
        bn = 21

        while True:
            bn = floor(bn * self.coefficient)
            if bn >= variable:
                break
            mas_of_results.append((bn,bn))

        return list(reversed(mas_of_results))


    def scaning(self,image):

        try:

            self.size = next(self.list_of_frame_sizes)
            self.counter = 0
            print("Size=",self.size)
            distance_from_centre = self.size[0] // 2
        except:
            print("----------------------------------")
            print("-----------EndOfScaning-----------")
            print("----------------------------------")
            return self.copy_of_image



        for i in range(len(image)):
            for j in range(len(image[0])):

                if self.checking_condition(i,j,distance_from_centre) == True:
        
                    our_frame = image[i - distance_from_centre : i + distance_from_centre + 1]
                    our_frame = [our_frame[k][j-distance_from_centre : j + distance_from_centre + 1] for k in range(len(our_frame))]

                    answer =  AdaBoost_test_01.AdaBoost('n',our_frame).ans

                    if answer == True:

                        for m in range(i - distance_from_centre, i + distance_from_centre + 1):
                            for n in range(j - distance_from_centre, j + distance_from_centre + 1):
                                self.copy_of_image[m][n] = 1

        self.scaning(self.image)

    def print_copy(self):
        print("------------------------------------------")
        for v in range(len(self.copy_of_image)):
            print("|", end="")
            for b in range(len(self.copy_of_image[0])):
                print(self.copy_of_image[v][b],end="")
            print("|")
        print("------------------------------------------")



    def checking_condition(self,i,j,distance_from_centre):




        
        if (distance_from_centre <= i < self.height - distance_from_centre) and (distance_from_centre <= j < self.width - distance_from_centre):
            self.counter = self.counter + 1
            if self.counter == 1:
                self.prev_i = i
                self.prev_j = j

            zone = self.copy_of_image[i - distance_from_centre: i + distance_from_centre + 1]


            height_of_zone = len(zone)

            zone = [zone[k][j - distance_from_centre: j + distance_from_centre + 1] for k in range(len(zone))]


            width_of_zone = len(zone[0])
            num_of_pixels_in_zone = height_of_zone * width_of_zone

            if (abs(i - self.prev_i) >= distance_from_centre) or (abs(j - self.prev_j) >= distance_from_centre ) or self.counter == 1:
                self.prev_i = i
                self.prev_j = j
            else:
                return False

            if (round(zone.count(1)/num_of_pixels_in_zone,2)*100) <= 5 :
                return True
            else: return False

        else: return False



def main():
    start = time.time()
    image = cv2.imread(input("Type name of image: "))
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    fr = Frame(image_grey)
    for i in range(len(fr.copy_of_image)):
        for j in range(len(fr.copy_of_image[0])):
            if fr.copy_of_image[i][j] == 1:
                image[i][j] = image_grey[i][j]



    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    end = time.time()
    print("TIME:",end-start)



if __name__ == "__main__":
    main()