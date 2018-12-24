import pygame
import math
import random

class AsteroidsMechanics:
    pygame.init()

    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 32)

        self.size = self.width, self.height = 600, 400
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Asteroids")

        self.runTitle = True    # will be used for the game's title screen loop
        self.runGame = False    # will be used for the game's main screen loop
        self.runEnd = False     # will be used for the game's end screen loop

        self.score = 0          # holds the player's score

        self.ship = PlayerShip(self.WHITE, self.width, self.height, self.screen) # creates a ship object


    # should be run once an iteration to keep the game running correctly
    def drawStage(self):
        self.ship.redraw()

        self.clock.tick(60)
        pygame.display.flip()

        self.handleExit()

    # should be run once an iteration to prevent trailing
    def refreshScreen(self):
        self.screen.fill(self.BLACK)

    # ends all loops and closes the game
    def handleExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runTitle = False
                self.runGame = False
                self.runEnd = False

class PlayerShip:
    pygame.init()

    def __init__(self, colour, width, height, screen):
        self.colour = colour
        self.width = width
        self.height = height
        self.screen = screen
        self.angle = 0
        self.velocity = 0
        self.lastVector = (self.createVector(self.velocity))

        initShipPoints = [(width / 2, height / 2 - 10), (width / 2 - 7, height / 2 + 10), (width / 2 + 7, height / 2 + 10)]
        self.ship = pygame.draw.polygon(self.screen, self.colour, initShipPoints, 1)

        # keeps the coords for the centre of the ship
        self.x = width / 2
        self.y = height / 2

        # keeps the coords for the ship's points
        self.points = initShipPoints

    def redraw(self):
        self.ship = pygame.draw.polygon(self.screen, self.colour, self.points, 1)

    # checks to see if the up arrow is pressed
    def checkForward(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return True
        self.moveForwardPassive()
        return False

    # checks to see if the right arrow is pressed
    def checkRight(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            return True
        return False

    # checks to see if the left arrow is pressed
    def checkLeft(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return True
        return False

    # creates the scalar value for the last vector
    def vectorScalar(self):
        vectorDifference = None

    # move the character forward based on velocity
    def moveForwardPassive(self):
        vx, vy = self.createVector(self.velocity)
        self.changePoints(vx, vy)

    # moves the character in the direction its facing
    def moveForward(self, d):
        self.velocity += d
        if self.velocity > 5:
            self.velocity = 5
        vx, vy = self.createVector(self.velocity)
        self.changePoints(vx, vy)
        self.lastVector = (vx, vy)

    # moves the character right
    def moveRight(self, angle):
        self.getPoints((self.x, self.y), self.points, angle)

    # moves the character left
    def moveLeft(self, angle):
        self.getPoints((self.x, self.y), self.points, angle)

    # wraps the character around the screen
    def wrapChar(self):
        if (self.x < -15):
            self.changePoints(self.width + 15, 0)
        if (self.x > self.width + 15):
            self.changePoints(-(self.width + 15), 0)
        if (self.y < -15):
            self.changePoints(0, self.height + 15)
        if (self.y > self.height + 15):
            self.changePoints(0, -(self.height + 15))

    # create a vector from the current ship pos, scaled by d
    # rotated to make the top the forward facing side
    def createVector(self, d):
        vx = math.cos(self.angle - math.radians(90))
        vy = math.sin(self.angle - math.radians(90))
        return (vx * d, vy * d)

    # updates the current character's points
    def changePoints(self, dx, dy):
        for p in range(len(self.points)):
            x, y = self.points[p]
            self.points[p] = (x + dx, y + dy)
        self.x += dx
        self.y += dy

    # updates the current polygon points to the new points
    def getPoints(self, centre, points, angle):
        angle = math.radians(angle) # converts the angle to radians
        self.angle += angle
        if self.angle >= math.pi * 2:
            self.angle = 0

        s = math.sin(angle)
        c = math.cos(angle)
        cx, cy = centre

        counter = 0
        for p in points:
            # moves the point to the origin
            x, y = p
            x -= cx
            y -= cy

            # rotate the point
            nx = x * c - y * s
            ny = x * s + y * c

            # moves the point back
            x = nx + cx
            y = ny + cy
            self.points[counter] = (x, y)
            counter += 1

    # returns x
    def getX(self):
        return self.x

    # returns y
    def getY(self):
        return self.y