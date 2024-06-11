# import cv2 as cv
# from cvzone.ClassificationModule import Classifier
# mydata = Classifier('keras_model.h5','labels.txt')
# cap=cv.VideoCapture(0)
# while True:
#     _,img=cap.read()
#     predict,index = mydata.getPrediction(img,color=(0,0,255))
#     print(predict,index)
#     cv.imshow('frame',img)
#     key= cv.waitKey(1)
#     if key==27:
#         break

import cv2 as cv
from cvzone.ClassificationModule import Classifier

class ClassificationApp:
    def __init__(self, model_path, labels_path):
        self.mydata = Classifier(model_path, labels_path)

    def run(self):
        cap = cv.VideoCapture(0)
        
        while True:
            ret, img = cap.read()
            if not ret:
                break
            
            predict, index = self.mydata.getPrediction(img, color=(0, 0, 255))
            print(predict, index)
            
            cv.imshow('frame', img)
            key = cv.waitKey(1)
            if key == 27:
                break
        
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    model_path = 'keras_model.h5'
    labels_path = 'labels.txt'

    app = ClassificationApp(model_path, labels_path)
    app.run()
