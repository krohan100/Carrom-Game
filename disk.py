import pygame
import random
import math
 
class Disk(pygame.sprite.Sprite):
 
    def __init__(self, board, color, radius, mass, is_striker=False):
 
 
        pygame.sprite.Sprite.__init__(self)             #Initialise Sprite
        self.board          = board
        self.arena_width    = board.ARENA_WIDTH
        self.arena_height   = board.ARENA_HEIGHT
        self.color          = color
        self.radius         = radius
        self.mass           = mass
        self.image          = pygame.Surface([2*radius,2*radius])     #Sprite as a surface
        self.image.fill(board.WHITE)                          #White Background
        self.image.set_colorkey(board.WHITE)

        #pygame.draw.ellipse(self.image,color,[0,0,2*radius,2*radius]) #Make the circle
        pygame.draw.circle(self.image,color,[int(radius),int(radius)],int(radius))
             
 
        self.rect   = self.image.get_rect()       #rectangle for the sprite
        self.rect.x = random.randrange(board.BOARD_THICKNESS, board.BOARD_THICKNESS + board.ARENA_WIDTH)
        self.rect.y = random.randrange(board.BOARD_THICKNESS, board.BOARD_THICKNESS + board.ARENA_HEIGHT)
 
        self.other_disks = pygame.sprite.Group()
        self.speed      = [0,0]
        self.speed[0]   = 0 #random.randrange(-8,8)
        self.speed[1]   = 0 #random.randrange(-8,8)
        self.speed_changed = False
 
        self.is_striker = is_striker
 
 
 
    def reflect(self):
        if self.rect.x < self.board.BOARD_THICKNESS:
            self.set_pos(self.board.BOARD_THICKNESS,self.rect.y)
            self.speed[0] = abs(self.speed[0]) * self.board.HIT_LOSS
 
        if self.rect.x > self.board.ARENA_WIDTH + self.board.BOARD_THICKNESS - 2*self.radius:
            self.set_pos(self.board.ARENA_WIDTH + self.board.BOARD_THICKNESS - 2*self.radius,self.rect.y)
            self.speed[0] = -abs(self.speed[0]) *self.board.HIT_LOSS
 
        if self.rect.y < self.board.BOARD_THICKNESS:
            self.set_pos(self.rect.x, self.board.BOARD_THICKNESS)
            self.speed[1] = abs(self.speed[1]) * self.board.HIT_LOSS
 
        if self.rect.y > self.board.ARENA_HEIGHT + self.board.BOARD_THICKNESS - 2*self.radius:
            self.set_pos(self.rect.x,self.board.ARENA_HEIGHT + self.board.BOARD_THICKNESS - 2*self.radius)
            self.speed[1] = -abs(self.speed[1]) * self.board.HIT_LOSS
 
    def collide(self):
 
        if self.board.state == 3:
 
            self.other_disks.empty()
 
            for disk in self.board.disk_list:
                if disk != self:
                    self.other_disks.add(disk)
 
            for disk in  self.other_disks:
                self.board.collideDisk(self, disk)
 
    def go_to_holes(self):
         for hole in self.board.hole_list:
            if self.board.is_in_region(self.rect.x, self.rect.y, hole.x, hole.y, hole.x + 2*self.board.HOLE_RADIUS, hole.y + 2*self.board.HOLE_RADIUS):
 
                if self.is_striker == True:
                    self.board.striker_in_hole = True
 
                if self.is_striker == False:
                    if self.color == self.board.BLACK:
                        #self.board.score += 10
                        self.board.black_in_hole = True
                        self.board.number_of_blacks = self.board.number_of_blacks + 1
                        print "Black in Hole"
                    if self.color == self.board.SANDY_BROWN:
                        #self.board.score += 20
                        self.board.white_in_hole = True
                        self.board.number_of_whites = self.board.number_of_whites + 1
                        print "White in Hole"
                    if self.color == self.board.VIOLET_RED:
                        #self.board.score += 50
                        self.board.queen_in_hole = True
 
 
                self.board.disk_list.remove(self)
 
                #print self.board.score 
 
    def set_pos(self,x,y):
 
        self.rect.x = x
        self.rect.y = y
 
 
 
 
 
    def update(self):
 
 
 
        self.reflect()
        self.collide()
        self.go_to_holes()
 
        if self.board.mod(self.speed) < 1:
            self.speed = [0,0]
        else:
            self.speed[0] = self.speed[0] - self.board.FRICTION*(self.speed[0]/self.board.mod(self.speed))
            self.speed[1] = self.speed[1] - self.board.FRICTION*(self.speed[1]/self.board.mod(self.speed))
 
 
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
 
class Striker(Disk):
 
    def __init__(self,board,color,radius,mass,is_striker):
 
        super(Striker,self).__init__(board,color,radius,mass,is_striker)
 
    def update(self):
        pos = pygame.mouse.get_pos()
 
        x = pos[0]
        y = pos[1]
 
 
        if self.board.state == 0:
 
            self.set_striker_pos(x,y)
 
        elif self.board.state == 1:
 
            self.correct_placement = True
            self.correct_direction = True
 
            # TO see that the striker is not overlapping with any disk that is lying on the striker-bar
            for disk in self.other_disks:
                if pygame.sprite.collide_circle(self,disk):
                    self.correct_placement = False
                    break
 
            # To see that the Striker is not overlapping with the corner circles
            '''
            if self.board.current_player.position == "bottom" or self.board.current_player.position == "top":
                if (self.rect.x > self.board.current_player.low_limit and self.rect.x < (self.board.current_player.low_limit + self.board.BAND_HEIGHT)) or (self.rect.x > (self.board.current_player.high_limit - self.board.BAND_HEIGHT) and self.rect.x < self.board.current_player.high_limit):
                    self.correct_placement = False
            elif self.board.current_player.position == "left" or self.board.current_player.position == "right":
                if (self.rect.y > self.board.current_player.low_limit and self.rect.y < (self.board.current_player.low_limit + self.board.BAND_HEIGHT)) or (self.rect.y > (self.board.current_player.high_limit - self.board.BAND_HEIGHT) and self.rect.y < self.board.current_player.high_limit):
                    self.correct_placement = False
            '''
 
            if self.correct_placement == True:
                if self.board.current_player.position == "bottom":
 
                    if y > self.board.BOTTOM_BAND.y + self.board.BAND_HEIGHT/2 :
                        pygame.draw.line(self.board.screen, self.board.RED, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1) 
                        self.correct_direction = False
                    else :
                        pygame.draw.line(self.board.screen, self.board.BLUE, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1)
 
                elif self.board.current_player.position == "top":
 
                    if y < self.board.TOP_BAND.y + self.board.BAND_HEIGHT/2:
                        pygame.draw.line(self.board.screen, self.board.RED, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1) 
                        self.correct_direction = False
                    else:
                        pygame.draw.line(self.board.screen, self.board.BLUE, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1)
 
                elif self.board.current_player.position == "left":
 
                    if x < self.board.LEFT_BAND.x + self.board.BAND_HEIGHT/2:
                        pygame.draw.line(self.board.screen, self.board.RED, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1) 
                        self.correct_direction = False
                    else:
                        pygame.draw.line(self.board.screen, self.board.BLUE, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1)
 
                elif self.board.current_player.position == "right":
 
                    if x > self.board.RIGHT_BAND.x + self.board.BAND_HEIGHT/2:
                        pygame.draw.line(self.board.screen, self.board.RED, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1) 
                        self.correct_direction = False
                    else:
                        pygame.draw.line(self.board.screen, self.board.BLUE, (self.rect.x + self.radius,self.rect.y + self.radius), pos, 1)
            else:
                self.board.state = 0
 
 
        elif self.board.state == 2:
 
            if(self.correct_direction == False):
                self.board.state = 1
                return
 
            self.board.state = 3
            direction = [pos[0] - (self.rect.x + self.radius),pos[1] - (self.rect.y + self.radius)]
            dist =  math.sqrt((pos[0] - (self.rect.x + self.radius))**2 + (pos[1] - (self.rect.y + self.radius))**2)
 
            self.speed[0] += 15*direction[0]/dist
            self.speed[1] += 15*direction[1]/dist
 
            print self.speed
 
            #self.board.striker.reflect()
            #self.board.striker.collide()
            #print str(self.board.striker.speed[0]) + str(self.board.striker.speed[1])
 
        super(Striker, self).update()
 
    def set_striker_pos(self,x,y):
 
        if self.board.current_player.position == "top" or self.board.current_player.position == "bottom":
 
            self.rect.x = x - self.radius
            self.rect.y = self.board.current_player.fixed_limit
 
            if self.rect.x >= self.board.current_player.high_limit - self.board.BAND_HEIGHT/2:
                self.rect.x = self.board.current_player.high_limit - self.board.BAND_HEIGHT/2
 
            if self.rect.x <= self.board.current_player.low_limit - self.board.BAND_HEIGHT/2:
                self.rect.x = self.board.current_player.low_limit - self.board.BAND_HEIGHT/2
 
        elif self.board.current_player.position == "left" or self.board.current_player.position == "right":
 
            self.rect.y = y - self.radius
            self.rect.x = self.board.current_player.fixed_limit
 
            if self.rect.y >= self.board.current_player.high_limit - self.board.BAND_HEIGHT/2:
                self.rect.y = self.board.current_player.high_limit - self.board.BAND_HEIGHT/2
 
            if self.rect.y <= self.board.current_player.low_limit - self.board.BAND_HEIGHT/2:
                self.rect.y = self.board.current_player.low_limit - self.board.BAND_HEIGHT/2
 
 
