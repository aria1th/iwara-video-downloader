### download video from iwara.tv
### usage: python iwara [url]
### by AngelBottomless @ github
# download from iwara page
import requests
# use selenium to get video url
from selenium import webdriver
import argparse

def download_video(url):
    # save video to local
    filename = url.split('/')[-1] + '.mp4'
    # get video
    driver = run_webdriver(url)
    click_accept(driver)
    driver.implicitly_wait(2)
    click_play(driver)
    url = find_video_url(driver)
    # download video
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
    # close driver
    driver.close()

def download_with_retry(url, retry=3):
    # retry download
    for _ in range(retry):
        try:
            download_video(url)
            break
        except:
            print('download failed, retrying...')
            continue

def run_webdriver(url):
    # use selenium to get video url
    # mute chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    # run webdriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(4)
    return driver

def click_accept(driver):
    # xpath = /html/body/div[3]/div/div[2]/button[1]
    button = driver.find_element('xpath', '/html/body/div[3]/div/div[2]/button[1]')
    button.click()
def click_play(driver):
    # xpath = //*[@id="vjs_video_3"]/button
    button = driver.find_element('xpath', '//*[@id="vjs_video_3"]/button')
    button.click()

def find_video_url(driver):
    # xpath //*[@id="vjs_video_3_html5_api"]
    #access 'src'
    video = driver.find_element('xpath', '//*[@id="vjs_video_3_html5_api"]')
    video_url = video.get_attribute('src')
    return video_url


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='iwara video url')
    args = parser.parse_args()
    # download video
    download_with_retry(args.url)
