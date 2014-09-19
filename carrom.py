import pygame
from disk import *
from player import *
import random
from math import *
from numpy import *
 
class Carrom:
 
    def __init__(self):
 
        pygame.init()
 
        #COLORS           R     G    B
 
        self.BLACK        = (   0,   0,   0)
        self.WHITE        = ( 255, 255, 255)
        self.BLUE         = (   0,   0, 255)
        self.GREEN        = (   0, 255,   0)
        self.RED          = ( 255,   0,   0)
        self.SANDY_BROWN  = ( 244, 164,  96)
        self.CREAM        = ( 255, 255, 224)
        self.PINK         = ( 128,   0,   0)
        self.VIOLET_RED   = ( 139,  71,  93)
        #MAROON       = ( 128,   0,   0)
        #SALMON       = ( 255, 160, 122)
 
 
 
        # BOARD VARIABLES
        
        self.SCREEN_WIDTH       = 980
        self.SCREEN_HEIGHT      = 700
        self.BOARD_WIDTH        = 700   # I.e. Window Width
        self.BOARD_HEIGHT       = 700   # I.e. Window height
        self.ARENA_WIDTH        = 630   # Playing surface width
        self.ARENA_HEIGHT       = 630   # Playing surface height
        self.FPS                = 120   
        self.HOLE_RADIUS        = 30    # Radius of holes
        self.BOARD_THICKNESS    = (self.BOARD_WIDTH - self.ARENA_WIDTH)/2   # Wooden Border Thickness
        self.OFFSET_1           = 1.5*self.BOARD_THICKNESS + 2*self.HOLE_RADIUS 
        self.OFFSET_2           = 15
        self.CENTRE_RING_RADIUS = 20    # Circle that holds the Queen
        self.BAND_HEIGHT        =  0.9*self.BOARD_THICKNESS                 # Band in which the Striker is placed
        self.STRIKER_RADIUS     = self.BAND_HEIGHT/2
        self.DISK_RADIUS        = self.STRIKER_RADIUS*0.7   # Radius of Disk
        self.BAND_WIDTH         = (self.BOARD_WIDTH - 2*self.OFFSET_1 - 2*self.BAND_HEIGHT - 2*self.OFFSET_2)   # Band in which the Striker is placed
        self.MIDDLE_RING_RADIUS = int(round(5*self.DISK_RADIUS))            # Circle that holds all the disks in the centre
        #self.BAND_GAP           = (self.ARENA_WIDTH - self.BAND_WIDTH)/2
        self.ARENA_X            = (self.BOARD_WIDTH - self.ARENA_WIDTH)/2   # STARTING X CO-ORDINATE OF PLAYING ARENA
        self.ARENA_Y            = (self.BOARD_HEIGHT - self.ARENA_HEIGHT)/2 # STARTING Y CO-ORDINATE OF PLAYING ARENA
        #self.DISK_NUMBER        = 12
        self.HIT_LOSS           = 0.9   # Energy Loss due to collision
        self.FRICTION           = 0.07  # Friction
 
        self.SCREEN_SIZE         = (self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        self.BOARD_CENTER       = (self.BOARD_WIDTH/2,self.BOARD_HEIGHT/2)
        self.ARENA_SIZE         = (self.ARENA_WIDTH,self.ARENA_HEIGHT)
 
        self.VERTICAL_CENTER_LINE   = [[self.BOARD_WIDTH/2,self.BOARD_WIDTH/2 - self.MIDDLE_RING_RADIUS], [self.BOARD_WIDTH/2,self.BOARD_WIDTH/2 + self.MIDDLE_RING_RADIUS]]
        self.HORIZONTAL_CENTER_LINE = [[self.BOARD_WIDTH/2 - self.MIDDLE_RING_RADIUS,self.BOARD_WIDTH/2],[self.BOARD_WIDTH/2 + self.MIDDLE_RING_RADIUS,self.BOARD_WIDTH/2]]
        self.NWN_CENTER_LINE        = [[self.BOARD_WIDTH/2 - math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 - math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS], [self.BOARD_WIDTH/2 + math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 + math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS]]
        self.NWW_CENTER_LINE        = [[self.BOARD_WIDTH/2 - math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 - math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS], [self.BOARD_WIDTH/2 + math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 + math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS]]
        self.NEN_CENTER_LINE        = [[self.BOARD_WIDTH/2 + math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 - math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS], [self.BOARD_WIDTH/2 - math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 + math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS]]
        self.NEE_CENTER_LINE        = [[self.BOARD_WIDTH/2 + math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 - math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS], [self.BOARD_WIDTH/2 - math.cos(math.radians(30))*self.MIDDLE_RING_RADIUS, self.BOARD_WIDTH/2 + math.cos(math.radians(60))*self.MIDDLE_RING_RADIUS]]
 
        self.BAND_LENGTH = self.BAND_WIDTH
 
        self.TOP_BAND       = pygame.Rect(self.OFFSET_1 + self.BAND_HEIGHT + self.OFFSET_2, self.OFFSET_1, self.BAND_WIDTH, self.BAND_HEIGHT)
        self.BOTTOM_BAND    = pygame.Rect(self.OFFSET_1 + self.BAND_HEIGHT + self.OFFSET_2, self.BOARD_HEIGHT - self.OFFSET_1 - self.BAND_HEIGHT, self.BAND_WIDTH, self.BAND_HEIGHT)
        self.LEFT_BAND      = pygame.Rect(self.OFFSET_1, self.OFFSET_1 + self.BAND_HEIGHT + self.OFFSET_2, self.BAND_HEIGHT, self.BAND_WIDTH)
        self.RIGHT_BAND     = pygame.Rect(self.BOARD_WIDTH - self.OFFSET_1 - self.BAND_HEIGHT, self.OFFSET_1 + self.BAND_HEIGHT + self.OFFSET_2, self.BAND_HEIGHT, self.BAND_WIDTH)
 
        self.TOP_LEFT_CIRCLE        = pygame.Rect(self.TOP_BAND.x - self.BAND_HEIGHT/2, self.TOP_BAND.y, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.TOP_RIGHT_CIRCLE       = pygame.Rect(self.TOP_BAND.x + self.BAND_LENGTH - self.BAND_HEIGHT/2,self.TOP_BAND.y, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.LEFT_TOP_CIRCLE        = pygame.Rect(self.LEFT_BAND.x, self.LEFT_BAND.y - self.BAND_HEIGHT/2, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.LEFT_BOTTOM_CIRCLE     = pygame.Rect(self.LEFT_BAND.x, self.LEFT_BAND.y + self.BAND_LENGTH - self.BAND_HEIGHT/2, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.BOTTOM_LEFT_CIRCLE     = pygame.Rect(self.BOTTOM_BAND.x - self.BAND_HEIGHT/2, self.BOTTOM_BAND.y, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.BOTTOM_RIGHT_CIRCLE    = pygame.Rect(self.BOTTOM_BAND.x + self.BAND_LENGTH - self.BAND_HEIGHT/2, self.BOTTOM_BAND.y, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.RIGHT_TOP_CIRCLE       = pygame.Rect(self.RIGHT_BAND.x, self.RIGHT_BAND.y - self.BAND_HEIGHT/2, self.BAND_HEIGHT, self.BAND_HEIGHT)
        self.RIGHT_BOTTOM_CIRCLE    = pygame.Rect(self.RIGHT_BAND.x, self.RIGHT_BAND.y + self.BAND_LENGTH - self.BAND_HEIGHT/2, self.BAND_HEIGHT, self.BAND_HEIGHT)
 
        self.DISK_MASS = 10
        self.STRIKER_MASS = 20

        self.screen     = pygame.display.set_mode(self.SCREEN_SIZE)
        self.score      = 0
        self.font       = pygame.font.Font(None, self.BOARD_THICKNESS)
        self.striker_in_hole = False
        self.white_in_hole = False
        self.black_in_hole = False
        self.queen_in_hole = False
        self.queen_state = 0
        self.foul = False
 
    def draw_holes(self):
 
        left_top_hole      = pygame.draw.circle(self.screen, self.BLACK, [self.ARENA_X + self.HOLE_RADIUS, self.ARENA_Y + self.HOLE_RADIUS], self.HOLE_RADIUS)
        left_bottom_hole   = pygame.draw.circle(self.screen, self.BLACK, [self.ARENA_X + self.HOLE_RADIUS, self.ARENA_Y + self.ARENA_HEIGHT - self.HOLE_RADIUS], self.HOLE_RADIUS) 
        right_top_hole     = pygame.draw.circle(self.screen, self.BLACK, [self.ARENA_X + self.ARENA_WIDTH - self.HOLE_RADIUS, self.ARENA_Y + self.HOLE_RADIUS], self.HOLE_RADIUS) 
        right_bottom_hole  = pygame.draw.circle(self.screen, self.BLACK, [self.ARENA_X + self.ARENA_WIDTH - self.HOLE_RADIUS, self.ARENA_Y + self.ARENA_HEIGHT - self.HOLE_RADIUS], self.HOLE_RADIUS)
 
        self.hole_list     = [left_top_hole, left_bottom_hole, right_top_hole, right_bottom_hole]
 
    def draw_bands(self):
 
        self.top_band      = pygame.draw.rect(self.screen, self.BLACK, self.TOP_BAND, 2)
        self.bottom_band   = pygame.draw.rect(self.screen, self.BLACK, self.BOTTOM_BAND, 2)
        self.left_band     = pygame.draw.rect(self.screen, self.BLACK, self.LEFT_BAND, 2)
        self.right_band    = pygame.draw.rect(self.screen, self.BLACK, self.RIGHT_BAND, 2)
 
        self.band_length   = self.BAND_WIDTH        
 
        self.top_left_circle        = pygame.draw.ellipse(self.screen, self.RED, self.TOP_LEFT_CIRCLE)
        self.top_right_circle       = pygame.draw.ellipse(self.screen, self.RED, self.TOP_RIGHT_CIRCLE)
        self.left_top_circle        = pygame.draw.ellipse(self.screen, self.RED, self.LEFT_TOP_CIRCLE)
        self.left_bottom_circle     = pygame.draw.ellipse(self.screen, self.RED, self.LEFT_BOTTOM_CIRCLE)
        self.bottom_left_circle     = pygame.draw.ellipse(self.screen, self.RED, self.BOTTOM_LEFT_CIRCLE)
        self.bottom_right_circle    = pygame.draw.ellipse(self.screen, self.RED, self.BOTTOM_RIGHT_CIRCLE)
        self.right_top_circle       = pygame.draw.ellipse(self.screen, self.RED, self.RIGHT_TOP_CIRCLE)
        self.right_bottom_circle    = pygame.draw.ellipse(self.screen, self.RED, self.RIGHT_BOTTOM_CIRCLE)
 
        #Drawing the boundary of the above circles
        self.top_left_circle_boundary                 = pygame.draw.ellipse(self.screen, self.BLACK, self.TOP_LEFT_CIRCLE, 2)
        self.top_right_circle_boundary                = pygame.draw.ellipse(self.screen, self.BLACK, self.TOP_RIGHT_CIRCLE, 2)
        self.left_top_circle_boundary                 = pygame.draw.ellipse(self.screen, self.BLACK, self.LEFT_TOP_CIRCLE, 2)
        self.left_bottom_circle_boundary              = pygame.draw.ellipse(self.screen, self.BLACK, self.LEFT_BOTTOM_CIRCLE, 2)
        self.bottom_left_circle_boundary              = pygame.draw.ellipse(self.screen, self.BLACK, self.BOTTOM_LEFT_CIRCLE, 2)
        self.bottom_right_circle_boundary             = pygame.draw.ellipse(self.screen, self.BLACK, self.BOTTOM_RIGHT_CIRCLE, 2)
        self.right_top_circle_boundary                = pygame.draw.ellipse(self.screen, self.BLACK, self.RIGHT_TOP_CIRCLE, 2)
        self.right_bottom_circle_boundary             = pygame.draw.ellipse(self.screen, self.BLACK, self.RIGHT_BOTTOM_CIRCLE, 2)
 
        self.band_list = [self.top_band, self.bottom_band, self.left_band, self.right_band]
 
        #self.separation = sqrt((self.top_left_circle.x  - self.left_top_circle.x)**2 + (self.top_left_circle.y - self.left_top_circle.y)**2) - self.BAND_HEIGHT
 
        self.separation = [self.TOP_LEFT_CIRCLE.center[0] - self.LEFT_TOP_CIRCLE.center[0], self.TOP_LEFT_CIRCLE.center[1] - self.LEFT_TOP_CIRCLE.center[1]]
 
        radius = (sqrt(self.separation[0]**2 + self.separation[1]**2) - self.BAND_HEIGHT)/2
 
 
        hypotenuse = sqrt(self.separation[0]**2 + self.separation[1]**2)
        cos_theta  = self.separation[0]/hypotenuse
        sin_theta  = self.separation[1]/hypotenuse
 
        #Drawing the tangent circles
        self.top_left_tangent_circle     = pygame.draw.ellipse(self.screen, self.BLACK, [self.LEFT_TOP_CIRCLE.center[0] + hypotenuse*cos_theta/2 - radius, self.LEFT_TOP_CIRCLE.center[1] + hypotenuse*sin_theta/2 - radius, 2.5*radius, 2.5*radius],2)   
        self.bottom_left_tangent_circle  = pygame.draw.ellipse(self.screen, self.BLACK, [self.BOTTOM_LEFT_CIRCLE.center[0] - hypotenuse*cos_theta/2 - radius, self.BOTTOM_LEFT_CIRCLE.center[1] + hypotenuse*sin_theta/2 - radius, 2.5*radius, 2.5*radius],2)
        self.bottom_right_tangent_circle = pygame.draw.ellipse(self.screen, self.BLACK, [self.BOTTOM_RIGHT_CIRCLE.center[0] + hypotenuse*cos_theta/2 - radius, self.BOTTOM_RIGHT_CIRCLE.center[1] + hypotenuse*sin_theta/2 - radius, 2.5*radius, 2.5*radius],2)
        self.top_right_tangent_circle    = pygame.draw.ellipse(self.screen, self.BLACK, [self.RIGHT_TOP_CIRCLE.center[0] - hypotenuse*cos_theta/2 - radius, self.RIGHT_TOP_CIRCLE.center[1] + hypotenuse*sin_theta/2 - radius, 2.5*radius, 2.5*radius],2)
 
        #Drawing the foul lines          
        line_length            =   self.BAND_LENGTH/2
        self.top_left_line     =   pygame.draw.line(self.screen, self.BLACK, self.top_left_tangent_circle.center, [self.top_left_tangent_circle.center[0] - sin_theta*line_length, self.top_left_tangent_circle.center[1] + cos_theta*line_length], 1)       
        self.top_right_line    =   pygame.draw.line(self.screen, self.BLACK, self.top_right_tangent_circle.center, [self.top_right_tangent_circle.center[0] + sin_theta*line_length, self.top_right_tangent_circle.center[1] + cos_theta*line_length], 1)       
        self.bottom_left_line  =   pygame.draw.line(self.screen, self.BLACK, self.bottom_left_tangent_circle.center, [self.bottom_left_tangent_circle.center[0] - sin_theta*line_length, self.bottom_left_tangent_circle.center[1] - cos_theta*line_length], 1)       
        self.bottom_right_line =   pygame.draw.line(self.screen, self.BLACK, self.bottom_right_tangent_circle.center, [self.bottom_right_tangent_circle.center[0] + sin_theta*line_length, self.bottom_right_tangent_circle.center[1] - cos_theta*line_length], 1)       
 
        #Drawing the foul arcs
        pygame.draw.arc(self.screen, self.BLACK, [self.top_left_tangent_circle.center[0] - sin_theta*line_length - 0.4*line_length, self.top_left_tangent_circle.center[1] + cos_theta*line_length - 0.4*line_length, line_length/2, line_length/2], 1.25*math.pi, 2.25*math.pi, 1)
        pygame.draw.arc(self.screen, self.BLACK, [self.bottom_left_tangent_circle.center[0] - sin_theta*line_length - 0.4*line_length, self.bottom_left_tangent_circle.center[1] - cos_theta*line_length - 0.1*line_length, line_length/2, line_length/2], 1.75*math.pi, 2.75*math.pi, 1)
        pygame.draw.arc(self.screen, self.BLACK, [self.top_right_tangent_circle.center[0] + sin_theta*line_length - 0.1*line_length, self.top_right_tangent_circle.center[1] + cos_theta*line_length - 0.4*line_length, line_length/2, line_length/2], 2.75*math.pi, 3.75*math.pi, 1)
        pygame.draw.arc(self.screen, self.BLACK, [self.bottom_right_tangent_circle.center[0] + sin_theta*line_length - 0.1*line_length, self.bottom_right_tangent_circle.center[1] - cos_theta*line_length - 0.1*line_length, line_length/2, line_length/2], 2.25*math.pi, 3.25*math.pi, 1)
 
    def makeDisks(self):
 
        #Disk_List contains all the Disks (Carrom Men & Striker)  
        self.disk_list = pygame.sprite.Group()
        '''
        for i in range(self.DISK_NUMBER):
 
            disk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS)
            self.disk_list.add(disk)
        '''
        # Position all the Carrom Men in the Centre Circle
        self.makeCarromMen()
 
        # Add Striker to the Board
        self.striker = Striker(self, self.GREEN, self.STRIKER_RADIUS, self.STRIKER_MASS, True)
        self.disk_list.add(self.striker)
 
 
    def makeCarromMen(self):
 
        # Positioning Disks on Vertical Line
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - tempDisk.radius), (self.BOARD_CENTER[1] - 5*tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - tempDisk.radius), (self.BOARD_CENTER[1] - 3*tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - tempDisk.radius), (self.BOARD_CENTER[1] + 1*tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - tempDisk.radius), (self.BOARD_CENTER[1] + 3*tempDisk.radius))
        self.disk_list.add(tempDisk)
 
        # Positioning Disks on -60 degrees line
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 2*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - 2*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 2*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] + 2*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
 
        #Positioning Disks on +60 degrees line
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 2*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] + 2*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 2*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - 2*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.SANDY_BROWN, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(60)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
 
        # Positioning remaining 6 Disks
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(60)) - tempDisk.radius),(self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(30)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(60)) - tempDisk.radius),(self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(30)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30)) - tempDisk.radius),(self.BOARD_CENTER[0] - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(60)) - tempDisk.radius),(self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(30)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
        tempDisk = Disk(self, self.BLACK, self.DISK_RADIUS,self.DISK_MASS)
        tempDisk.set_pos((self.BOARD_CENTER[0] - 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(60)) - tempDisk.radius),(self.BOARD_CENTER[0] + 4*tempDisk.radius*math.cos(math.radians(30))*math.cos(math.radians(30)) - tempDisk.radius))
        self.disk_list.add(tempDisk)
 
        self.queen = Disk(self, self.VIOLET_RED, self.DISK_RADIUS,self.DISK_MASS)
        self.queen.set_pos((self.BOARD_CENTER[0] - self.queen.radius), (self.BOARD_CENTER[1] - self.queen.radius))
        self.disk_list.add(self.queen)
 
    def is_in_region(self, pos_x, pos_y, start_x, start_y, end_x, end_y):
 
        if pos_x >= start_x and pos_x <= end_x:
            if pos_y >= start_y and pos_y <= end_y:
                return True
 
        return False 
 
 
 
    '''

    This is the function that checks for collision between the two disks (passed as parameters)
    It uses the sprite.CollideCircle method
    It uses Momentum Conservation (keeping masses equal)

    '''
 
    def collideDisk(self,self_disk, other_disk):
 
        if pygame.sprite.collide_circle(self_disk, other_disk):
 
            # Making direction vectors, based on position of two disks
            normal_vector       = [self_disk.rect.center[0] - other_disk.rect.center[0], self_disk.rect.center[1] - other_disk.rect.center[1]]
            unit_normal_vector  = dot(normal_vector, 1/self.mod(normal_vector))
            unit_tangent_vector = [-unit_normal_vector[1] , unit_normal_vector[0]]
 
            '''
            This has been added to remove the bug that happens when two disks overlap, and are unable to pry apart
            The solution is: To separate the disks (along the normal line), by the overlapped distance, and then do the reflection jobs
            '''
            overlap = self_disk.radius + other_disk.radius - self.mod(normal_vector)
            self_disk.rect.x    += self.next_int(overlap*unit_normal_vector[0]/2)
            other_disk.rect.x   -= self.next_int(overlap*unit_normal_vector[0]/2)
            self_disk.rect.y    += self.next_int(overlap*unit_normal_vector[1]/2)
            other_disk.rect.y   -= self.next_int(overlap*unit_normal_vector[1]/2)
 
            # Initial speeds (along normal and tangent directions), I.e. Before the collision
            self_speed_initial_normal   = dot(self_disk.speed, unit_normal_vector)
            self_speed_initial_tangent  = dot(self_disk.speed, unit_tangent_vector)
            other_speed_initial_normal  = dot(other_disk.speed, unit_normal_vector)
            other_speed_initial_tangent = dot(other_disk.speed, unit_tangent_vector)
 
            # Final Tangent speeds ( = Initial tangent speeds)
            self_speed_final_tangent    = self_speed_initial_tangent
            other_speed_final_tangent   = other_speed_initial_tangent
 
            # Final Normal Speeds ( = exchanged Initial Normal Speeds, With some loss of Power)
            self_speed_final_normal     = ((self_disk.mass - other_disk.mass)*self_speed_initial_normal + 2*other_disk.mass*other_speed_initial_normal)*self.HIT_LOSS/(self_disk.mass + other_disk.mass)#other_speed_initial_normal * self.HIT_LOSS
            other_speed_final_normal    = ((other_disk.mass - self_disk.mass)*other_speed_initial_normal + 2*self_disk.mass*self_speed_initial_normal)*self.HIT_LOSS/(self_disk.mass + other_disk.mass)#self_speed_initial_normal * self.HIT_LOSS
 
            # Vector addition of Final speeds
            self_disk.speed     = add(dot(self_speed_final_normal,unit_normal_vector) , dot(self_speed_final_tangent,unit_tangent_vector))
            other_disk.speed    = add(dot(other_speed_final_normal,unit_normal_vector) , dot(other_speed_final_tangent,unit_tangent_vector))
 
            # This is to notify that the two disks have collided, hence they need not be checked again!
            self_disk.speed_changed     = True
            other_disk.speed_changed    = True
 
 
    # Returns mod of the vector (I.e. sqrt(a^2 + b^2))
    def mod(self,vect):
        return (sqrt(vect[0]*vect[0] + vect[1]*vect[1]))
 
 
    # Used for approximating floats to Integers, but excluding ZEROS
    def next_int(self,a):
 
        if a>0:
            return ceil(a)
        else:
            return floor(a)
 
 
 
    def draw_board(self):
 
 
        '''
        DRAW RECTANGLES ON THE SCREEN
        '''
        self.screen.fill(self.CREAM)
        
        #pygame.draw.rect(self.screen, brown, [i, i, i, self.BOARD_HEIGHT - 2*i])
            
        for i in range(0, self.BOARD_THICKNESS/2 + 1, 2):
            
            brown = (150 + i, 102 + i, i)
            pygame.draw.rect(self.screen, brown, [i, i, self.BOARD_WIDTH - 2*i, i])
            pygame.draw.rect(self.screen, brown, [i, i, i, self.BOARD_HEIGHT - 2*i])
            pygame.draw.rect(self.screen, brown, [self.BOARD_WIDTH - 2*i, i, i, self.BOARD_HEIGHT - 2*i])
            pygame.draw.rect(self.screen, brown, [i,self.BOARD_HEIGHT - 2*i, self.BOARD_WIDTH - 2*i, i])
        
        
 
        self.text = self.font.render("Scoreboard" , True, self.BLACK)
        self.screen.blit(self.text, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 - 60, self.BOARD_THICKNESS/2 + 30])
        self.text_1 = self.font.render("Team 1: ", True, self.BLACK)
        self.screen.blit(self.text_1, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 - 110, self.SCREEN_HEIGHT/2 - 150])
        self.text_2 = self.font.render("Team 2: ", True, self.BLACK)
        self.screen.blit(self.text_2, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 - 110, self.SCREEN_HEIGHT/2 - 100])
        
        self.text_striker =  self.font.render("Striker Vel: " + str(math.ceil(10*self.mod([self.striker.speed[0], self.striker.speed[1]])/10.0)), True, self.BLACK)
        self.screen.blit(self.text_striker, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 - 110, self.SCREEN_HEIGHT/2])


        #self.screen.blit(self.text_2, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 - 100, self.SCREEN_HEIGHT/2 - 100])
        
        pygame.draw.circle(self.screen, self.BLACK, [self.BOARD_WIDTH/2, self.BOARD_HEIGHT/2], self.MIDDLE_RING_RADIUS,1)
        pygame.draw.circle(self.screen, self.PINK, [self.BOARD_WIDTH/2, self.BOARD_HEIGHT/2], self.CENTRE_RING_RADIUS)
 
 
 
 
        self.draw_holes()
        self.draw_bands()
 
 
    def makePlayers(self):
        self.player_list = [None]*4
 
        self.player_bottom = Player(self, "bottom")
        self.player_left = Player(self, "left")
        self.player_top = Player(self, "top")
        self.player_right = Player(self, "right")
 
        self.player_list[0] = self.player_bottom
        self.player_list[1] = self.player_left
        self.player_list[2] = self.player_top
        self.player_list[3] = self.player_right
 
        self.player_index = 0
        self.current_player = self.player_list[self.player_index]
 
 
 
    # Returns TRUE if ALL disks have stopped
    def all_disks_have_stopped(self):
 
        for disk in self.disk_list:
            if self.mod(disk.speed) != 0:
                return False
 
        return True
 
    '''
    This is the main part of the game.
    This method has a while loop that keeps running continuously, until the game ends.
    The loop runs over on each frame
    '''
 
    def checkStatus(self):
 
        if self.current_player.position == "bottom" or self.current_player.position == "top":
            if self.white_in_hole == False or self.black_in_hole == True:
                self.foul = True
                print "Bottom/Top Foul"
 
        if self.current_player.position == "left" or self.current_player.position == "right":
            if self.black_in_hole == False or self.white_in_hole == True:
                self.foul = True
                print "Left/Right Foul"
 
        if self.striker_in_hole == True:
            self.foul = True 
            self.striker.speed = [0,0]   
            self.disk_list.add(self.striker)
            print "Striker foul"
 
        
        if self.queen_in_hole == True:
            self.queen_state += 1
            print self.queen_state
 
            if self.queen_state == 2:
                if self.current_player.position == "bottom" or self.current_player.position == "top":
                    if self.white_in_hole == False:
                        self.foul = True
                        self.queen_state = 0
                        self.queen_in_hole = False
                        self.queen.set_pos(self.BOARD_CENTER[0] - self.queen.radius, self.BOARD_CENTER[1] - self.queen.radius)
                        self.disk_list.add(queen)
                    else:
                        self.queen_state = 3
 
 
                elif self.current_player.position == "left" or self.current_player.position == "right":
                    if self.black_in_hole == False:
                        self.foul = True
                        self.queen_state = 0
                        self.queen_in_hole = False
                        self.queen.set_pos(self.BOARD_CENTER[0] - self.queen.radius, self.BOARD_CENTER[1] - self.queen.radius)
                        self.disk_list.add(queen)
                    else:
                        self.queen_state = 3
 
            if self.queen_state == 1:
                self.foul = False
        
        if self.foul == True:
            self.player_index = (self.player_index + 1) % 4
            self.current_player = self.player_list[self.player_index]
            mouse_pos = pygame.mouse.get_pos()
            self.striker.set_striker_pos(mouse_pos[0],mouse_pos[1])
            self.striker_in_hole = False
 
    def resetParams(self):
 
        self.white_in_hole = False
        self.black_in_hole = False
        self.striker_in_hole = False
        self.foul = False        
    
    #def draw_start_screen(self):


 
    def start_game(self):
 
        self.done = False
        self.clock = pygame.time.Clock()
 
        # Initialise the Disks on Board
        self.makeDisks()
 
        # Initialise Players
        self.makePlayers()
 
        self.state = 0
        self.number_of_blacks = 0
        self.number_of_whites = 0
 
        while not self.done:
 
            for event in pygame.event.get():
 
                # Quit Condition --- Keyboard Q
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.done = True
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 0:
                        self.state = 1
                    elif self.state == 1:
                        self.state = 2
 
            if self.all_disks_have_stopped() == True and self.state == 3:   # If the disks have stopped moving ...
                self.state = 0
 
 
                self.checkStatus()
 
                if self.number_of_whites == 9 or self.number_of_blacks == 9:
                    self.done = True
 
 
                self.resetParams()
 
 
                #if event.type == pygame.MOUSEBUTTONDOWN:
                #   self.state = 1
 
            #self.striker_pos = [self.striker.rect.x + self.STRIKER_RADIUS, self.striker.rect.y + self.STRIKER_RADIUS]
 
            self.draw_board()                   # Draw the Board on Screen
            self.disk_list.draw(self.screen)    # Draw the Disks on Screen
            self.disk_list.update()             # Update the disks' positions/speeds 
 
            for disk in self.disk_list:
                disk.speed_changed = False      # Reset the speed_changed values before the loop repeats
 
 
 
            # Display all the changes onto screen
            pygame.display.flip()
 
            # Method for limiting Frame rate, by limiting how many times does the loop run in a second
            self.clock.tick(self.FPS)
 
        self.endGame()
        pygame.display.flip()
        #pygame.quit()
 
    def endGame(self):
 
        self.done = qTrue
        self.score = 0
 
        if self.number_of_whites == 9:
 
            for disk in self.disk_list:
                if disk.color == self.BLACK:
                    self.score = self.score + 1
 
            #self.text_1 = self.font.render("Player 1 and 3: ", True, self.BLACK)
            #self.screen.blit(self.text_1, [self.SCREEN_WIDTH - 150, 150])
            self.text_3 = self.font.render(str(self.score), True, self.BLACK)
            self.screen.blit(self.text_3, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30 , self.SCREEN_HEIGHT/2 - 150])
            self.text_4 = self.font.render("0", True, self.BLACK)
            self.screen.blit(self.text_4, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30, self.SCREEN_HEIGHT/2 - 100])
            #self.text_5 = self.font.render("Team 1 Wins!", True, self.BLACK)
            #self.screen.blit(self.text_5, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30, self.SCREEN_HEIGHT/2 + 100])
                       
           
 
        elif self.number_of_blacks == 9:
 
            for disk in self.disk_list:
                if disk.color == self.SANDY_BROWN:
                    self.score = self.score + 1
            
            self.text_3 = self.font.render(str(self.score), True, self.BLACK)
            self.screen.blit(self.text_3, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30, self.SCREEN_HEIGHT/2 - 100])
            sqelf.text_4 = self.font.render("0", True, self.BLACK)
            self.screen.blit(self.text_4, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30, self.SCREEN_HEIGHT/2 - 150])
            #self.text_5 = self.font.render("Team 2 Wins!", True, self.BLACK)
            #self.screen.blit(self.text_5, [self.BOARD_WIDTH + (self.SCREEN_WIDTH - self.BOARD_WIDTH)/2 + 30, self.SCREEN_HEIGHT/2 + 100])
             
            
            
        self.state = -1
 
 
 
 
    def run(self):
 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_game()
 
        return True
 
def main():
 
    game = Carrom()
    while game.run():
        pass
 
if __name__ == '__main__':
    main()
 
