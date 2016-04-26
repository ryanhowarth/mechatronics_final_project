

import Claw
from time import sleep


myClaw = Claw.claw(0,7)
myClaw.getPins()

while True:
    myClaw.pickupGift()
    sleep(1)

    myClaw.dropGift()
    sleep(1)
