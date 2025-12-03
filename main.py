from playwright.sync_api import sync_playwright
import os
import subprocess
import time
import shutil
import datetime
import requests

LOCATOR_TO_FIND_EMAILS = '[data-focusable-row="true"]'
USER_DATA_PATH = os.path.join(os.path.dirname(__file__), "browser_data")
ROOT_DOWNLOADS_PATH = os.path.join(os.path.dirname(__file__), "downloads")
AUDIO_DOWNLOADS_PATH = os.path.join(ROOT_DOWNLOADS_PATH, "audio")
HTML_DOWNLOADS_PATH = os.path.join(ROOT_DOWNLOADS_PATH, "html")
SLOW_MO = 200
FEED="scriptnotes-seasons-1-2"


page = None
current_download_folder = ROOT_DOWNLOADS_PATH


def unselect():
    global page
    page.evaluate("window.getSelection().removeAllRanges()")
    page.evaluate("document.activeElement.blur()")


def copy_string_to_clipboard(s: str):
    subprocess.run(["xclip", "-selection", "clipboard"], input=s.encode(), check=True)


def setup_downloads(remove_old=False):
    if remove_old:
        shutil.rmtree(ROOT_DOWNLOADS_PATH, ignore_errors=True)
    if not os.path.exists(ROOT_DOWNLOADS_PATH):
        os.makedirs(ROOT_DOWNLOADS_PATH)
    if not os.path.exists(AUDIO_DOWNLOADS_PATH):
        os.makedirs(AUDIO_DOWNLOADS_PATH)
    if not os.path.exists(HTML_DOWNLOADS_PATH):
        os.makedirs(HTML_DOWNLOADS_PATH)


def save_page_as_html(filename=None):
    retried = False
    try:
        global page
        if filename is None:
            # Generate filename from current URL
            current_url = page.url
            filename = current_url.split("/")[-1] or "page"
    
        # Get the complete HTML content
        html_content = page.content()
    
        # Save to HTML downloads folder
        html_file_path = os.path.join(HTML_DOWNLOADS_PATH, filename + ".html")
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
        print(f"Page saved as: {html_file_path}")
        return html_file_path
    except Exception as e:
        print(f"Error saving page as HTML: {e}")
        if not retried:
            retried = True
            print("Retrying save...")
            return save_page_as_html(filename)


def save_audio_from_page():
    retried = False
    try:
        global page
        title = page.url.split("/")[-1]
        player_section = page.locator(".listen-episode-player")
        secondary_buttons = player_section.locator(".player_secondary_buttons")
        download_button = secondary_buttons.locator("a")
        url_link = download_button.get_attribute("href")
        response = requests.head(url_link)
        file_path = os.path.join(AUDIO_DOWNLOADS_PATH, title + ".mp3")
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(requests.get(url_link).content)
            print(f"Audio saved as: {file_path}")

    except Exception as e:
        print(f"Error downloading audio: {e}")
        if not retried:
            retried = True
            print("Retrying download...")
            save_audio_from_page()


def process_episode_page():
    save_audio_from_page()
    save_page_as_html()


def process_list_page():
    global page
    listing = page.locator(".listen-episode-listing")
    episode_links = listing.locator("a")
    links = [episode_links.nth(i).get_attribute("href") for i in range(episode_links.count())]
    for i in range(len(links)):
        episode_url = links[i]
        print(f"Processing episode: {episode_url}")
        page.goto(episode_url)
        process_episode_page()


def main():
    global page
    global current_download_folder
    print("Starting Playwright script...")
    print("Removing old downloads...")
    setup_downloads(True)
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_PATH,
            headless=False,
            slow_mo=SLOW_MO,
            viewport={"width": 1920, "height": 1080},
        )  # slow_mo adds delays

        page = browser.new_page()
        for page_number in range(1):
            #page.goto(f"https://scriptnotes.supportingcast.fm/listen?feed={FEED}&page={page_number}", wait_until="networkidle")
            url = f"https://scriptnotes.supportingcast.fm/listen?page={page_number}"
            print(f"Processing list: {url}")
            page.goto(url, wait_until="networkidle")
            process_list_page()
            
        browser.close()


if __name__ == "__main__":
    main()
