REGISTER_MODE = True
FARM_MODE = True

# ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃     REFERRAL TIMING    ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
# The time that referrals will be registering

DAYS = 0
HOURS = 0
MINUTES = 10

# ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃   DELAY BEFORE START   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
# The time in seconds the account will wait before process, 60 * 60 = 1 hour

MIN_DELAY_BEFORE_START = 0
MAX_DELAY_BEFORE_START = 12 * 60 * 60

# ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ SSL CERTIFICATE VERIFY ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
# False only if error: SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed

SSL = True
