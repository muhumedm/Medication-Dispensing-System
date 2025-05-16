"""

Medication Reminder System


Last Updated: 15/05/2025


What it does:

- Connects to the Django system to check for upcoming medication doses

- Blinks an LED and sounds the correct buzzer for each due dose

- Waits for the patient to press a confirmation button

- Sends that confirmation back to the system and notifies the carer via email

"""



# ========== IMPORTS ========== #



import lgpio  # GPIO control for Raspberry Pi

import time  # For delays and timing between alerts

import requests  # To send and receive API requests

import logging  # For saving logs to a file

from datetime import datetime, timedelta, timezone  # Date and time handling

from zoneinfo import ZoneInfo  # For timezone conversion (UTC to BST)



# ========== LOGGING CONFIGURATION ========== #

logging.basicConfig(

    filename="/home/muna/Documents/reminder.log",  # Log file location

    level=logging.INFO,  # Logs Info

    format='[%(asctime)s] [%(levelname)s] %(message)s',  # Log format

    datefmt='%Y-%m-%d %H:%M:%S'  # Date/time format

)



# ========== GPIO SETUP ========== #

CHIP = lgpio.gpiochip_open(0)  # Open GPIO chip 0 for control


# Pin mapping for each medication LED

LED_PINS = {
    
    #Bread Board 1 - First 7 Medications
    "Amlodipine Besylate": 2,

    "Azithromycin": 3,

    "Levothyroxine": 4,

    "Metformin": 14,

    "Lisinopril": 15,

    "Atorvastatin": 17,

    "Simvastatin": 18,
    
    
    # Bread Board 2 - Next 7 Medications
    
    "Warfarin": 5,

    "Omeprazole": 6,

    "Donepezil": 12,

    "Gabapentin": 13,

    "Sertraline": 16,

    "Hydrocodone": 19,

    "Ciprofloxacin": 20

}



BUZZER1_PIN = 27  # Buzzer for board 1

BUZZER2_PIN = 21  # Buzzer for board 2

BUTTON_PINS = [22, 26]  # Buttons for patient confirmation


# Set output mode for LEDs and buzzers

for pin in list(LED_PINS.values()) + [BUZZER1_PIN, BUZZER2_PIN]:

    lgpio.gpio_claim_output(CHIP, pin, 0)


# Set input mode for buttons

for pin in BUTTON_PINS:

    lgpio.gpio_claim_input(CHIP, pin)



# ========== API ENDPOINTS ========== #

# Base API URL and endpoints for fetching and confirming medication doses

API_BASE_URL = "http://192.168.1.193:8000/medications/api"

FETCH_ENDPOINT = f"{API_BASE_URL}/due-doses/"  # Endpoint to fetch due doses

CONFIRM_ENDPOINT = f"{API_BASE_URL}/confirm-dose/"  # Endpoint to confirm a taken dose


# ========== FUNCTIONS ========== #

#Function to fetch all doses due in a certain time range
def fetch_due_doses():

    """

    Get doses due between 2 hours ago and 1 hour from now

    """

    try:

        response = requests.get(FETCH_ENDPOINT)

        if response.status_code == 200:

            raw_doses = response.json()

            now_utc = datetime.now(timezone.utc)

            time_from = now_utc - timedelta(hours=2)

            time_to = now_utc + timedelta(hours=1)

            print(f"[DEBUG] Current time: {now_utc}")

            for d in raw_doses:

                print(f"[DEBUG] Dose ID {d['id']} scheduled for: {d['scheduled_time']}")

            return [

                d for d in raw_doses

                if time_from <= datetime.fromisoformat(d['scheduled_time']) <= time_to

            ]

    except Exception as e:

        logging.error(f"Fetch failed: {e}")

        print(f"[{datetime.now()}] Error: Could not fetch due doses – {e}")

    return []


# Function to confirm that a dose has been taken
def confirm_dose(dose_id, patient_name, med_name, scheduled_time):

    """Send dose confirmation to the server"""

    try:

        now_utc = datetime.now(timezone.utc)

        london_tz = ZoneInfo("Europe/London")

        scheduled_local = scheduled_time.astimezone(london_tz)

        confirmed_local = now_utc.astimezone(london_tz)

        msg = (

            f"Confirmed: {patient_name} took {med_name} | "

            f"Scheduled: {scheduled_local.strftime('%Y-%m-%d %H:%M')} | "

            f"Confirmed: {confirmed_local.strftime('%H:%M')}"

        )

        logging.info(msg)

        print(f"\n{msg}\n")

        response = requests.post(CONFIRM_ENDPOINT, json={"dose_id": dose_id})

        if response.status_code != 200:

            reason = response.json().get('error', 'Unknown error')

            logging.error(f"Could not confirm dose {dose_id}: {reason}")

            print(f"\nCould not confirm dose {dose_id}: {reason}\n")

    except Exception as e:

        logging.error(f"Error while confirming dose {dose_id}: {e}")

        print(f"\nError while confirming dose {dose_id}: {e}\n")



# Determines which buzzer to use based on medication group
def get_buzzer_for_medication(med_name):

    group1 = [

        "Amlodipine Besylate", "Azithromycin", "Levothyroxine", "Metformin",

        "Lisinopril", "Atorvastatin", "Simvastatin"

    ]

    return BUZZER1_PIN if med_name in group1 else BUZZER2_PIN


# Plays a short buzzer sound for a set duration
def play_buzzer(pin, duration):

    period = 1.0 / 2500

    half_period = period / 2

    end_time = time.time() + duration

    while time.time() < end_time:

        lgpio.gpio_write(CHIP, pin, 1)

        time.sleep(half_period)

        lgpio.gpio_write(CHIP, pin, 0)

        time.sleep(half_period)



#Blinks LED, sounds buzzer, and waits for button confirmation
def alert_and_confirm(dose):

    med_name = dose['medication_name']

    dose_id = dose['id']

    led_pin = LED_PINS.get(med_name)

    buzzer_pin = get_buzzer_for_medication(med_name)



    if not led_pin:

        msg = f"No LED mapped for {med_name}"

        logging.warning(msg)

        print(f"[{datetime.now()}] Skipped: {msg}")

        return



    patient_name = dose.get("patient_name", "")

    patient_id = dose.get("patient_id", "")

    scheduled_raw = dose.get("scheduled_time", "")


    try:

        scheduled_dt = datetime.fromisoformat(scheduled_raw)

        if scheduled_dt.tzinfo is None:

            scheduled_dt = scheduled_dt.replace(tzinfo=timezone.utc)

        scheduled_local = scheduled_dt.astimezone(ZoneInfo("Europe/London"))

    except Exception as e:

        logging.error(f"Failed to parse scheduled_time: {e}")

        scheduled_dt = datetime.now(timezone.utc)


    print("\n")

    alert_msg = (

        f"ALERT: {med_name} is due for {patient_name} "

        f"(Patient {patient_id}, Dose ID: {dose_id})"

    )

    logging.info(alert_msg)



    time.sleep(1)

    print(f"[{datetime.now()}] Waiting for confirmation (button press)...")

    logging.info("Waiting for confirmation (button press)...")



    start_time = time.time()

    while time.time() - start_time < 30:

        lgpio.gpio_write(CHIP, led_pin, 1)

        play_buzzer(buzzer_pin, 0.5)

        lgpio.gpio_write(CHIP, led_pin, 0)

        time.sleep(0.5)



        for pin in BUTTON_PINS:

            if lgpio.gpio_read(CHIP, pin) == 1:

                confirm_dose(dose_id, patient_name, med_name, scheduled_dt)

                lgpio.gpio_write(CHIP, led_pin, 0)

                return



    lgpio.gpio_write(CHIP, led_pin, 0)

    play_buzzer(buzzer_pin, 1.0)

    timeout_msg = f"Timed out: No confirmation for dose {dose_id}"

    logging.warning(timeout_msg)

    print(f"\n[{datetime.now()}] {timeout_msg}\n")



# ========== MAIN LOOP ========== #

# Continuous loop to check and alert for new doses - 3 hours timeframe set in case of any issues (e.g. rebooting etc)

seen_dose_ids = set()



try:

    while True:

        logging.info("Checking for due doses...")

        print(f"[{datetime.now()}] Checking for due doses...")

        doses = fetch_due_doses()



        if not doses:

            msg = "There are no more scheduled doses at this time."

            logging.info(msg)

            print(f"[{datetime.now()}] {msg}\n")



        for dose in doses:

            if dose['id'] not in seen_dose_ids:

                alert_and_confirm(dose)

                seen_dose_ids.add(dose['id'])

                time.sleep(60)  # Wait before checking again



except KeyboardInterrupt:

    logging.info("Program shut down manually by user.")

    print("\nProgram shut down successfully.\n")



finally:

    lgpio.gpiochip_close(CHIP)  # Clears GPIO

    logging.info("GPIO resources released.")
