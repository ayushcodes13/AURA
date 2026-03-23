import ssl
import urllib.request

print("Python SSL:", ssl.OPENSSL_VERSION)

try:
    print("Testing HTTPS request...")
    response = urllib.request.urlopen("https://api.deepgram.com")
    print("HTTPS status:", response.status)
except Exception as e:
    print("SSL ERROR:", e)