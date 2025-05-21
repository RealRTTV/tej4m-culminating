from RPi.GPIO import setmode, BCM, setup, OUT, PWM, cleanup
from time import sleep, time
from typing import List
import math

SERVO_PIN: int = 23
FULL_ANIMATION_DURATION: float = 10.0
START_RANGE_OF_MOTION: float = -10.0
END_RANGE_OF_MOTION: float = 90.0
ANIMATION_FRAMES: List[float] = []

def lerp(a: float, b: float, delta: float) -> float:
    return (b - a) * delta + a

def set_target_angle(pwm: PWM, angle: float) -> None:
    dc: float = 5.2 * angle / 110.0 + 5.0
    pwm.ChangeDutyCycle(dc)

def rotate_to(pwm: PWM, angle: float) -> None:
    set_target_angle(pwm, angle)
    print(f"Moving to {angle}")
    sleep(2.5)

def read_animation_frames_from_file(file: str) -> None:
    ANIMATION_FRAMES.clear()
    with open(file, "rb") as f:
        while (byte := f.read(1)):
            angle = lerp(START_RANGE_OF_MOTION, END_RANGE_OF_MOTION, byte / 255.0)
            ANIMATION_FRAMES.append(angle)

def main():
    read_animation_frames_from_file("animation_data.bin")

    setmode(BCM)
    setup(SERVO_PIN, OUT)

    pwm: PWM = PWM(SERVO_PIN, 50)
    pwm.start(0)
    rotate_to(pwm, 90)
    
    start_timestamp: float = time()
    while True:
        timestamp: float = time()
        duration: float = timestamp - start_timestamp
        frame: float = duration % FULL_ANIMATION_DURATION
        (frame_delta: float, frame: float) = math.modf()
        frame: int = int(frame)
        angle = lerp(ANIMATION_FRAMES[frame], ANIMATION_FRAMES[(frame + 1) % len(ANIMATION_FRAMES)], frame_delta)
        set_target_angle(pwm, angle)

    pwm.stop(0)

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
