import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyautogui as gui
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def close_new_user_modal(driver):
    print("LOADED PHOTOPEA...")
    print("--- CLOSING INTRO MODAL ---")
    driver.find_element_by_xpath('//span[@onclick="hideCap()"]').click()
    print("--- CLOSED INTRO MODAL ---")

def load_font_into_photopea(driver):
    try:
        print("-- LOAD FONT INTO PHOTOPEA --")
        gui.moveTo(130, 176)
        gui.drag(978, 506, 2, button='left')
        gui.moveTo(1417, 456)
        gui.click()
        print("-- FONT LOADED --")
    except:
        pass

def set_font(driver):
    print("-- SETTING FONT CHOICE --")
    # Click the Text Tool
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[1]/div[2]/button[14]').click()
    # Click the font dropdown
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]/span[1]/button[1]').click()
    # Select All and then agian to unselect
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/span/input').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/span/input').click()
    # Select our local font loaded & click off so it stays selected
    driver.find_element_by_xpath("//span[contains(text(), 'Friz')]").click()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("-- FONT CHOICE SET! --")

def open_psd_template(driver):
    print("--- Open PSD URL MODAL --- ")
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/span/button[1]').click()
    driver.find_element_by_xpath("//*[contains(text(), 'Open from URL...')]").click()
    driver.find_element_by_xpath('//span[@class="fitem tinput"]/input').click()
    print("--- INPUT %s IN URL MODAL --- " % os.getenv("ASSC_PSD_URL"))
    driver.find_element_by_xpath('//span[@class="fitem tinput"]/input').send_keys(os.getenv("ASSC_PSD_URL"))
    print("--- SENDING REQUEST ---")
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/button').click()
    print("--- LOADING TEMPLATE ---")

    loaded_template = False
    while loaded_template is False:
        try:
            print('--- CHECKING IF LOADED... ---')
            driver.find_element_by_xpath("//*[contains(text(), 'ANTI')]")
            loaded_template = True
            print('--- TEMPLATE LOADED ---')
        except:
             print('--- TEMPLATE NOT LOADED ---')
             sleep(2)
             pass

def set_file_name(driver, filename):
    gui.click(x=int(os.getenv("PEA_FILENAME_X")), y=int(os.getenv("PEA_FILENAME_Y")), clicks=2)
    gui.typewrite(filename)
    gui.press('tab')
    gui.press('enter')


def set_social_tags(driver, idx, tag):
    print("SETTING SOCIAL TO %s" % (tag))
    # These are the location to click on the template for text of Social Text Holder
    SOCIAL_COORDS = [
        [int(os.getenv("SOCIAL_TAG_1_X")), int(os.getenv("SOCIAL_TAG_1_Y"))],
        [int(os.getenv("SOCIAL_TAG_2_X")), int(os.getenv("SOCIAL_TAG_2_Y"))]
    ]
    # Layer Container ( will list layers)
    # '/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div'
    driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div")[idx + 1].click()
    set_font(driver)
    gui.moveTo(SOCIAL_COORDS[idx][0], SOCIAL_COORDS[idx][1])
    gui.doubleClick()
    gui.typewrite(tag, interval=0.1)

    # Get pointer tool selected and select all
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[4]/div[1]/div[2]/button[1]").click()
    # select the first element
    driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div")[0].click()
    #select our first social template
    driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div")[idx + 1].click()

    # Select -> All via dropdown
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/span/button[5]").click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[3]/div[1]/span[2]").click()

    aligned = False
    while aligned is False:
        try:
            print('--- ATTEMPTING TO ALIGN... ---')
            driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]/span[5]/button[2]").click()
            aligned = True
            print('--- ALIGNED ---')
        except:
             print('--- ALERT MODAL BLOCKING ACTION ---')
             pass

def set_font_color(driver, customer_color):
    # Highlight ANTI -> CLUB Shift select and change color
    print("--- Highlighting Text Elements ---")
    driver.find_element_by_xpath("//*[contains(text(), 'ANTI')]").click()
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).perform()
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[3]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[3]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/div[4]').click()


    # Click the Text Tool and set the color
    # Select Text Tool
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[1]/div[2]/button[14]').click()
    # Click Color Box
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]/span[3]").click()
    # Click HEx Input &  send customer value
    driver.find_element_by_xpath('//span[@class="fitem tinput"]/input').click()
    print("--- INPUT %s AS COLOR (HEX) --- " % customer_color)
    gui.hotkey('ctrl', 'a')
    gui.typewrite(customer_color)
    # Submit Change
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/button').click()
    set_font(driver)

def save_file(driver):
    print("--- SAVING FILE ---")
    # Open File Dropdown
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/span/button[1]').click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[3]/div[9]/span[2]").click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[4]/div[1]").click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/button").click()
    sleep(1)
    gui.click(x=int(os.getenv("SAVE_FILE_X")), y=int(os.getenv("SAVE_FILE_Y")))
    sleep(2)
    gui.press('enter')
    print("--- FILE SAVED ---")
    driver.quit()


def create_logo(new_social_tags, color, filename):
    fp = webdriver.FirefoxProfile(os.getenv("FIREFOX_PROFILE"))
    driver = webdriver.Firefox(fp, executable_path=os.getenv("GECKODRIVER_LOC"))
    driver.set_window_position(2000,0)
    driver.get('https://photopea.com')

    try:
        # ---- Dont need this just preload font and cache it
        # close_new_user_modal()
        # load_font_into_photopea()
        open_psd_template(driver)
        set_file_name(driver, filename)

        # Set Social Tags to something new
        # TODO: IMPLEMENT CHECK TO MAKE SURE THE TEXT WAS CHANGED
        for idx, tag in enumerate(new_social_tags):
	    set_social_tags(driver, idx, tag)
        set_font_color(driver, color)
        save_file(driver)
    except:
        print("Error During Create Logo")
        driver.quit()


# ---------------- MAIN -------------------
#ASSC_PSD_URL = os.getenv("ASSC_PSD_URL")
#FIREFOX_PROFILE = os.getenv("FIREFOX_PROFILE")
#GECKODRIVER_LOC = os.getenv("GECKODRIVER_LOC")

# This is some sample data that will be passed in to the main function
#new_social_tags=["DIET", "KETO"]
#customer_color='#000'
#filename = 'MIMII'
#create_logo(new_social_tags, customer_color, filename)
