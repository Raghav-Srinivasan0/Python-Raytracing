from PIL import Image
import numpy as np
import math

DIMENSIONS = (1080,1080)

FILENAME = "new"

class Light:
   def __init__(self,position):
      self.position = position
   def getVectorTo(self,position):
      #print(type(position))
      return (position[0]-self.position[0],position[1]-self.position[1],position[2]-self.position[2])

class Ray:
   def __init__(self,point_a,point_b):
      self.vector = (point_b[0]-point_a[0],point_b[1]-point_a[1],point_b[2]-point_a[2])
      magnitude = math.sqrt(self.vector[0]**2+self.vector[1]**2+self.vector[2]**2)
      self.vector = (self.vector[0]/magnitude,self.vector[1]/magnitude,self.vector[2]/magnitude)
      self.constant = point_a
   def getPointOfCollision(self):
      a = self.vector[0]**2 + self.vector[1]**2 + self.vector[2]**2
      b = 2*(self.vector[0]*self.constant[0]+self.vector[1]*self.constant[1]+self.vector[2]*self.constant[2])
      c = -4 + self.constant[0]**2 + self.constant[1]**2 + self.constant[2]**2
      if b**2-4*a*c < 0:
         return -1
      elif b**2-4*a*c == 0:
         t = (-b + math.sqrt(b**2-4*a*c))/(2*a)
         return (self.vector[0]*t + self.constant[0],self.vector[1]*t + self.constant[1],self.vector[2]*t + self.constant[2])
      else:
         t1 = (-b + math.sqrt(b**2-4*a*c))/(2*a)
         t2 = (-b - math.sqrt(b**2-4*a*c))/(2*a)
         p1 = (self.vector[0]*t1 + self.constant[0],self.vector[1]*t1 + self.constant[1],self.vector[2]*t1 + self.constant[2])
         p2 = (self.vector[0]*t2 + self.constant[0],self.vector[1]*t2 + self.constant[1],self.vector[2]*t2 + self.constant[2])
         if math.dist(p1,self.constant) < math.dist(p2,self.constant):
            return p1
         else:
            return p2
   def generateReflection(self):
      collisionPoint = self.getPointOfCollision()
      weirdExpression = 2*((self.constant[0]*collisionPoint[0]+self.constant[1]*collisionPoint[1]+self.constant[2]*collisionPoint[2])/math.sqrt(collisionPoint[0]**2+collisionPoint[1]**2+collisionPoint[2]**2))
      return Ray(collisionPoint,(-self.constant[0]+weirdExpression*collisionPoint[0],-self.constant[1]+weirdExpression*collisionPoint[1],-self.constant[2]+weirdExpression*collisionPoint[2]))

class Camera:
   def __init__(self, position):
      self.position = position
      self.rays = [[0 for j in range(DIMENSIONS[1])] for i in range(DIMENSIONS[0])]
      for i in range(DIMENSIONS[0]):
         for j in range(DIMENSIONS[1]):
            self.rays[i][j] = Ray(self.position,((i-DIMENSIONS[0]/2)/(DIMENSIONS[0]/2),
                                                 (j-DIMENSIONS[1]/2)/(DIMENSIONS[1]/2),
                                                 self.position[2]+1))
   def render(self):
      pixels = [[0 for j in range(DIMENSIONS[1])] for i in range(DIMENSIONS[0])]
      for i in range(DIMENSIONS[0]):
         for j in range(DIMENSIONS[1]):
            poC = self.rays[i][j].getPointOfCollision()
            if poC != -1:
               lvector = light.getVectorTo(poC)
               intensity = poC[0]*lvector[0]+poC[1]*lvector[1]+poC[2]*lvector[2]
               intensity = 255/intensity
               pixels[i][j] = (intensity,0,0)
            else:
               pixels[i][j] = (0,0,0)
      return pixels

camera = Camera((0,0,-3))
light = Light((0,1,-1))

# Convert the pixels into an array using numpy
array = np.array(camera.render(), dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save(FILENAME + '.png')