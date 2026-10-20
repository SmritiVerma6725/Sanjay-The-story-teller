import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    ("NAD Contact (Capital C)", "https://nadindia.org/Contact"),
    ("DEF Contact (Trailing Slash)", "https://def.org.in/contact/"),
    ("IGNOU SOH HTTPS", "https://www.ignou.ac.in/ignou/aboutignou/school/soh/introduction"),
    ("IGNOU SOH Contact HTTPS", "https://www.ignou.ac.in/ignou/aboutignou/school/soh/contact"),
    ("IGNOU SOH Faculty HTTPS", "https://www.ignou.ac.in/ignou/aboutignou/school/soh/faculty"),
]

for label, url in urls:
    print(f"\n--- Testing {label} ({url}) ---")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            titles = re.findall(r"<title[^>]*>(.*?)</title>", html, re.I | re.DOTALL)
            emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html))
            obfuscated = re.findall(r"[a-zA-Z0-9_.+-]+\s*\[(?:at|AT)\]\s*[a-zA-Z0-9-]+\s*\[(?:dot|DOT)\]\s*[a-zA-Z0-9-.]+", html)
            print(f"Status: {resp.status}")
            print(f"Title: {titles[0].strip() if titles else 'No title'}")
            print(f"Emails found: {emails}")
            if obfuscated:
                print(f"Obfuscated emails: {obfuscated}")
            # print snippet of body
            clean_text = re.sub(r"<[^>]+>", " ", html)
            clean_text = re.sub(r"\s+", " ", clean_text).strip()
            print(f"Text snippet: {clean_text[:300]}...")
    except Exception as e:
        print(f"Error: {e}")
