import time
from typing import Optional, Callable, List

import pylibftdi as ftdi
import logging

logger = logging.getLogger(__name__)

class FTDIDevice:

    BAUDRATE = 38400


    def __init__(self, manufactuter, name, device_id):
        self.device = None
        self.manufactuter = manufactuter
        self.name = name
        self.device_id = device_id

    def __str__(self):
        return "{}:{}:{}".format(self.manufactuter, self.name, self.device_id)

    def open(self):
        self.device = ftdi.Device(self.device_id)
        self.device.baudrate = FTDIDevice.BAUDRATE
        result = self.device.ftdi_fn.ftdi_set_line_property(8,0,0)
        if result != 0:
            self.device = None
            raise Exception("Can't initialize device")
        self.device.open()
        # OPS = 1
        # self.device.ftdi_fn.ftdi_set_bitmode(OPS, 1)  # FIXME(Select correct bit mode)

    def close(self):
        self.device.close()
        self.device = None

    def write(self, code : int, data: List[int]=None):
        temp = bytes([code]+ data) if data is not None else bytes(code)
        self.device.write(temp)
        time.sleep(0.5)

    def read(self, nbytes) -> List[int]:
        s = self.device.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)

    @staticmethod
    def find_all_device(key: Optional[Callable] = None):
        devices = []
        dev_list = filter(lambda x: key(x[0]), ftdi.Driver().list_devices())
        for dev in dev_list:
            devices.append(FTDIDevice(*dev))
        return devices

    @staticmethod
    def find_new_device(exist_dev: List["HVDevice"], key: Optional[Callable] = None):
        devices = []
        dev_list = filter(lambda x: key(x[0]), ftdi.Driver().list_devices())
        for dev in dev_list:
            for exist in exist_dev:
                device: FTDIDevice = exist.device
                if (dev[2] != device.device_id):
                    devices.append(FTDIDevice(*dev))
        return devices