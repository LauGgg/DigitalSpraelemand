#http://pyax-12.readthedocs.io/en/latest/index.html
from pyax12.connection import Connection
import time

class Emu():
    """Klasse til at kontrollere Dynamixel AX12 actuators"""
    sc = Connection(port="/dev/ttyUSB0", baudrate=1000000)
    # sc = Connection(port="COM12", baudrate=1000000)

    def __init__(self):
        pass

    def start(self):
        """Metode til at finde USB-porten, fx COM12 på Win, ttyUSB0 på linux"""
        #sc = Connection(port="/dev/ttyUSB0", baudrate=57600)
        #sc = Connection(port="/dev/ttyUSB0", baudrate=1000000)
        #sc = Connection(port="COM12", baudrate=1000000)
        Emu.sc.flush()

    def scanUnits(self):
        """Scanner dynamixel motorer og returnere deres id'er i en liste"""
        ids = Emu.sc.scan()
        return ids

    def readDxl(self,ID):
        """Printer oplysninger motoren med ID"""
        Emu.sc.flush()
        Emu.sc.pretty_print_control_table(ID)

    def jointMode(self,ID):
        """Skifter motoren med ID til joint mode"""
        Emu.sc.set_cw_angle_limit(ID,0,False)
        Emu.sc.set_ccw_angle_limit(ID,1023,False)

    def wheelMode(self,ID):
        """Skifter motoren med ID til wheelmode"""
        Emu.sc.set_ccw_angle_limit(ID,0,False)
        Emu.sc.set_cw_angle_limit(ID,0,False)

    def moveJoint(self, ID, position):
        """Flytter motoren med ID til position"""
        Emu.sc.goto(ID, position, speed=512, degrees=True)
        time.sleep(1)

    def moveWheel(self,ID, speed):
        """Starter en motor i wheelmode med hastigheden speed"""
        if speed < 0:
            if speed < -1024:
                speed = 2047
            else:
                speed = 1023 + -speed
        else:
            if speed > 1023:
                speed = 1023
        Emu.sc.flush()
        Emu.sc.goto(ID, 0, int(speed), degrees=False)

    def stop(self):
        """Lukker forbindelsen gennem USB-porten til dynamixlerne"""
        Emu.sc.close()

    def getPos(self, ID):
        """Returnere motoren med ID's position"""
        position = Emu.sc.get_present_position(ID, True)
        return position