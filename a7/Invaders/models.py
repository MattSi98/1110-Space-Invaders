"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Matthew Simon mls498 Nicholas Robinson nar73
12/3/17
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.

class dLine(GPath):
    """
    A class to represent the defense line.
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW dLine
    def __init__(self, points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                 linewidth = 2, linecolor = 'grey'):
        """
        Initializes a GPath object.
        
        Parameter points: the two points the line will go between
        Precondition: list of x/y values like [x1,y1,x2,y2] that are int types
        Parameter linewidth: the width of the line in pixels
        Precondition: linewidth is an int
        Parameter linecolor: the color of the line
        Precondition: a valid color (RGB,CMYK,colormodel,etc.)
        """
        super().__init__(points = points,
                         linewidth = linewidth, linecolor = linecolor)
        
    
class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _dead = determines if the ship is dead[Boolean]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getX(self):
        """
        Returns the ship's x attribute value.
        """
        return self.x
    
    def getY(self):
        """
        Returns the ship's y attribute value.
        """
        return self.y
    
    def setDead(self):
        self._dead = True
        
    def getDead(self):
        return self._dead
        
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x = GAME_WIDTH/2 , y = SHIP_HEIGHT/2 + SHIP_BOTTOM ,
                 source = 'ship.png',dead=False):
        """
        Initilializes a ship object.
        
        Parameter x: the x value for the center of the ship
        Precondition: x is a float or an int
        Parameter y: the y value for the center of the ship
        Precondition: y is a float or an int
        Parameter source: the image file for the ship - what it looks like
        Precondition: source is a valid png file
        Parameter dead: boolean that tells you if the ship is dead or not
        Precondition: dead is a boolean
        Parameter width: the width of the ship 
        Precondition: width is a float 
        Parameter height: the height of the ship 
        Precondition: height is a float 
        """
        super().__init__(x = x , y = y , width = SHIP_WIDTH ,
                         height = SHIP_HEIGHT, source = source)
        self._dead = dead
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with this ship.
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        fourCorners = bolt.findBoltCorners()
        for x in fourCorners:
            if self.contains(x) and not bolt.getSBolt():
                return True
            
    def moveShipRight(self, movement):
        """
        This method moves the ship right by changing its x attribute value.
        
        Parameter movement: the amount to move the ship
        Precondition: movment is an int (plus or minus SHIP_MOVEMENT)
        """
        self.x = self.x + movement
        if self.x + SHIP_WIDTH/2 > GAME_WIDTH:
            self.x = GAME_WIDTH - SHIP_WIDTH/2
            
    def moveShipLeft(self, movement):
        """
        This method moves the ship left by changing its x attribute value.
        
        Parameter movement: the amount to move the ship
        Precondition: movment is an int (plus or minus SHIP_MOVEMENT)
        """
        self.x = self.x - movement
        if self.x - SHIP_WIDTH/2 < 0:
            self.x = 0 + SHIP_WIDTH/2
 

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def moveLeft(self):
        """
        This method moves the alien left by changing its x attribute value,
        determined by the const ALIEN_H_WALK.
        """
        self.x-= ALIEN_H_WALK
        
    def moveDown(self):
        """
        This method moves the alien down by changing its y attribute value,
        determined by the const ALIEN_V_WALK.
        """
        self.y-=ALIEN_V_WALK
    
    def moveRight(self):
        """
        This method moves the alien right by changing its x attribute value,
        determined by the const ALIEN_H_WALK.
        """
        self.x+=ALIEN_H_WALK
    
    def getX(self):
        """
        Returns the x attribute value of the alien.
        """
        return self.x
    
    def getY(self):
        """
        Returns the y attribute value of the alien.
        """
        return self.y
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x = (ALIEN_H_SEP + ALIEN_WIDTH/2) ,
                 y = (GAME_HEIGHT - (ALIEN_CEILING + ALIEN_HEIGHT/2)),
                 source = 'alien1.png'):
        """
        Initiliaizes an alien object.
        
        Parameter x: the x value for the center of the alien
        Precondition: x is a float or an int
        Parameter y: the y value for the center of the alien
        Precondition: y is a float or an int
        Parameter source: the image file for the alien - what it looks like
        Precondition: source is a valid png file
        Parameter width: the width of the alien
        Precondition: width is a float 
        Parameter height: the height of the alien
        Precondition: height is a float 
        """
        super().__init__(x = x , y = y , width = ALIEN_WIDTH,
                         height = ALIEN_HEIGHT, source = source)
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        fourCorners = bolt.findBoltCorners()
        for x in fourCorners:
            if self.contains(x) and bolt.getSBolt():
                return True 
            

class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _SBolt: determines whether the bolt is from the ship
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def getBoltVelocity(self):
        """
        Returns the _velocity attribute value of the bolt.
        """
        return self._velocity
    
    def moveBoltShip(self):
        """
        This method moves a bolt upward (because it was fired from the ship),
        it does this by changing the y attribute value of the bolt.
        """
        self.y += self._velocity
        
    def moveBoltAlien(self):
        """
        This method moves a bolt downward
        (because it was fired from the aliens),
        it does this by changing the y attribute value of the bolt.
        """
        self.y-=self._velocity
        
    def getSBolt(self):
        """
        Returns the _SBolt attribute value of the bolt.
        """
        return self._SBolt
    
    def getY(self):
        """
        Returns the y attribute value of the bolt.
        """
        return self.y
    
    def getX(self):
        """
        Returns the x attribute value of the bolt.
        """
        return self.x
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,ship,width=BOLT_WIDTH,height=BOLT_HEIGHT,
                 speed=BOLT_SPEED, lcolor = 'red',fcolor= 'red'):
        """
        Inilitalizes a bolt object.
        
        Parameter x: the x value for the center of the bolt
        Precondition: x is a float or an int
        Parameter y: the y value for the center of the bolt
        Precondition: y is a float or an int
        Parameter ship: determines if the ship shot the bolt(True)
        Precondition: Boolean 
        Parameter width: the width of the bolt 
        Precondition: width is a float 
        Parameter height: the height of the bolt
        Precondition: height is a float
        Parameter speed: how many pixels the bolt will travel each update
        Precondition: speed is an int
        Parameter lcolor: the line color
        Precondition: a valid color (RGB,CMYK,colormodel,etc.)
        Parameter fcolor: the fill color 
        Precondition: a valid color (RGB,CMYK,colormodel,etc.)
        """
        super().__init__(x=x,y=y,width =width, height = height,
                         fillcolor=fcolor)
        self._SBolt = ship
        self.linecolor = 'red'
        self._velocity = speed
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def findBoltCorners(self):
        """
        Returns the four corners of a bolt object as a list of the tuples
        of (x,y).
        ie [(x1,y1),(x2,y2),(x3,y3),(x4,y4)] 
        This method finds the four corners of a bolt object in coordinate
        form (x,y).
        """
        rightX = self.getX() + BOLT_WIDTH/2
        leftX = self.getX() - BOLT_WIDTH/2
        topY = self.getY() + BOLT_HEIGHT/2
        botY = self.getY() - BOLT_HEIGHT/2
        # corners are (rightX,topY), (leftX,topY), (rightX,boty), (leftX, botY)
        corners = []
        topRight =(rightX, topY)
        topLeft = (leftX, topY)
        botRight = (rightX, botY)
        botLeft = (leftX, botY)
        corners.append(topRight)
        corners.append(topLeft)
        corners.append(botRight)
        corners.append(botLeft)
        return corners
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE