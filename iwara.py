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
            return True
        except:
            print('download failed, retrying...')
            continue
    return False

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

def track_clipboard():
    import pyperclip
    import time
    import subprocess
    failed_urls = []
    success_urls = set()
    print('tracking clipboard...')
    # loop to track clipboard
    # if clipboard contains url, download video
    # track every 1 second
    previous = ''
    # expect KeyboardInterrupt and return 0
    try:
        while True:
            # get clipboard
            clipboard = pyperclip.paste()
            if clipboard != previous:
                # if clipboard contains url
                if 'iwara.tv' in clipboard:
                    print('url detected, downloading...')
                    # use subprocess to download video in background
                    # ['python', '-m', 'iwara', clipboard]
                    subprocess.Popen(['python', '-m', 'iwara', clipboard])
                    print('download complete')
                    previous = clipboard
            time.sleep(1)
    except KeyboardInterrupt:
        print('exiting...')
        return 0

if __name__ == '__main__':
    failed_urls = []
    success_urls = set()
    import sys
    # parse args
    parser = argparse.ArgumentParser()
    # track clipboard option, when 'track' is used, url is not required
    parser.add_argument('-t', '--track', action='store_true', help='track clipboard for iwara url')
    # add url argument, if not specified, use ''
    parser.add_argument('url', nargs='?', default='', help='iwara url')
    args = parser.parse_args()
    # download video
    if args.track:
        track_clipboard()
    elif 'iwara.tv' in args.url:
        result = download_with_retry(args.url)
        if not result:
            print('download failed')
            failed_urls.append(args.url)
        else:
            print('download complete')
            success_urls.add(args.url)
        if len(failed_urls) > 0:
            print('failed urls:')
            for url in failed_urls:
                print(url)
                # write in ./failed.txt
                with open('failed.txt', 'a') as f:
                    f.write(url + '\n')
                sys.exit(1)
    else:
        print('invalid url')
        sys.exit(1)
