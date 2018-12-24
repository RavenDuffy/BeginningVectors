from AsteroidsMechanics import AsteroidsMechanics

am = AsteroidsMechanics()

while am.runTitle == True:
    am.refreshScreen()

    if am.ship.checkForward() == True:
        am.ship.moveForward(.1)
    if am.ship.checkRight() == True:
        am.ship.moveRight(5)
    if am.ship.checkLeft() == True:
        am.ship.moveLeft(-5)

    am.ship.wrapChar()

    am.drawStage()
