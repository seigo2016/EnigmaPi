import smbus
from util import enigma_rotary


def get_i2c_addresses():
    addresses = []
    bus = smbus.SMBus(1)
    for device in range(128):
        try:
            bus.read_byte(device)
            addresses.append(hex(device))
        except Exception as e:
            # print(e)
            pass
    print(addresses)
    return addresses

class I2CDeviceNotFoundError(Exception):
    pass


class RotaryConnectionError(Exception):
    pass


def check():
    # I2C Address Check
#    addresses = set([0x20, 0x21, 0x22, 0x48])
    detected_addresses = set(get_i2c_addresses())
    addresses = set(['0x20', '0x21', '0x22', '0x23', '0x48'])
    if addresses != detected_addresses:
        difference = addresses - detected_addresses
        print(difference)
        error_address = ""
        for i, d in enumerate(difference):
            if i != 0:
                error_address += ","
            error_address += d

        raise I2CDeviceNotFoundError(f"Module not found\n ({error_address})")

    # Rotary Status Check
    rotary = enigma_rotary.EnigmaRotary()
    # rotary_state = [None, 0, 2]
    rotary_state = rotary.get_state()
    # print(rotary_state)
    if None in rotary_state:
        raise RotaryConnectionError(
            f"Invalid Status of Rotary No.{rotary_state.index(None)+1}")

    return 0


if __name__ == '__main__':
    check()

