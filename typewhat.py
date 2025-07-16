import os
import openai
import dns.resolver
from dotenv import load_dotenv

# Load configuration
load_dotenv()
TYPO_COUNT = int(os.getenv("TYPO_COUNT", 10))
DNS_TYPE = os.getenv("DNS_TYPE", "ALL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

openai.api_key = OPENAI_API_KEY

def generate_typos(domain, typo_count):
    prompt = (
        f"Generate a list of {typo_count} plausible typo-squatting variants for the domain '{domain}', "
        "including common keyboard mistakes, character swaps, missing letters, or substitutions. "
        "Only output the raw domain variants, one per line, no commentary."
    )
    # Use new OpenAI API for chat completions
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.6
    )
    typos = [line.strip() for line in response.choices[0].message.content.splitlines() if line.strip()]
    return typos

def check_domain_registered(domain, dns_type):
    try:
        if dns_type.upper() == "ALL":
            # Check common record types
            for rtype in ['A', 'AAAA', 'MX', 'CNAME', 'NS']:
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    if answers:
                        return True
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                    continue
            return False
        else:
            answers = dns.resolver.resolve(domain, dns_type)
            return bool(answers)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
        return False

def main(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        domains = [line.strip() for line in infile if line.strip()]

    found_typos = []
    for domain in domains:
        print(f"Generating typos for: {domain}")
        try:
            typos = generate_typos(domain, TYPO_COUNT)
        except Exception as e:
            print(f"OpenAI error for {domain}: {e}")
            continue

        for typo in typos:
            if typo == domain:  # Skip the original domain if generated
                continue
            print(f"Checking {typo} ...", end=' ')
            if check_domain_registered(typo, DNS_TYPE):
                print("REGISTERED")
                found_typos.append(typo)
            else:
                print("not registered")

    # Write to output file
    with open(output_filename, 'w') as outfile:
        for typo in found_typos:
            outfile.write(typo + "\n")
    print(f"Detection complete. Found {len(found_typos)} registered typos.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python detect_typosquat.py <input_file.txt> <output_file.txt>")
        exit(1)
    main(sys.argv[1], sys.argv[2])
