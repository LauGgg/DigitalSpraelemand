from EmuControl2 import Emu
import time

emu = Emu()
emu.start()
ids = emu.scanUnits()
idList = []
for id in ids:
    idList.append(id)
    print(id)
for id in idList:
    emu.jointMode(id)
    emu.moveJoint(id, 0)

def move(n, moveDegrees):
    emu.moveJoint(idList[n], moveDegrees )

def end():
    emu.stop()
