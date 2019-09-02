"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Matthew Simon mls498 Nicholas Robinson nar73
12/3/17

Citation:
We used the file arrows.py created by Walker M. White (wmw2), as a reference to
figure out how to move our ship with the arrow keys.  We also used this input style
to fire bolts.

We used the file pryo.py created by Walker M. White (wmw2), as a reference to
figure out how to delete bolts from the list.
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)
class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        
        
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
      
        _right:  determines whether or not the aliens should be going right or
        left
        _boltTime: amount of time since last ship bolt has been fired [float]
        _steps: the amount of steps since the alien wave last fired [int]
        _score: keeps track of the amount of aliens you've killed [int]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
           """
           Returns the _ship attribute values (will be a ship object).
           """
           return self._ship
        
    def dead(self):
        """
        Returns a boolean
        Determines if the ship has been shot.
        """
        return self._ship.getDead()
    
    def getLives(self):
        """
        Returns the _lives attribute valuee.
        """
        return self._lives
    
    def getShip(self):
        """
        Returns the _ship attribute values (will be a ship object).
        """
        return self._ship

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes all of the attributes of wave.
        Therefore wave makes a new group of aliens, sets time to 0, makes a ship,
        sets the edge value, makes an empty list for bolts, sets the ship lives, etc. 
        """
        self._newAlienGroup()
        self._time = 0
        self._edge = ALIEN_H_SEP
        self._right =True
        self._ship = Ship()
        self._bolts = []
        self._boltTime = 0
        self._steps =0
        self._lives=SHIP_LIVES
        self._dLine = dLine()
        self._score = GLabel(text='Score: 0', halign = 'center',
                            valign = 'middle',
                            font_size = '25', x = SCOREX, y = SCOREY,
                            linecolor = 'black',
                            font_name = 'ComicSans.ttf')
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,time,input, view):
        """
        Update method is responsible for "playing" the game.
        This method does all of the work.
        This is looped through while the game is being played.
        
        Main functions: movment fo the shio, movement of the aliens,
        firing of bolts from aliens and from the ship,deleting bolts,
        getting keyboard input, and checking for collisions
        
        Parameter time: the update speed (game time)
        Preconditon: time is a float
        Parameter input: the input from the keyboard (inherited, but must be
        passed to be used)
        Preconditon: input is a valid keyboard input
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        self.fireBolt(input)
        self.whichWay(view,time)
        self.moveShip(input)
        self.moveBolt()
        self.offScreenBolt()
        self.collisions()
        self._updateText()
        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def drawWave(self, view):
        """
        Draws Alien wave, Ship, Defense line, and Bolts to the GView
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        self._drawAliens(view)
        self._drawShip(view)
        self._drawDline(view)
        self._drawBolts(view)
        self._score.draw(view)
        
    # HELPER METHODS FOR COLLISION DETECTION, movement, Bolt function, and anythign else needed
    def more1Life(self):
        """
        Returns a boolean True/Flase if the _lives attribute value > 0.
        """
        return self._lives >0
    
    def remakeShip(self):
        """
        This method calls the ship constructor, to make a new ship object.
        """
        self._ship = Ship()
    
    def noAliens(self):
        """
        Returns a boolean, True if all alieans are destoryed, false otehrwise.
        """
        no_aliens =True
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if isinstance(self._aliens[x][y],Alien):
                    no_aliens =False
        return no_aliens
            
    def offScreenBolt(self):
        """
        This method deletes a bolt if it goes off the screen 
        """
        counter =0
        list_len = len(self._bolts)
        while counter < list_len:
            bolt = self._bolts[counter]
            if bolt.getY()>=BOLT_OFF_SCREEN_TOP or bolt.getY()<=BOLT_OFF_SCREEN_BOTTOM:
                self._bolts.pop(counter)
                list_len-=1
            else:
                counter+=1

    def collisions(self):
        """
        Determines if the ship has been shot by aliens or if the aliens have
        been shot by the ship.
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                alien = self._aliens[x][y]
                if type(alien) == Alien:
                    counter =0
                    list_len = len(self._bolts)
                    while counter < list_len:
                        bolt = self._bolts[counter]
                        if alien.collides(bolt):
                            self._aliens[x][y]= None
                            self._bolts.pop(counter)
                            list_len-=1
                            shot = Sound('pop2.wav')
                            shot.play()
                        else:
                            counter+=1
        counter2 =0
        list_len=len(self._bolts)
        while counter2 < list_len:
            boltA = self._bolts[counter2]
            if type(self._ship) == Ship:
                if self._ship.collides(boltA):
                    shot = Sound('pop1.wav')
                    shot.play()
                    self._lives-=1
                    self._bolts.pop(counter2)
                    list_len-=1
                    self._ship.setDead()
                else:
                    counter2+=1
                
    def destoryBolts(self):
        """
        sets the attribute _bolts to an empty list
        """
        self._bolts =[]
    
    def defenseBreach(self):
        """
        Returns whether or not the aliens have passed the defense line
        This method checks to see if the bottom most alien breaches the defense line.
        """
        bottom_list =[]
        lowest_y =GAME_HEIGHT
        breach =False
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                alien = self._aliens[x][y]
                if isinstance(alien,Alien):
                    if alien.getY() < lowest_y:
                        lowest_y = alien.getY()    
        if lowest_y - ALIEN_HEIGHT/2 <= DEFENSE_LINE:
            breach = True
        return breach
                        
    def alienFireBolt(self):
        """
        This method finds the lowest alien in each col,
        and randomly chooses one of them to fire, the fire rate is also randomly chosen (between 1-BOLT_RATE)
        """
        self._steps+=1
        shoot = random.randint(0,BOLT_RATE)
        if self._steps >= shoot :
            bottom_list =[]
            for col in range(len(self._aliens[0])):
                lowest_y =GAME_HEIGHT
                temp_alien = None 
                for row in range(len(self._aliens)):
                    temp = self._aliens[row][col]
                    if isinstance(temp,Alien):
                        if temp.getY() < lowest_y:
                            temp_alien= temp
                if isinstance(temp_alien,Alien):            
                    bottom_list.append(temp_alien)
            x = random.randint(0,len(bottom_list)-1)
            shooter = bottom_list[x]  
            newBolt = Bolt(shooter.getX(),shooter.getY()-BOLT_START_ALIEN,False)
            self._bolts.append(newBolt)
            shot =Sound('pew1.wav')
            shot.volume=.3
            shot.play()
            self._steps=0
                    
    def fireBolt(self,input):
        """
        This method determines if the 'up' arrow is pressed, if it is pressed,
        determines if the object is a ship,
        and determines if there are any other ship-fired bolts in the bolt list.
        If there are no other ship-fired bolts, and the up arrow is pressed, the ship will fire a bolt.
    
        Parameter input: the input from the keyboard (inherited, but must be passed to be used)
        Preconditon: input is a valid keyboard input
        """
        x = False
        for j in range(len(self._bolts)):
            if self._bolts[j].getSBolt():
                x= True
        if input.is_key_down('up') and not x:
            newBolt = Bolt(self._ship.getX(),self._ship.getY()+BOLT_START_HEIGHT,True)
            self._bolts.append(newBolt)
            shot =Sound('pew2.wav')
            shot.play()
         
    def moveBolt(self):
        """
        This method moves teh bolts of both the aliens and the ship.
        It determines if the bolt was sot from teh ship or from teh aliens.
        If it came from the ship it moves the bolts up,
        and if it came from the aliens it moves the bolts down.
        """
        if len(self._bolts) > 0:
            for x in self._bolts:
                if x.getSBolt():
                    x.moveBoltShip()
                else:
                    x.moveBoltAlien()
    
    def moveShip(self,input):
        """
        This method moves the ship, it determines if 'left' or 'right' key is being pressed.
        It them moves the ship in the correct way.
        
        Parameter input: the input from the keyboard (inherited, but must be passed to be used)
        Preconditon: input is a valid keyboard input
        """
        if type(self._ship) == Ship:
            movement = SHIP_MOVEMENT
            if input.is_key_down('left'):
                self._ship.moveShipLeft(movement)
            if input.is_key_down('right'):
                self._ship.moveShipRight(movement)
           
    def determineRightEdge(self):
        """
        Returns rigthern most alien's x position
        """
        right =0
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if isinstance(self._aliens[x][y], Alien):
                    if self._aliens[x][y].getX() > right:
                        right = self._aliens[x][y].getX()
        return right
            
    def determineLeftEdge(self):
        """
        Returns left most alien's x position
        """
        left =GAME_WIDTH
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if isinstance(self._aliens[x][y], Alien):
                    if self._aliens[x][y].getX() <left:
                        left= self._aliens[x][y].getX()
        return left
            
    def whichWay(self,view,time):   
        """
        Determines which way the alien wave will move
        
        Determines wheter the alien wave will move to the right, down, or to the left
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        Parameter time: the update speed (game time)
        Preconditon: time is a float >= 0
        """
        right_edge =self.determineRightEdge()
        if self._right and GAME_WIDTH-right_edge<= ALIEN_H_SEP + ALIEN_HALF_WIDTH:   
            self._right = False
            self._alienMarchDown()
            self._alienMarchLeft(time)
        elif self.determineLeftEdge() <= ALIEN_H_SEP and not self._right:
            self._right = True
            self._alienMarchDown()
            self._alienMarchRight(time)
        elif self._right:
            self._alienMarchRight(time)
        elif not self._right:
            self._alienMarchLeft(time)
          
    #Hidden Methods
    def _updateText(self):
        """
        updates the text of the score object
        """
        score = self._incrementScore()
        self._score.text = 'Score: ' + str(score)
        
    def _incrementScore(self):
        """
        Returns number of aliens killed
        """
        counter = 0
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] == None:
                    counter +=1
        return counter
      
    def _alienMarchDown(self):
        """
        Moves the Alien wave down by ALIEN_V_WALK pixels.
        """
        for row in self._aliens:
            for i in row:
                if type(i) == Alien:
                    i.moveDown()
        self.alienFireBolt()
        
    def _alienMarchRight(self,time):
        """
        Moves the alien wave to the right by ALIEN_H_WALK pixels
        
        Parameter time: the update speed (game time)
        Preconditon: time is a float >= 0
        """
        self._time =  self._time + time
        if self._time > ALIEN_SPEED:
            for row in self._aliens:
                for i in row:
                    if type(i) == Alien:
                        i.moveRight() 
            self._time =0
            self.alienFireBolt()
            
    def _alienMarchLeft(self, time):
        """
        Moves the alien wave to the left by ALIEN_H_WALK pixels
        
        Parameter time: the update speed (game time)
        Preconditon: time is a float >= 0
        """
        self._time =  self._time + time
        if self._time > ALIEN_SPEED:
            for row in self._aliens:
                for i in row:
                    if type(i) == Alien:
                        i.moveLeft() 
            self._time =0
            self.alienFireBolt()
            
    def _drawBolts(self, view):
        """
        Draws the bolt to the GView.
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        if len(self._bolts) > 0:
            for x in self._bolts:
                x.draw(view)
                
    def _drawDline(self, view):
        """
        Draws the defense line.
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        self._dLine.draw(view)
        
    def _drawShip(self, view):
        """
        Draws the ship.
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        ship = self._ship
        if type(ship) == Ship:
            ship.draw(view)
        
    def _drawAliens(self, view):
        """
        Draws the aliens (all rows), draws the list _aliens.
        
        Parameter view: the game window
        Preconditon: view is a Gview object
        """
        for row in self._aliens:
            for i in row:
                if type(i) == Alien:
                    i.draw(view)
        
    def _newAlienGroup(self):
        """
        Creates ALIEN_ROWS amount of lists, each representing a row of aleins,
        which are stored in _aliens list,
        rows are ALEIN_CIELING from the top, then spaced by ALIEN_V_SEP vertically
        """
        self._aliens = []
        imageNum = 3
        for n in range(ALIEN_ROWS):
            if n%2 == 1:
                imageNum = imageNum - 1
                if imageNum < 1:
                    imageNum = 3
            if imageNum == 3:
                png = 'alien3.png'
            if imageNum == 2:
                png = 'alien2.png'
            if imageNum == 1:
                png = 'alien1.png'
            row = self._newAlienRow(y = GAME_HEIGHT - (
                (ALIEN_CEILING + ALIEN_HEIGHT/2)+((ALIEN_V_SEP+ALIEN_HEIGHT)*n)),
                                   source = png)
            self._aliens.append(row)
            
    def _newAlienRow(self,y,source):
        """
        creates a row of aliens, with ALIENS_IN_ROW amount of aliens,
        aliens are spaced horizontally by ALEIN_H_SEP
        
        Parameter y: the y separation of alien rows
        Precondition: y is a float
        Parameter source: what teh alien will look like
        Precondition: source is a valid png file
        """
        alienList = []
        for n in range(1,ALIENS_IN_ROW+1):
            alien = Alien(x = (ALIEN_H_SEP+ALIEN_WIDTH)*n, y=y, source = source)
            alienList.append(alien)
        return alienList
       
        