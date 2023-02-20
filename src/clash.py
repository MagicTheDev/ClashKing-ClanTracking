import coc
import os

import dotenv
dotenv.load_dotenv()
clash_client = coc.EventsClient(key_names="Test", raw_attribute=True, throttle_limit=30, key_count=10)

async def setup_coc():
    try:
        await clash_client.login(email=os.getenv("EMAIL"), password=os.getenv("EMAIL_PW"))
    except Exception as exc:
        exit(1)