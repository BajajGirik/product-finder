## Intro:

This project is a web crawler designed to discover product URLs from multiple e-commerce websites.
It navigates website structures to extract product pages while handling dynamic content.

## Setup:

0. [Optional] Install virtual environment for project
   * Run `python3 -m venv .venv` to create a virtual environment
   * Run `source .venv/bin/activate` to activate the virtual environment
1. Install dependencies via `pip install -r requirements.txt`
2. Run `playwright install`
3. Run `python -u product_finder/main.py` from the root directory

## Todos and Future Improvements:
1. **Better Product URL Detection**: Add custom handling for different e-commerce platforms
2. **Multi-threading**: Use threads to offload work (Currently the code heavy relies on asynchronous tasks for efficiency)
3. **Rate Limiting & Respecting Robots.txt**: Implement better compliance with site policies.
