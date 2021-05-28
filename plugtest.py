import pigpio
import time

pi = pigpio.pi()
pi.set_mode(20, pigpio.OUTPUT)
pi.set_mode(21, pigpio.INPUT)
pi.set_pull_up_down(21, pigpio.PUD_UP)

pi.write(20, 0)
time.sleep(1)
print(pi.read(21))
