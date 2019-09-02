"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There 
is no need for any additional classes in this module.  If you need more classes, 99% of 
the time they belong in either the wave module or the models module. If you are unsure 
about where a new class should go, post a question on Piazza.

Matthew Simon mls498 Nicholas Robinson nar73
12/3/17

Citations (all):
We used code written by Walker White for the helper function _determineState, as well
as the instance attribute _lastkeys, these came from the file states.py

We used the file arrows.py created by Walker M. White (wmw2), as a reference to
figure out how to move our ship with the arrow keys.  We also used this input style
to fire bolts.

We used the file pryo.py created by Walker M. White (wmw2), as a reference to
figure out how to delete bolts from the list.
"""
import cornell
from consts import *
from game2d import *
from wave import *
from models import *
# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py
class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification for the
    method update.
    
    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be 
    documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _lastkeys: the number of keys pressed last frame
                   [int >= 0]
                   
        _win: a boolean, defaulted to False, if True you won(destroyed all aliens).
        
    """
    # DO NOT MAKE A NEW INITIALIZER!
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _text) saying that the user should press to play a game.
        """
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._lastkeys = 0
        self._wave = None
        self._win= False
        self._text = GLabel(text='Press s to start game', halign = 'center',
                            valign = 'middle',
                            font_size = '40', x = 400, y = 300,
                            linecolor = 'green',
                            font_name = 'ComicSans.ttf')
        mysong = Sound('Changing Tides.wav')
        mysong.volume =.7
        mysong.play()
        
    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these 
        does its own thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the 
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen. 
        The application switches to this state if the state was STATE_INACTIVE in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._determineState()
        if self._state == STATE_NEWWAVE:
            self.newWaveState()
        if self._state == STATE_ACTIVE:
            self.stateActive(dt)
        if self._state == STATE_PAUSED:
            self._wave.destoryBolts()
            if self._wave.more1Life():
                self._determineState()
            else:
                self.determineComplete()
        if self._state == STATE_CONTINUE:
            self._wave.remakeShip()
            self._state = STATE_ACTIVE
            self._text =None
        if self._state == STATE_COMPLETE:
            if self._win:
                self.winScreen()
            else:
                self.loseScreen()
                
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._wave.drawWave(self.view)
        if self._state== STATE_PAUSED:
            self._text.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._text.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def winScreen(self):
        """
        This method creates the message you see when you win, and sets
        that GLabel to the _text attribute 
        """
        self._text = GLabel(text='You won!', halign = 'center',
            valign = 'middle',
            font_size = '40', x = 400, y = 300,
            linecolor = 'green',
            font_name = 'ComicSans.ttf')
        
    def loseScreen(self):
        """
        This method creates the message you see when you lose, and sets
        that GLabel to the _text attribute.
        """
        self._text = GLabel(text='You lost the game: how pathetic\nUninstall the game', halign = 'center',
                            valign = 'middle',
                            font_size = '40', x = 400, y = 300,
                            linecolor = 'green',
                            font_name = 'ComicSans.ttf')
        
    def stateActive(self,dt):
        """
        Determines what should happen while self._state = STATE_ACTIVE
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        
        if self._wave.dead():
            self.resume()
            self._state =STATE_PAUSED
        elif self._wave.noAliens():
            self._win =True
            self._state = STATE_COMPLETE
        elif self._wave.defenseBreach():
            
            self._state = STATE_COMPLETE
        else:
            self._wave.update(dt,self.input, self.view)
        
    def resume(self):
        """
        This method creates the message you see when you lose a life and the
        game is paused.  It sets that GLabel to teh _text attribute.
        It also sets _lastKeys to zero so that _determinestate will work
        """
        self._lastkeys = 0
        self._text = GLabel(
            text='Lives left: '+str(self._wave.getLives())+'\nPress any key to resume the game',
                            halign = 'center',
                            valign = 'middle',
                            font_size = '40', x = 400, y = 300,
                            linecolor = 'green',
                            font_name = 'ComicSans.ttf')
        
    def newWaveState(self):
        """
        This method clears any messages on the screen, and creates a new wave of aliens.
        It then sets the state to active state.
        """
        self._text = None
        self._wave = Wave()
        self._state= STATE_ACTIVE
         
    def determineComplete(self):
        """
        This method determines if you win or lose. If you haven't destoryed
        all of the aliens, it doesn't update _win therefore you lose,
        otherwise it updates _win adn you will win
        """
        if self._wave.noAliens():
            self._state= STATE_COMPLETE
            self._win = True
        elif self._wave.more1Life:
            self._state= STATE_COMPLETE

    def _determineState(self):
        """
        Determines the current state and assigns it to self.state
        
        This method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        
        Citation:
        This helper function was copied from code written by Walker White 
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.lastkeys == 0
        if change:
            self._state = (self._state + 1) % NUM_STATES
        self.lastkeys= curr_keys