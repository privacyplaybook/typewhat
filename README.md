# Typo Squatting Domain Detector

This tool detects registered typo-squatting domains that are similar to legitimate domains you specify. It uses the OpenAI API to generate plausible typo variants for each domain and then checks whether those variants are already registered by querying DNS records.

## Features

* **Generates typo-squatting variants** using OpenAI LLMs (e.g., GPT-4, GPT-4o).
* **Customizable output:** Choose how many typo variants to generate per domain.
* **DNS record check:** Specify which DNS record types to check (A, MX, etc., or ALL).
* **Simple input/output:** Works with plain text files for easy automation and scripting.

## Prerequisites

* Python 3.7+
* [OpenAI API key](https://platform.openai.com/signup)
* Basic knowledge of the command line

## Installation

1. **Clone the repository or copy the script** to your machine.

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Create a **\`\`** file** in the same directory as the script with your configuration:

   ```env
   TYPO_COUNT=10
   DNS_TYPE=ALL
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   OPENAI_MODEL=gpt-4o
   ```

   * `TYPO_COUNT`: (Optional) Number of typo variants to generate per domain (default: 10)
   * `DNS_TYPE`: (Optional) DNS record type to check, e.g., `A`, `MX`, `CNAME`, or `ALL` (default: ALL)
   * `OPENAI_API_KEY`: **Required** – your OpenAI API key
   * `OPENAI_MODEL`: (Optional) OpenAI model name (default: `gpt-4o`)

## Usage

1. **Prepare an input file** (e.g., `targets.txt`) with one domain per line:

   ```
   example.com
   mysite.org
   anotherdomain.net
   ```

2. **Run the script:**

   ```sh
   python detect_typosquat.py domains.txt typosquat_found.txt
   ```

   * `domains.txt` – input file with domains to check
   * `typosquat_found.txt` – output file with registered typo domains

3. **Review the output:**
   The output file (`typosquat_found.txt`) will contain a list of typo domains that are currently registered (one per line).

## Example

```
$ python detect_typosquat.py domains.txt typosquat_found.txt
Generating typos for: example.com
Checking exmaple.com ... REGISTERED
Checking exampl.com ... not registered
Checking exapmle.com ... REGISTERED
...
Detection complete. Found 2 registered typos.
```

## Notes

* **API usage**: Generating typo variants with OpenAI may consume tokens and incur costs.
* **DNS checks**: Not all registered domains respond to all DNS record queries; some false negatives may occur.
* **Rate limiting**: For large inputs, consider adding delays or batching to avoid API and DNS rate limits.

## License

MIT License
