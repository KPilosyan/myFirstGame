import os
from math import sin, radians, degrees, copysign, sqrt, ceil
import time
import pygame
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, angle=0.0, carLength=1.5, max_steering=80):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = carLength
        self.max_steering = max_steering
        # self.turning_radius = 100
        self.max_velocity = 8
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.max_velocity, 0)
        self.velocity.x = self.max_velocity
        

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering)) 
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
    
class Collision:
    def __init__(self, position):
        self.position = position 

    def borderCollision(self, screenWidth, screenHeight):

        x = self.position[0]
        y = self.position[1]
        
        return x <= 185 or y <= 100 or x >= screenWidth - 210 or y >= screenHeight - 120 


    def traceCollision(self, traceCoords1, traceCoords2, eps1, eps2):
        collide = 0
        
        if eps1 and eps2:
            dddd = []
            for i in traceCoords1[:-1]:
                diff = self.position - i
                xx = diff[0]
                yy = diff[1]
                collide += sqrt(xx**2+yy**2) < eps1 
                dddd.append(sqrt(xx**2+yy**2))

            for i in traceCoords2[:-1]:
                diff = self.position - i
                xx = diff[0]
                yy = diff[1]
                collide += sqrt(xx**2+yy**2) < eps2 
                dddd.append(sqrt(xx**2+yy**2))

            return bool(collide)
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tron")
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h 
        monitor_size = [self.width, self.height]
        # self.width = 1200
        # self.height = 750
        self.screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.ticks = 80
        self.exit = False
        
    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path1 = os.path.join(current_dir, "tr1.png")
        car_image1 = pygame.image.load(image_path1)
        image_path2 = os.path.join(current_dir, "car2.png")
        car_image2 = pygame.image.load(image_path2)
        # bg = pygame.image.load('Tron.png')
        self.screen.fill((50, 80, 55))
        data = pygame.image.tostring(self.screen,'RGBA')
        # tr = pygame.image.load('trace.png')
        # pygame.image.save(self.screen,"screenshot.jpeg")
        player1 = Car(25, 25)
        player2 = Car(10, 10)
        ppu = 32
        count = 0
        # k = 3
        cc = 0
        trace_length = 50
        trace_gap = 5
        # 
        trace1 = []
        trace2 = []

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queuea
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()
            rotated1 = pygame.transform.rotate(car_image1, player1.angle)
            rect1 = rotated1.get_rect()
            rotated2 = pygame.transform.rotate(car_image2, player2.angle)
            rect2 = rotated2.get_rect()
            # rotated_tr = pygame.transform.rotate(tr, player1.angle)

            if pressed[pygame.K_RIGHT]:
                player1.steering -= 1000 * dt
            elif pressed[pygame.K_LEFT]:
                player1.steering += 1000 * dt
            else:
                player1.steering = 0
            player1.steering = max(-player1.max_steering, min(player1.steering, player1.max_steering))

            if pressed[pygame.K_d]:
                player2.steering -= 1000 * dt
            elif pressed[pygame.K_a]:
                player2.steering += 1000 * dt
            else:
                player2.steering = 0
            player2.steering = max(-player2.max_steering, min(player2.steering, player2.max_steering))


            # Logic

            player1.update(dt)
            player2.update(dt)
            if Collision(player1.position * ppu - (rect1.width / 2, rect1.height / 2)).borderCollision(self.width, self.height):
                self.exit = True
            if Collision(player2.position * ppu - (rect2.width / 2, rect2.height / 2)).borderCollision(self.width, self.height):
                self.exit = True
            
            traces = count / trace_length
            # traceGap = k / 3
            
            
            if traces.is_integer() == False and count != 0 and (cc >= trace_gap or cc==0): 
                
                trace1.append(tuple(player1.position * ppu - (rect1.width / 2, rect1.height / 2)))
                trace2.append(tuple(player2.position * ppu - (rect2.width / 2, rect2.height / 2)))
                
                if cc==0:
                    firstElement = trace1[-1][0] - trace1[-2][0]
                    secondElement = trace1[-1][1] - trace1[-2][1]
                    eps1 = sqrt(firstElement ** 2 + secondElement ** 2)
                    firstElement = trace2[-1][0] - trace2[-2][0]
                    secondElement = trace2[-1][1] - trace2[-2][1]
                    eps2 = sqrt(firstElement ** 2 + secondElement ** 2)
                
                # if len(trace)-1 >= k:
                #     del trace[k]
                #     k += 3                
                cc=0
                
                self.screen.blit(rotated1, player1.position * ppu - (rect1.width / 2, rect1.height / 2))
                self.screen.blit(rotated2, player2.position * ppu - (rect2.width / 2, rect2.height / 2))
                trrrr = (count+1)/trace_length
                if trrrr.is_integer():
                    data = pygame.image.tostring(self.screen,'RGBA')#.save(self.screen,"screenshot.jpeg")
                
                pygame.display.flip()

            else:  #tunnel
                cc+=1   
                # self.screen.blit(bg, (0,0))
                # saved_screen = pygame.image.load('screenshot.jpeg')
                bumagaga = pygame.image.fromstring(data, (self.width,self.height), 'RGBA')
                self.screen.blit(bumagaga,(0,0))
                
                self.screen.blit(rotated1, player1.position * ppu - (rect1.width / 2, rect1.height / 2))
                self.screen.blit(rotated2, player2.position * ppu - (rect2.width / 2, rect2.height / 2))
                pygame.display.flip()
                
            try:
            
                if Collision(player1.position * ppu - (rect1.width / 2, rect1.height / 2)).traceCollision(trace1,trace2, eps1, eps2):
                    self.exit = True
                if Collision(player2.position * ppu - (rect2.width / 2, rect2.height / 2)).traceCollision(trace2,trace1, eps2, eps1):
                    self.exit = True
            except:
                pass

            self.clock.tick(self.ticks)         
            

            # Drawing
        
            
            # try:
            #     self.screen.blit(tr, trace[-1] * ppu - (rect.width / 2, rect.height / 2))
            # except:
            #     pass
            
                
            
            count += 1
            # k += 1
            
            # pygame.display.flip()
                        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()