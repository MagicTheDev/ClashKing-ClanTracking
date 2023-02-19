import coc
import os

client = coc.EventsClient(key_names="Test", raw_attribute=True)

async def setup_coc():
    print(os.getenv("EMAIL"))
    try:
        await client.login(email=os.getenv("EMAIL"), password=os.getenv("EMAIL_PW"))
    except Exception as exc:
        print(f"Failed to setup clash api connection. Exiting! {exc}")
        exit(1)