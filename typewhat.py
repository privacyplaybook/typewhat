import os
import openai
import dns.resolver
from dotenv import load_dotenv
import whois
import time

# Load configuration
load_dotenv()
TYPO_COUNT = int(os.getenv("TYPO_COUNT", 10))
DNS_TYPE = os.getenv("DNS_TYPE", "ALL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", 60))
WHOIS_DELAY = float(os.getenv("WHOIS_DELAY", 1.5))  # seconds between WHOIS queries

openai.api_key = OPENAI_API_KEY

def generate_typos(domain, typo_count):
    prompt = (
        f"Generate a list of {typo_count} plausible typo-squatting variants for the domain '{domain}', "
        "including common keyboard mistakes, character swaps, missing letters, or substitutions. "
        "Only output the raw domain variants, one per line, no commentary."
    )
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.6,
        timeout=OPENAI_TIMEOUT,
    )
    typos = [line.strip() for line in response.choices[0].message.content.splitlines() if line.strip()]
    return typos

def check_domain_registered(domain, dns_type):
    try:
        if dns_type.upper() == "ALL":
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

def get_whois_entity(domain):
    try:
        w = whois.whois(domain)
        # Try to get most reliable organization/owner info
        entity = w.get('org') or w.get('registrant_org') or w.get('name') or w.get('registrar') or w.get('emails')
        if isinstance(entity, list):
            entity = ', '.join(entity)
        return str(entity) if entity else None
    except Exception as e:
        return None

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

        print(f"Getting WHOIS for {domain} (original)")
        orig_entity = get_whois_entity(domain)
        if not orig_entity:
            print(f"  [!] WHOIS info for original domain not found.")
        else:
            print(f"  [*] Registered to: {orig_entity}")

        for typo in typos:
            if typo == domain:
                continue
            print(f"Checking {typo} ...", end=' ')
            if check_domain_registered(typo, DNS_TYPE):
                typo_entity = get_whois_entity(typo)
                time.sleep(WHOIS_DELAY)
                if typo_entity:
                    is_same = (orig_entity and typo_entity and orig_entity.lower() == typo_entity.lower())
                    print(f"REGISTERED - WHOIS: {typo_entity}")
                    found_typos.append({
                        'typo': typo,
                        'registered': True,
                        'whois': typo_entity,
                        'same_owner': is_same
                    })
                else:
                    print("REGISTERED - WHOIS: Not found")
                    found_typos.append({
                        'typo': typo,
                        'registered': True,
                        'whois': None,
                        'same_owner': False
                    })
            else:
                print("not registered")

    # Write results to output file
    with open(output_filename, 'w') as outfile:
        for result in found_typos:
            outfile.write(f"{result['typo']}\tregistered={result['registered']}\twhois={result['whois']}\tsame_owner={result['same_owner']}\n")
    print(f"Detection complete. Found {len(found_typos)} registered typos.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python typosquat_whois_check.py <input_file.txt> <output_file.txt>")
        exit(1)
    main(sys.argv[1], sys.argv[2])
