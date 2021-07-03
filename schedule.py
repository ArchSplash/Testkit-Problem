from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import platform


plat = platform.platform().lower()
if plat.startswith("mac"):
    inherit = webdriver.Safari
else:
    inherit = webdriver.Chrome


class Browser(inherit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Go to site
        self.get("https://neilo.webuntis.com/WebUntis/?school=Wilhelm-Raabe-Schule+Lueneburg#/basic/timetable")

    def get_classes(self):
        # Wait until elements are visible
        wait = WebDriverWait(self, 30)
        classes_div = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "un-timetable-quickselect")))

        # Returns list of WebElements (all classes)
        classes = classes_div.find_elements_by_class_name("un-timetable-quickselect__button")
        return classes

    def get_day_schedule(self, date, i):
        # Get all classes and click
        classes = self.get_classes()
        classes[i].click()

        # Empty schedule from 1st to 10th period
        schedule = [[], [], [], [], [], [], [], [], [], []]

        # Wait 1 second (load)
        time.sleep(1)

        # Wait until timetable appears
        wait = WebDriverWait(self, 20)

        # Following code is unstable
        # load_xpath = '//*[@id="app"]/div/div/div[2]/div/div/section/div[1]/div/section/section/div/div/div[3]/div'
        # wait.until(ec.presence_of_element_located((By.XPATH, load_xpath)))
        # ---

        content = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "grupetScrollContainerContent")))

        # Get timetables
        day_schedule = content.find_elements_by_class_name("entryLayer")[0]

        # Get all periods
        try:
            WebDriverWait(day_schedule, 20).until(ec.presence_of_all_elements_located((By.TAG_NAME, "a")))
        # If timeout == no school
        except TimeoutException:
            # Return empty schedule
            return schedule

        # Get timetable for the day
        timetables = day_schedule.find_elements_by_tag_name("a")

        # Filter out every lesson that is NOT for the date
        timetables = list(filter(lambda tm: date in tm.get_attribute("href").split("/")[-2], timetables))

        # For each period...
        for t in timetables:
            # Get unconverted period
            time_ = t.get_attribute("href").split("/")[-2][len(date) + 1:len(date) + 3]
            # Get class subject, teacher and room
            classes = list(filter(lambda td: td.get_attribute("colspan") is not None,
                                  t.find_elements_by_tag_name("td")))

            # Convert period / hour to index
            index = int(time_) - 8

            template = []
            cancelled = "text-decoration: line-through;"

            # If class is cancelled
            # -> Append "-"
            if cancelled in classes[0].get_attribute("style"):
                template.append("-")
                template.append("-")

            # Else
            # -> Append subject and room
            else:
                template.append(classes[0].text)
                template.append(classes[-1].text)

            schedule[index].append(template)

        return schedule


# Get all schedules
def get_all_schedules(date: str):
    options = ChromeOptions()
    options.add_argument("--headless")
    browser = Browser()#"/usr/lib/chromium-browser/chromedriver") #, options=options)
    schedules = []
    classes_ = browser.get_classes()
    for i in range(len(classes_)):
        if classes_[i].text == "12":
            break
        schedules.append([classes_[i].text, browser.get_day_schedule(date, i)])
    return schedules
