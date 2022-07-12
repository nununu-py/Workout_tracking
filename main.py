import requests
import os
import datetime
from requests.auth import HTTPBasicAuth

current_date = datetime.date.today()
format_current_date = current_date.strftime("%Y/%m/%d")
current_time = datetime.datetime.now()
format_current_time = current_time.strftime("%H:%M:%S")

DATE = format_current_date
TIME = format_current_time
ACTION_KEY = [1, 2, 3, 4]
APP_ID = os.environ['MY_APP_ID']
API_KEY = os.environ['API_KEY']
AUTH_CODE = os.environ['AUTH']
HEADERS = {
    "Authorization": AUTH_CODE
}
PASSWORD = os.environ['PASSWORD']
BASIC_AUTH = HTTPBasicAuth("nununu_py", PASSWORD)

GENDER = "male"
MY_WEIGHT = 51.5
MY_HEIGHT = 157.5
MY_AGE = 23


def exercise_api(action_code):
    global API_KEY, APP_ID, GENDER, MY_AGE, MY_HEIGHT, MY_WEIGHT

    if action_code == 2 or action_code == 3:
        query = input("What exercise you did today : ")

        exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

        headers = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
        }

        parameters = {
                "query": query,
                "gender": GENDER,
                "weight_kg": MY_WEIGHT,
                "height_cm": MY_HEIGHT,
                "age": MY_AGE
            }

        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        result = response.json()["exercises"]

        return result

    else:

        return 0


def sheety_api(exercise_api_result, action_code):
    global DATE, TIME
    sheety_getpost_endpoint = "https://api.sheety.co/c31e003fae0f88b9d086de42f34e277f/workoutTracking/workouts"

    if exercise_api_result != 0:
        for data in exercise_api_result:
            exercise = data["user_input"]
            duration = data["duration_min"]
            calories = data["nf_calories"]

            sheety_parameters = {
                "workout": {
                    "date": DATE,
                    "time": TIME,
                    "exercise": exercise.title(),
                    "duration": duration,
                    "calories": calories
                }
            }

            if action_code == 2:
                new_response = requests.post(url=sheety_getpost_endpoint, json=sheety_parameters, auth=BASIC_AUTH)
                print(new_response.status_code)
            elif action_code == 3:
                specified_row = int(input("Which row do you want to modify : "))
                if specified_row > 1:
                    new_response = requests.put(url=f"https://api.sheety.co/c31e003fae0f88b9d086de42f34e277f/"
                                                f"workoutTracking/workouts/{specified_row}", json=sheety_parameters,
                                                auth=BASIC_AUTH)
                    print(new_response.status_code)
                else:
                    print("Cannot edit or remove Subject")

    else:
        if action_code == 1:
            new_response = requests.get(url=sheety_getpost_endpoint, auth=BASIC_AUTH)
            print(new_response.status_code)
            print(new_response.json())
        elif action_code == 4:
            specified_row = int(input("Which row do you want to delete : "))
            if specified_row > 1:
                new_response = requests.delete(url=f"https://api.sheety.co/c31e003fae0f88b9d086de42f34e277f/"
                                                   f"workoutTracking/workouts/{specified_row}", headers=HEADERS)
                print(new_response)
            else:
                print("Cannot edit or remove Subject")


action = int(input("What action do you want\n"
                   "1. GET DATA \n"
                   "2. POST DATA \n"
                   "3. PUT DATA \n"
                   "4. DELETE DATA \n"
                   "Chose action : "))

if action in ACTION_KEY:
    sheety_api(exercise_api(action), action)
else:
    print("Key is not available")
