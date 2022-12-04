from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os


class gpt3:
    def __init__(self):
        PLAY = sync_playwright().start()
        BROWSER = PLAY.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright", headless=False,
        )
        self.page = BROWSER.new_page()

        # create a folder to store the code
        os.mkdir("code")

    def get_input_box(self):
        """Get the child textarea of `PromptTextarea__TextareaWrapper`"""

        return self.page.query_selector(
            "div[class*='PromptTextarea__TextareaWrapper']"
        ).query_selector("textarea")

    def is_logged_in(self):
        try:
            # See if we have a textarea with data-id="root"
            return self.get_input_box() is not None
        except AttributeError:
            return False

    def send_message(self, message):
        # Send the message
        box = self.get_input_box()
        box.click()
        box.fill(message)
        box.press("Enter")
        while self.page.query_selector(".result-streaming") is not None:
            time.sleep(0.1)

    def get_last_message(self):
        """Get the latest message"""
        page_elements = self.page.query_selector_all(
            "div[class*='ConversationItem__Message']"
        )
        last_element = page_elements[-1]

        try:
            self.get_code_from_message(last_element.inner_html())
        except AttributeError:
            pass

        return last_element.inner_text()

    def get_code_from_message(self, message):
        soup = BeautifulSoup(message, "html.parser")
        code = soup.find("pre").text

        # remove 'Copy code' from the code
        code = code.replace("Copy code", "")

        # write the code to a file
        file_name = f"code_{int(time.time())}.py"
        with open(f"code/{file_name}", "w") as f:
            f.write(code)

        return file_name

    def chat(self, message):
        self.page.goto("https://chat.openai.com/")
        if not self.is_logged_in():
            print("Please log in to OpenAI Chat")
            print("Press enter when you're done")
            input()
        else:
            print("Logged in")

        self.send_message(message)
        response = self.get_last_message()

        return response

    def rate_my_code(self, path_to_code):
        # try to read the code
        try:
            with open(path_to_code, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print("File not found")
            return

        # send the code to openai saying can you rate this code from 1-10 and why?
        return self.chat(f"{code}")

    def get_code(self, file_name=None):
        if file_name is None:
            file_name = os.listdir("code")[-1]
        else:
            file_name = f"code_{file_name}.py"
