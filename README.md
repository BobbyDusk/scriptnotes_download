# Scriptnotes Podcast Downloader

This project automates the downloading of episodes from the "scriptnotes" podcast. It scrapes the podcast's website to extract episode links and downloads both the HTML page and the audio MP3 file for each episode.

## Project Structure
```
scriptnotes_download/
├── main.py               # Main script with scraping logic
├── pyproject.toml        # Project metadata and dependencies
├── justfile              # Commands for running and maintenance
├── .python-version       # Python version specification (3.12)
├── .gitignore            # Ignored files and directories
├── uv.lock               # Dependency lock file
├── AGENTS.md             # Guide for AI agents
└── README.md             # This file
```

## Tech Stack
- **Language**: Python 3.12
- **Package Manager**: [uv](https://docs.astral.sh/uv/)
- **Web Scraping**: [Playwright](https://playwright.dev/python/) for browser automation
- **HTTP Requests**: [Requests](https://docs.python-requests.org/) for downloading audio files
- **HTML Parsing**: [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) (available but not currently used in main.py)
- **Task Runner**: [just](https://just.systems/) (via justfile)

## Dependencies
- `playwright`: Browser automation for scraping dynamic web pages.
- `requests`: HTTP library for downloading audio files.
- `beautifulsoup4`: HTML parsing library (available for future use).
- `httpx`: Async HTTP client (available for future use).
- `pytest-playwright`: Testing framework for Playwright (available for future testing).

## Installation
1. **Prerequisites**: Ensure Python 3.12 is installed.
2. **Install uv**: Follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
3. **Install dependencies**:
   ```bash
   uv sync
   ```
4. **Install Playwright browsers**:
   ```bash
   uv run playwright install chromium
   ```

## Usage
- **Run the downloader**:
  ```bash
  just run
  ```
  Or directly:
  ```bash
  uv run main.py
  ```
- **Clear downloaded files**:
  ```bash
  just clear-downloads
  ```

## How It Works
1. The script launches a Chromium browser using Playwright.
2. It navigates to the podcast listing page.
3. It extracts links to individual episode pages.
4. For each episode page:
   - Downloads the audio MP3 file to `downloads/audio/`.
   - Saves the HTML page to `downloads/html/`.
5. The browser context is stored in `browser_data/` for persistence.

## Notes
- The script currently processes only the first page of episodes (hardcoded).
- A slow motion delay (`slow_mo=200`) is added between browser actions.
- Errors are caught and retried once automatically.
- Downloaded files are stored in the `downloads/` directory.

## License
This project is for personal use only. Respect the podcast's terms of service.