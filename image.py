import cv2
import numpy as np

class Image(object):
    def __init__(self, image, title="picture"):
        if (isinstance(image, Image)):
            image = image.raw
        # BGR image
        self.raw = image
        self.point1 = (0, 0)
        self.point2 = (0, 0)
        self.title = title
        self.select_image = np.zeros(1)

    def match(self, tpl, resize=1):
        if (isinstance(tpl, Image)):
            tpl = tpl.raw
        height, width = tpl.shape[:2]
        tpl = cv2.resize(tpl, (int(width*resize), int(height*resize)))
        result = cv2.matchTemplate(self.raw, tpl, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        loc = [0, 0]
        loc[0] = int(max_loc[0])
        loc[1] = int(max_loc[1])
        if (max_val < 0.6):
            return None, None
        return (loc[0], loc[1]), (loc[0]+width, loc[1]+height)


    def waitKey(self):
        cv2.waitKey(0)

    def show(self):
        cv2.imshow(self.title, self.raw)

    def read(filename):
        return Image(cv2.imread(filename, cv2.IMREAD_COLOR))

    def save(self, filename):
        cv2.imwrite(filename, self.raw)

    def select(self):
        cv2.imshow(self.title, self.raw)
        cv2.setMouseCallback(self.title, self.on_mouse)
        cv2.waitKey(0)
        return self.select_image

    def on_mouse(self, event, x, y, flags, param):
        origin_image = self.raw
        img = origin_image.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point1 = (x,y)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):        
            cv2.rectangle(img, self.point1, (x,y), (255,0,0), 3)
            cv2.imshow(self.title, img)
        elif event == cv2.EVENT_LBUTTONUP:
            self.point2 = (x,y)
            cv2.rectangle(img, self.point1, self.point2, (255,0,0), 3) 
            min_x = min(self.point1[0], self.point2[0])     
            min_y = min(self.point1[1], self.point2[1])
            width = abs(self.point1[0]-self.point2[0])
            height = abs(self.point1[1]-self.point2[1])
            self.select_image = Image(origin_image[min_y:min_y+height, min_x:min_x+width], 'cut')
    pass    
