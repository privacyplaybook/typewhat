![AI-Generated](https://img.shields.io/badge/code-AI--generated-blueviolet)

# Typo Squatting Domain Detector with WHOIS Check

Detect registered typo-squatting domains for a list of input domains, and check if they are owned by the same entity as the original. The tool uses the OpenAI API to generate typo variants and checks their registration and WHOIS info.

---

## Features

* Generates typo-squatting domain variants using OpenAI LLMs
* Checks DNS records to see if the typo domain is registered
* Performs WHOIS lookups to compare the owner/organization with the original domain
* Outputs a summary including registration and owner comparison

---

## Installation

1. **Clone or Download** this repository, or copy the Python script files to your directory.

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   *Dependencies: `openai`, `python-dotenv`, `dnspython`, `python-whois`*

3. **Create a `.env` file** in the same folder with these contents:

   ```env
   TYPO_COUNT=10
   DNS_TYPE=ALL
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   OPENAI_MODEL=gpt-4o
   OPENAI_TIMEOUT=60
   WHOIS_DELAY=1.5
   ```

   * `TYPO_COUNT` = Max number of typos generated per domain (default 10)
   * `DNS_TYPE` = DNS record to check (`A`, `MX`, `CNAME`, or `ALL` for all; default ALL)
   * `OPENAI_API_KEY` = Your OpenAI API key
   * `OPENAI_MODEL` = OpenAI model to use (e.g., `gpt-4o`)
   * `OPENAI_TIMEOUT` = OpenAI API call timeout (seconds)
   * `WHOIS_DELAY` = Delay (seconds) between WHOIS queries (to avoid rate-limiting)

---

## Usage

1. **Prepare an input file** (e.g., `domains.txt`) with one domain per line:

   ```
   google.com
   example.org
   mysite.net
   ```

2. **Run the script:**

   ```sh
   python typewhat.py domains.txt typosquat_results.txt
   ```

   * The first argument is your input file.
   * The second argument is the output results file.

3. **Review the output**

   The output file (`typosquat_results.txt`) will contain lines like:

   ```
   gooogle.com	registered=True	whois=Google LLC	same_owner=True
   googl.com	registered=True	whois=Namecheap, Inc.	same_owner=False
   goggle.com	registered=True	whois=None	same_owner=False
   ```

   Each line gives:

   * The typo domain
   * Whether it's registered
   * Its WHOIS organization info (if available)
   * Whether the owner matches the original domain

---

## Notes & Limitations

* WHOIS info is sometimes unavailable, privacy-protected, or inconsistent.
* Typo generation uses OpenAI and may incur API cost.
* Avoid running against large lists too quickly (WHOIS lookups may get rate-limited; use `WHOIS_DELAY`).
* Not all domains will have clear/consistent organization info in WHOIS.

---

## License

This project is licensed under the terms of the
[Apache License 2.0](LICENSE).
