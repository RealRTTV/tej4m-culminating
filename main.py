from RPi.GPIO import setmode, BCM, setup, OUT, PWM
from time import sleep

SERVO_PIN = 23

def rotate(pwm, angle):
    dc = 5.2 * angle / 110.0 + 5.0
    pwm.ChangeDutyCycle(dc)
    print(f"Moving to {angle} (internal = {dc})")
    sleep(2.5)

setmode(BCM)
setup(SERVO_PIN, OUT)

def main():
    pwm = PWM(SERVO_PIN, 50)
    pwm.start(0)
    while True:
        rotate(pwm, 90)
        rotate(pwm, -10)
    pwm.stop(0)

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
