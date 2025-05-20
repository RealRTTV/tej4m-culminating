from RPi.GPIO import setmode, BCM, setup, OUT, PWM
from time import sleep

SERVO_PIN: int = 23

def set_target_angle(pwm: PWM, angle: float) -> None:
    dc = 5.2 * angle / 110.0 + 5.0
    pwm.ChangeDutyCycle(dc)

def rotate_to(pwm: PWM, angle: float) -> None:
    set_target_angle(pwm, angle)
    print(f"Moving to {angle} (internal = {dc})")
    sleep(2.5)

setmode(BCM)
setup(SERVO_PIN, OUT)

def main():
    pwm = PWM(SERVO_PIN, 50)
    pwm.start(0)
    while True:
        rotate_to(pwm, 90)
        rotate_to(pwm, -10)
    pwm.stop(0)

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()

