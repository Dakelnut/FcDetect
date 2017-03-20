from sklearn.model_selection import cross_val_score
import cv2
from sklearn.utils import shuffle
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
import os
from time import sleep
import sys
import numpy as np
import  pickle
#Load the database of faces
#Load database of none_faces
#Make them grey
#Shape them to 21 on 21

Do_you_need_to_train_net = True

path_of_positive_data = r"C:\Users\Dakelnut\Dropbox\Моё\Проекты\Программы Python\Main_BD_Faces\Positive_images"
path_of_negative_data = r"C:\Users\Dakelnut\Dropbox\Моё\Проекты\Программы Python\Main_BD_Faces\Negative_images"

name_of_clf_file = "my_estimator.pkl"
current_working_directory = os.getcwd()

class AdaBoost():

    X_of_pos = []
    X_of_neg = []

    w, h = 21,21

    ada = AdaBoostClassifier(n_estimators=100)

    ans = False

    def __init__(self,answ = None,frame = None):

        if answ == None:
            while True:
                val = input("Do you need to train the net?(y,n)")
                val = "n"
                if val == "y":
                    self.teach_net()
                    break
                elif val == "n":
                    self.use_net()
                    break
        else: self.use_net(frame)

    def teach_net(self):

        def load_database(path):
            os.chdir(path)
            mas = []
            o = 0
            for name_of_image in os.listdir():
                o = o + 1
                buf_mas = []
                print(name_of_image)
                img = cv2.imread(name_of_image)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (21, 21))
                for i in range(len(img)):
                    buf_mas = np.concatenate((buf_mas,img[i]))
                mas.append(buf_mas)

            return mas

        self.X_of_pos = load_database(path_of_positive_data)
        self.X_of_neg = load_database(path_of_negative_data)
        os.chdir(current_working_directory)

        y_of_pos = [1 for i in range(len(self.X_of_pos))]
        y_of_neg = [0 for j in range(len(self.X_of_neg))]

        X =  np.concatenate((self.X_of_pos, self.X_of_neg))
        X = np.array(X, dtype=np.float64) / 255

        y =  np.concatenate((y_of_pos,y_of_neg))

        X, y = shuffle(X, y, random_state=0)

        try:
            self.ada.fit(X,y)
        except:
            print("Something wrong with types of data or target")
            sys.exit()

        try:
            scores = cross_val_score(self.ada, X, y)
        except:
            print("Not enough examples")
            sys.exit()

        print("Accuracy is ",scores.mean())

        joblib.dump(self.ada, name_of_clf_file)

        print("Estimator is safe in file named:",name_of_clf_file)

        sys.exit()


    def use_net(self, frame=None):
        # try:
        # print(name_of_clf_file)
        self.ada = joblib.load(name_of_clf_file)
        # except:
        #     print("Weights not found. Reteach the net")
        #     sys.exit()
        #
        # frame = cv2.imread("13.jpg")
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize(frame, (self.w, self.h))
        frame = np.resize(frame, (self.w, self.h))

        buf_mas = []
        for i in range(len(frame)):
            buf_mas = np.concatenate((buf_mas, frame[i]))
        buf_mas = np.array(buf_mas, dtype=np.float64) / 255
        buf_mas = buf_mas.reshape(1, -1)
        answer = self.ada.predict(buf_mas)
        # print(answer)
        if answer >= 0.65:
            #print("The prediction is ",answer," may be it`s True")
            # print(True)
            self.ans = True
        else:
            # print("The prediction is ",answer," may be it`s false")
            # print(False)
            self.ans =  False















# clf = AdaBoostClassifier(n_estimators=100)
# scores = cross_val_score(clf, iris.data, iris.target)
# scores.mean()



# iris_X_train = iris_X[indices[:-10]]
# iris_y_train = iris_y[indices[:-10]]
# iris_X_test  = iris_X[indices[-10:]]
# iris_y_test  = iris_y[indices[-10:]]
# # Create and fit buf_mas nearest-neighbor classifier
# from sklearn.neighbors import KNeighborsClassifier
# knn = KNeighborsClassifier()
# knn.fit(iris_X_train, iris_y_train)
#
#
#
# knn.predict(iris_X_test)
#
# iris_y_test
