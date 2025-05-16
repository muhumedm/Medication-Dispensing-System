import lgpio

import time



# Open GPIO chip 0

CHIP = lgpio.gpiochip_open(0)



# Breadboard 1 LEDs

LED_PINS = {

    "Amlodipine Besylate": 2,

    "Azithromycin": 3,

    "Levothyroxine": 4,

    "Metformin": 14,

    "Lisinopril": 15,

    "Atorvastatin": 17,

    "Simvastatin": 18,



    # Breadboard 2 LEDs

    "Warfarin": 5,

    "Omeprazole": 6,

    "Donepezil": 12,

    "Gabapentin": 13,

    "Sertraline": 16,

    "Hydrocodone": 19,

    "Ciprofloxacin": 20

}



# Buzzers

BUZZER1_PIN = 27

BUZZER2_PIN = 21



# Claim output pins

for pin in list(LED_PINS.values()) + [BUZZER1_PIN, BUZZER2_PIN]:

    lgpio.gpio_claim_output(CHIP, pin, 0)



# Group 1 meds (Breadboard 1)

BREADBOARD1 = [

    "Amlodipine Besylate", "Azithromycin", "Levothyroxine",

    "Metformin", "Lisinopril", "Atorvastatin", "Simvastatin"

]



# Group 2 meds (Breadboard 2)

BREADBOARD2 = [

    "Warfarin", "Omeprazole", "Donepezil",

    "Gabapentin", "Sertraline", "Hydrocodone", "Ciprofloxacin"

]



def play_buzzer(pin, duration):


    period = 1.0 / 2500

    half_period = period / 2

    end_time = time.time() + duration

    while time.time() < end_time:

        lgpio.gpio_write(CHIP, pin, 1)

        time.sleep(half_period)

        lgpio.gpio_write(CHIP, pin, 0)

        time.sleep(half_period)


def test_meds_group(group, buzzer_pin):

    for med in group:

        led_pin = LED_PINS[med]

        print(f"Testing {med} ")

        for _ in range(3):

            lgpio.gpio_write(CHIP, led_pin, 1)

            play_buzzer(buzzer_pin, 0.5)

            lgpio.gpio_write(CHIP, led_pin, 0)

            time.sleep(0.5)

        print(f"{med} test complete ")
        print(f"\n\n")

        time.sleep(5)  # Pause 5 seconds before next med/led test


try:

    print("Testing Breadboard 1")

    test_meds_group(BREADBOARD1, BUZZER1_PIN)



    print("\nTesting Breadboard 2")

    test_meds_group(BREADBOARD2, BUZZER2_PIN)



except KeyboardInterrupt:

    print("Testing completed")



finally:

    lgpio.gpiochip_close(CHIP)
