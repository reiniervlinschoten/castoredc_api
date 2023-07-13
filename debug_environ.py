import platform
import ssl
import urllib3

print("OS", platform.platform())
print("Python", platform.python_version())
print(ssl.OPENSSL_VERSION)
print("urllib3", urllib3.__version__)
