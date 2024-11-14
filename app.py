import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, jsonify, Response
import threading
import time
import random
import pickle
import os
import json

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError("settings.json dosyası bulunamadı.")

settings = load_settings()

def load_api_keys():
    keys_file = settings["api"]["keys_file"]
    if os.path.exists(keys_file):
        with open(keys_file, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

API_KEYS = load_api_keys()

def save_cookies(driver):
    cookies = driver.get_cookies()
    with open(settings["cookies_path"], "wb") as f:
        pickle.dump(cookies, f)

def save_localstorage(driver):
    local_storage = driver.execute_script("return window.localStorage;")
    with open(settings["localstorage_path"], "wb") as f:
        pickle.dump(local_storage, f)

def load_cookies(driver):
    if os.path.exists(settings["cookies_path"]):
        with open(settings["cookies_path"], "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

def load_localstorage(driver):
    if os.path.exists(settings["localstorage_path"]):
        with open(settings["localstorage_path"], "rb") as f:
            local_storage = pickle.load(f)
            for key, value in local_storage.items():
                driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

def get_chrome_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument(f"user-agent={settings['driver']['user_agent']}")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    service = Service(settings["driver"]["chrome_driver_path"])
    driver = webdriver.Chrome(service=service, options=options)
    return driver

driver = get_chrome_driver()
driver.get("https://copilot.microsoft.com/")

load_cookies(driver)
load_localstorage(driver)

input(settings["log_messages"]["login_prompt"])

save_cookies(driver)
save_localstorage(driver)

app = Flask(__name__)

def extract_code_blocks(driver):
    code_elements = driver.find_elements(By.XPATH, settings["xpath_code_blocks"])
    code_text = "\n".join([elem.text for elem in code_elements if elem.text.strip()])
    return code_text

def remove_prefix(message):
    message = message.lstrip()
    prefixes = ["SaironAI+\n", "Copilot\n"]

    for prefix in prefixes:
        if message.startswith(prefix):
            message = message[len(prefix):]
            break

    return message

def modify_ai_message(message):
    for old, new in settings["replace"].items():
        message = message.replace(old, new)
    return message

def check_for_image_in_latest_message(latest_message_element):
    try:
        image_container = latest_message_element.find_element(By.XPATH, settings["xpath_img_container"])

        start_time = time.time()
        while time.time() - start_time < settings["img_link_check_timeout"]:
            try:
                img_element = latest_message_element.find_element(By.XPATH, './/img')
                if img_element:
                    img_src = img_element.get_attribute("src")
                    return {"img_link": img_src}
            except:
                pass
            time.sleep(0.1)
        
        return {"img_link": None}
    
    except:
        return {"img_link": None}

@app.route('/api', methods=['GET'])
def handle_api():
    yazi = request.args.get('yazi', '')
    api_key = request.args.get('key', '')

    if api_key not in API_KEYS:
        return jsonify({"error": settings["log_messages"]["invalid_api_key"]}), 403

    if not yazi:
        return jsonify({"error": settings["log_messages"]["missing_yazi_param"]}), 400

    try:
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, settings["xpath_user_input"]))
        )
        user_input.click()
        user_input.clear()
        user_input.send_keys(yazi)
        user_input.send_keys(Keys.ENTER)

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, settings["xpath_ai_message"]))
        )

        last_message = None
        while True:
            latest_message_element = driver.find_elements(By.XPATH, settings["xpath_ai_message"])[-1]
            latest_message = latest_message_element.text

            latest_message = remove_prefix(latest_message)
            latest_message = modify_ai_message(latest_message)

            if latest_message != last_message:
                last_message = latest_message
                time.sleep(0.3)
            else:
                code_block = extract_code_blocks(driver)
                image_data = check_for_image_in_latest_message(latest_message_element)

                response_data = {
                    settings["api"]["response_messages"]["ai_message"]: latest_message,
                    settings["api"]["response_messages"]["code_blocks"]: code_block,
                    settings["api"]["response_messages"]["img_link"]: image_data.get("img_link")
                }

                response_json = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
                return Response(response_json, content_type='application/json; charset=utf-8')

    except Exception as e:
        return jsonify({"error": f"Hata: {e}"}), 500

server_thread = threading.Thread(target=lambda: app.run(host=settings["server"]["host"], port=settings["server"]["port"]))
server_thread.start()

print(settings["log_messages"]["server_started"])
