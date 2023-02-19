import coc
import os

client = coc.EventsClient(key_names="Test", raw_attribute=True)

async def setup_coc():
    try:
        await client.login(email=os.environ.get("EMAIL"), password=os.environ.get("EMAIL_PW"))
    except Exception as exc:
        print(f"Failed to setup clash api connection. Exiting! {exc}")
        exit(1)