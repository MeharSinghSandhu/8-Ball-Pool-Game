import phylib;
import os;
import sqlite3;
from math import sqrt
import random

HEADER = """
<svg width="350" height="700" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """<line x1="0" x2="0" y2="0" y1="0" stroke="black"/>
</svg>\n"""




################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
PHYLIB_HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG= phylib.PHYLIB_DRAG ;
MAX_TIME = phylib.PHYLIB_MAX_TIME ;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS ;
FRAME_INTERVAL = 0.01;



################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
        
    def svg(self):
        color = BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)]

        return f'<circle cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{color}" />\n'
        
class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y),
        velocity (vx, vy), and acceleration (ax, ay) as arguments.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0)
        self.__class__ = RollingBall
        
    def svg(self):
        color = BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)]
        
        return f'<circle cx="{self.obj.rolling_ball.pos.x}" cy="{self.obj.rolling_ball.pos.y}" r="{BALL_RADIUS}" fill="{color}" />\n'

class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires position (x,y) as argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,  # Number not used for hole
                                      pos, None, None,
                                      pos.x, pos.y)
        self.__class__ = Hole
    def svg(self):
        return f'<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{PHYLIB_HOLE_RADIUS}" fill="black" />\n'

class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y-coordinate as argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,  # Number not used for cushion
                                      None, None, None,
                                      0.0, y)
        self.__class__ = HCushion
    def svg(self):
        y_position = "-25"  # Placeholder, adjust based on actual logic
        return f'<rect width="1400" height="25" x="-25" y="{y_position}" fill="darkgreen" />\n'

class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x-coordinate as argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,  # Number not used for cushion
                                      None, None, None,
                                      x, 0.0)
        self.__class__ = VCushion
        
    def svg(self):
        x_position = "-25"  # Placeholder, adjust based on actual logic
        return f'<rect width="25" height="2750" x="{x_position}" y="-25" fill="darkgreen" />\n'

    # add an svg method here


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg(self):
        svg_content = HEADER
        for obj in self:
            if obj is not None:
                svg_content += obj.svg()
        svg_content += FOOTER
        return svg_content
    
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                       Coordinate(0,0),
                                       Coordinate(0,0),
                                       Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                         Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) );
                    # add ball to table
                new += new_ball;
        # return table
        return new;
    
    def cueBall(self):
        for ball in self:
            if ball.obj.still_ball:
                return ball
        return None  # Or raise an exception if the cue ball is not found
################################################################################

class Database():
    def __init__(self, reset=False):
        self.db_path = "phylib.db"
        if reset and os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
 
    def createDB(self):
        cur = self.conn.cursor()
        
        # Create Ball table
        cur.execute("""CREATE TABLE IF NOT EXISTS Ball (
                        BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        BALLNO INTEGER NOT NULL,
                        XPOS FLOAT NOT NULL,
                        YPOS FLOAT NOT NULL,
                        XVEL FLOAT,
                        YVEL FLOAT);""")
                        # add not null
 
        # Create TTable table
        cur.execute("""CREATE TABLE IF NOT EXISTS TTable (
                        TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        TIME FLOAT NOT NULL);""")
 
        # Create BallTable table
        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable (
                        BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID));""")
 
        # Create Shot table
        cur.execute("""CREATE TABLE IF NOT EXISTS Shot (
                        SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID INTEGER NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID));""")
 
        # Create TableShot table
        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot (
                        TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES BallTable(TABLEID),
                        FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID));""")
 
        # Create Game table
        cur.execute("""CREATE TABLE IF NOT EXISTS Game (
                        GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME VARCHAR(64) NOT NULL);""")
 
        # Create Player table
        cur.execute("""CREATE TABLE IF NOT EXISTS Player (
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID));""")
        
        self.conn.commit()  # Commit the changes to the database
        cur.close()  # Close the cursor after executing the commands
 
 
    def readTable(self, tableID):
        # Adjust tableID according to SQL numbering
        adjusted_tableID = tableID + 1
 
        cur = self.conn.cursor()
 
        # Retrieve the time attribute for the table
        cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (adjusted_tableID,))
        table_time_data = cur.fetchone()
 
        if table_time_data is None:
            return None  # The specified TABLEID does not exist
 
        table_time = table_time_data[0]
 
        # Fetch all balls for the given table
        cur.execute("""
            SELECT b.BALLID, b.BALLNO, b.XPOS, b.YPOS, b.XVEL, b.YVEL
            FROM BallTable bt
            JOIN Ball b ON bt.BALLID = b.BALLID
            WHERE bt.TABLEID = ?
            """, (adjusted_tableID,)) # query is wrong, inner join write name like Ball.BALLID etc
 
        balls_data = cur.fetchall()
 
        # Initialize Table with standard holes and cushions
        table = Table()  # Initialize your Table object
        
        # Define holes with given positions
 
        table.time = table_time
 
 
        for ball_data in balls_data:
            _, ball_no, xpos, ypos, xvel, yvel = ball_data
            if xvel is None and yvel is None:
                table += StillBall(ball_no, Coordinate(xpos, ypos))
            else:
        # Calculate the magnitude of the velocity
                velocity_magnitude = (xvel**2 + yvel**2)**0.5
 
                if velocity_magnitude > VEL_EPSILON:
                    accx = (-xvel) / velocity_magnitude * DRAG
                    accy = (-yvel) / velocity_magnitude * DRAG
        # Assuming RollingBall can be instantiated with velocity magnitude in addition to xvel and yvel
                    table += RollingBall(ball_no, Coordinate(xpos, ypos), Coordinate(xvel, yvel), Coordinate(accx, accy))
            
 
        return table
 
        
 
        # for ball_data in balls_data:
        #     _, ball_no, xpos, ypos, xvel, yvel = ball_data
        #     # Instantiate as StillBall or RollingBall based on velocity
        #     if xvel == 0 and yvel == 0:
        #         ball = StillBall(ball_no, Coordinate(xpos, ypos))
        #     else:
        #         #Find acceleration like in a2 it is Coordinate(xvel,yel) not two seperate things
        #         ball = RollingBall(ball_no, Coordinate(xpos, ypos), xvel, yvel)
 
        #     table += ball
 
        # return table
 
    def writeTable(self, table):
        # Step 1: Insert table state into TTable
        cur = self.conn.cursor()
        cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = cur.lastrowid  # Retrieve autoincremented TABLEID
 
        for ball in table:
            # Determine if the ball is still or rolling to decide whether to add velocity
            if isinstance(ball, StillBall):
                # StillBall has no velocity
                cur.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?)
                """, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
            if isinstance(ball, RollingBall):
                # RollingBall includes velocity
                cur.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?)
                """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
              # Commit after each ball to ensure BALLID is updated
              # Retrieve autoincremented BALLID
            # Link ball to table state in BallTable
            if isinstance(ball,StillBall) or isinstance(ball, RollingBall):
                ball_id = cur.lastrowid
                cur.execute("""
                    INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?)
                """, (ball_id, table_id))
        
        self.conn.commit()  # Final commit after all inserts
        
        # Adjust TABLEID to start numbering at zero before returning
        return table_id - 1
 
    def getGame(self, gameID):
        cur = self.conn.cursor()
        # Fetch the game name
        cur.execute("SELECT GAMENAME FROM Game WHERE GAMEID = ?", (gameID,))
        gameName = cur.fetchone()[0] if cur.fetchone() else None
 
        # Fetch the player names associated with this game
        cur.execute("SELECT PLAYERNAME FROM Player WHERE GAMEID = ?", (gameID,))
        players = cur.fetchall()
 
        # Assuming two players per game for simplicity; adjust as needed
        playerNames = [player[0] for player in players]
 
        # Add check if players found are less than 2 then append None values accordingly
        while len(playerNames) < 2:
            playerNames.append(None)
 
        return (gameName, *playerNames[:2]) if gameName else None
 
 
    def setGame(self, gameName, player1Name, player2Name):
        cur = self.conn.cursor()
        # Step 1: Insert the new game
        cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = cur.lastrowid  # Get the ID of the newly inserted game
 
        # Step 2: Insert the players with the new gameID
        for playerName in [player1Name, player2Name]:
            cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, playerName))
 
        self.conn.commit()  # Commit the transaction
        return gameID
 
    def getGameID(self, gameName):
        cur = self.conn.cursor()
        cur.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,))
        result = cur.fetchone()
        return result[0] if result else None
 
    def getPlayerID(self, playerName, gameID):
        cur = self.conn.cursor()
        # It's assumed that player names are unique within a game, not across all games
        cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?", (playerName, gameID))
        result = cur.fetchone()
        return result[0] if result else None
 
    def newShot(self, gameName, playerName):
        gameID = self.getGameID(gameName)
        if gameID is None:
            raise ValueError(f"No game found with the name {gameName}")
 
        playerID = self.getPlayerID(playerName, gameID)
        if playerID is None:
            raise ValueError(f"No player found with the name {playerName} in game {gameName}")
 
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)
        """, (playerID, gameID))
        self.conn.commit()
        return cur.lastrowid
 
    def recordTableShot(self, tableID, shotID):
        """
        Records a new entry in the TableShot table linking a table state with a shot.
        
        :param tableID: The ID of the table state.
        :param shotID: The ID of the shot.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)
            """, (tableID + 1, shotID))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"An error occurred: {e}")
            # Handle the error as needed (e.g., rollback, log, raise custom exception)
 
 
 
    def close(self):
        self.conn.commit()
        self.conn.close()
        

class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        # Assuming a database instance is available in this scope as `database`
        self.database = Database()
        self.database.createDB()
 
        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1  # Adjusting gameID as per instructions
            # Retrieve existing game details from the database
            self.gameName, self.player1Name, self.player2Name = self.database.getGame(self.gameID)
        elif gameID is None and all(isinstance(name, str) for name in [gameName, player1Name, player2Name]):
            # Register a new game and players in the database
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = self.database.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("Invalid combination of arguments provided to Game constructor.")
 
 
    
    
    
 
    def shoot(self, gameName, playerName, table, xvel, yvel):
        # Assume gameID and database are accessible within this instance
 
        
       
        #shotID = self.database.newShot(gameName, playerName)
        
        for cue_ball in table:
        
            if isinstance(cue_ball, StillBall) and cue_ball.obj.still_ball.number == 0:
 
                cue_ball.type = phylib.PHYLIB_ROLLING_BALL
                xpos, ypos = cue_ball.obj.still_ball.pos.x, cue_ball.obj.still_ball.pos.y
                
                # Update cue ball to rolling state with new velocity and position
                cue_ball.obj.rolling_ball.pos.x = xpos
                cue_ball.obj.rolling_ball.pos.y = ypos
                cue_ball.obj.rolling_ball.vel.x = xvel
                cue_ball.obj.rolling_ball.vel.y = yvel
                # Assume acceleration is recalculated here
                velocity_magnitude = (xvel**2 + yvel**2)**0.5
 
                
                accx = (-xvel) / velocity_magnitude * DRAG
                accy = (-yvel) / velocity_magnitude * DRAG
                
                cue_ball.obj.rolling_ball.acc.x = accx
                cue_ball.obj.rolling_ball.acc.y = accy
        
        # Simulate movement until segment method returns None
        
        svg = []
        
 
        while True:
            copy = table
            
            start = table.time
            table = table.segment()  # Simulate next movement phase
            if table is None:
                break
            
            # Determine segment length and loop over each frame
            segment_length = int((table.time - start) / FRAME_INTERVAL)
            for frame in range(segment_length):
                frame_time = frame * FRAME_INTERVAL
 
                next_frame_table = copy.roll(frame_time)  # Roll to next frame
                
                # Update time and save the state
                next_frame_table.time = start + frame_time
                

 
                #table_id = self.database.writeTable(next_frame_table)
                
                svg.append(next_frame_table.svg())
                
                # Record in TableShot
                #self.database.recordTableShot(table_id, shotID)
                
                # Update segment_time for next iteration if needed
                
        found = False
        
        for obj in copy:
            if isinstance(obj,StillBall) and obj.obj.still_ball.number == 0:
                found = True
        
        if found == False:
            copy += StillBall(0,Coordinate( TABLE_WIDTH/2.0 + random.uniform(-3.0, 3.0),
                     TABLE_LENGTH - TABLE_WIDTH/2.0))
            
        svg.append(copy.svg())
                
        return [svg,copy]
        
   

        
        
        




#find . -name '*.svg' -delete