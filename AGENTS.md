# Agent Guide for scriptnotes_download

## Project Overview
This project downloads episodes of the "scriptnotes" podcast by scraping https://scriptnotes.supportingcast.fm/listen. It uses Playwright to automate a browser, extracts episode links, and downloads both the HTML page and the audio MP3 file for each episode.

## Development Setup
1. **Python Version**: 3.12 (see `.python-version`)
2. **Dependencies**: Managed with `uv` (see `pyproject.toml` and `uv.lock`)
3. **Installation**:
   - Ensure `uv` is installed: `pip install uv` or see https://docs.astral.sh/uv/getting-started/installation/
   - Install dependencies: `uv sync`
   - Install Playwright browsers: `uv run playwright install chromium`

## Running the Script
- Use the justfile command: `just run`
- Or directly: `uv run main.py`

## Code Structure
- `main.py`: The main script containing all logic.
  - `setup_downloads()`: Creates necessary directories.
  - `save_page_as_html()`: Saves the current page's HTML to a file.
  - `save_audio_from_page()`: Downloads the audio MP3 from the current episode page.
  - `process_episode_page()`: Processes a single episode page (audio + HTML).
  - `process_list_page()`: Extracts episode links from the list page and processes each.
  - `main()`: Entry point, launches Playwright and orchestrates the scraping.
- `pyproject.toml`: Project metadata and dependencies.
- `justfile`: Commands for running and clearing downloads.
- `.python-version`: Specifies Python 3.12.
- `.gitignore`: Ignores downloads, browser data, and Python artifacts.

## Testing
- No tests are currently implemented.
- `pytest-playwright` is a dependency, suggesting future testing with Playwright.

## Contributing
- Follow PEP 8 style guidelines.
- Keep functions focused and well-documented.
- Test changes manually by running the script and verifying downloads.

## Notes
- The script uses a persistent browser context stored in `browser_data/`.
- Downloads are saved to `downloads/audio/` and `downloads/html/`.
- The script currently processes only page 0 of the list (hardcoded `range(1)`).
- It uses `slow_mo=200` to add delays between actions.
- Errors are caught and retried once.