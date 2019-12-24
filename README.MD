## Anti XXX XXX CLUB GENERATOR
This repo contains all that is needed to have a VM that watches a single S3 Bucket
for orders to generate text images that then need to be sent to the REST Printful API

For this repo:
- AWS S3 for PSD storage that is streamed to PHOTOPEA
- geckodriver latest version (may need update as Firefox updates)
- Python 2.7
- boto3, pyautogui, selenium
- other script files for process and reading

# Setup
1. Open a fresh Ubuntu Latest stable VM
2. install repo and get latest geckodriver. Install virtualenv w/requirements
```
# Installing Geocokdriver latest
cd this_repo

wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

tar -xvzf geckodriver*

chmod +x geckodriver
```
3. Open firefox and go to photopea.com
4. Load in the `.ttf` font and click 'OK' when prompted to cache font. Close new user modal
5. Update ENV Vars
6. Will need to debug the coordinates for `pyautogui` coordinates :/ (selenium cant do it all)

# Overview of Functions
- Front end gets details of text for social replacement, color, and generates random filename
- Order is written to S3 bucket `requests` as `JSON` by backend
- A python script running on a EC2 Ubuntu VM is polling the `requests` folder for new requests
- It will read in request and create a logo by same filename in `results`
- It will remove the `request` JSON file by moving it to `processed`
- backend monitors `results` for `<filename>.png`. When available it streams back result to frontend
- User can then download image file generated (??)
- Can then proceed to generate mockups on hoodie, basic shirts
