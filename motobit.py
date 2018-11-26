import adafruit_bus_device.i2c_device as i2c_device

class MotoBitMotor:
    FORWARD_FLAG = 0x80

    def __init__(self, device, cmd_speed, invert):
        self._device = device
        self.cmd_speed = cmd_speed
        self.invert = invert

    def __drive(self, speed):
        flags = 0
        if self.invert:
            speed = -speed
        if speed >= 0:
            flags |= MotoBitMotor.FORWARD_FLAG
        speed = int(speed / 100 * 127)
        if speed < -127:
            speed = -127
        if speed > 127:
            speed = 127
        speed = (speed & 0x7f) | flags
        with self._device:
            self._device.write(bytes([self.cmd_speed, speed]))

    def forward(self, speed):
        self.__drive(speed)

    def reverse(self, speed):
        self.__drive(-speed)

class MotoBit:
    I2C_ADDR = 0x59
    CMD_ENABLE = 0x70
    CMD_SPEED_LEFT = 0x21
    CMD_SPEED_RIGHT = 0x20

    def __init__(self, i2c, address=I2C_ADDR):
        self._device = i2c_device.I2CDevice(i2c, address)

    def enable(self):
        with self._device:
            self._device.write(bytes([MotoBit.CMD_ENABLE, 0x01]))

    def disable(self):
        with self._device:
            self._device.write(bytes([MotoBit.CMD_ENABLE, 0x00]))

    def left_motor(self, invert=False):
        return MotoBitMotor(self._device, MotoBit.CMD_SPEED_LEFT, invert)

    def right_motor(self, invert=False):
        return MotoBitMotor(self._device, MotoBit.CMD_SPEED_RIGHT, invert)