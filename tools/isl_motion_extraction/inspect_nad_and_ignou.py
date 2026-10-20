import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Inspect NAD Contact
req = urllib.request.Request("https://nadindia.org/Contact", headers={"User-Agent": "Mozilla/5.0"})
html_nad = urllib.request.urlopen(req, context=ctx, timeout=15).read().decode("utf-8", errors="replace")
print("=== NAD India Contact Page Content ===")
for line in html_nad.splitlines():
    if any(k in line.lower() for k in ["email", "mail", "@", "phone", "contact", "address", "nadindia"]):
        print(line.strip())

# 2. Search IGNOU for School of Humanities
req_ignou = urllib.request.Request("https://www.ignou.ac.in/", headers={"User-Agent": "Mozilla/5.0"})
html_ignou = urllib.request.urlopen(req_ignou, context=ctx, timeout=15).read().decode("utf-8", errors="replace")
soh_links = [l for l in re.findall(r'href=["\']([^"\']*)["\']', html_ignou) if any(k in l.lower() for k in ["soh", "humanities", "disli", "schools"])]
print("\n=== IGNOU SOH Links on Homepage ===")
print(soh_links[:10])
