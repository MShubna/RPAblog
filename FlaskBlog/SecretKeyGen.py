#import secrets
#print(secrets.token_hex(16))

import os
for key in os.environ:
    print(key,"->", os.environ[key])

