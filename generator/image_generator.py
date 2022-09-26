import numpy as np
import time
import cv2
from scipy.spatial import distance


class MovingObject():
    def __init__(self, id, x, y, xspeed, yspeed, intensity, size, lifetime):
        self.id = id
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.lifetime = lifetime
        self.intensity = intensity
        self.size = size

    def get_xy(self):
        return (self.x, self.y)

    def get_distance(self):
        a = (self.x, self.y)
        b = (self.x + self.xspeed, self.y+self.yspeed)
        return distance.euclidean(a,b)

    def get_angle(self):
        v0 = np.array([self.x, self.y]) - np.array([self.xspeed, self.yspeed])
        v1 = np.array([self.x, self.y]) - np.array([self.x, self.yspeed])
        angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
        return np.degrees(angle)

    def get_lifetime(self):
        return self.lifetime

    def update_object(self):
        self.x += self.xspeed
        self.y += self.yspeed
        self.lifetime -=1

    def out_of_bounds(self, image_width, image_height):
        if self.x < 0 or self.x > image_width or self.y < 0 or self.y > image_height:
            return True

class ImageGenerator():
    def __init__(self):
        self.nextid = 0
        helligkeit = 120
        self.width = 720
        self.height = 480

        # Generate blury night sky
        img = np.uint8(helligkeit*np.random.rand(self.height, self.width))
        self.scene = cv2.GaussianBlur(src=img, ksize=(21, 21), sigmaX=3)
        self.object_ids = []
        self.objects = []

    def next_image(self):


        chance = np.random.random()
        if chance>0.95:
            self.add_object(self.nextid)
            self.nextid+=1

        # Generate nois of cam
        im = np.zeros((self.height,self.width), np.uint8)
        noise = cv2.randn(im,(0),(5))
        image = cv2.add(self.scene, noise)

        #draw objects
        for id in self.object_ids:
            o = self.get_objectInstance(id)
            x, y = o.get_xy()
            intensity = o.intensity
            c = int(255/intensity)

            image = cv2.circle(image, (x,y), radius=o.size, color=(c, c, c), thickness=-1)
        
        self.update_objects()
        self.destroy_objects()
        return len(self.object_ids), image

    def add_object(self, id):
        x = np.random.randint(720)
        y = np.random.randint(480)
        xspeed = np.random.randint(10)
        yspeed = np.random.randint(low=-4, high=4)
        size = np.random.randint(4)
        intensity = np.random.randint(1,3)
        lifetime = np.random.randint(low=4, high=50)
        self.object_ids.append(id)
        self.objects.append(MovingObject(id, x, y, xspeed, yspeed, intensity, size, lifetime))


    def get_objectInstance(self, oid):
        for oinst in self.objects:
            if oinst.id == oid:
                return oinst

    def update_objects(self):
        new_ids = []
        for id in self.object_ids:
            o = self.get_objectInstance(id)

            o.update_object()
        self.object_ids+=new_ids

    def destroy_objects(self):
        for id in self.object_ids:
            o = self.get_objectInstance(id)
            if o.out_of_bounds(self.width, self.height) or o.get_lifetime()<=0:
                self.objects.remove(o)
                self.object_ids.remove(id)


# imgen = ImageGenerator()

# id = 0
# while True:
#     start = time.time()
    
#     n, img = imgen.next_image()

#     cv2.imshow('Image', img)
#     k = cv2.waitKey(27) & 0xFF
#     if k == ord('q'):
#         break

#     # Keep 25fps
#     time.sleep(max(1./25 - (time.time() - start), 0))

# cv2.destroyWindow('Image')
