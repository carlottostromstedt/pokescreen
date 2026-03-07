import asyncio
import random
from tcgdexsdk import Language, TCGdex, Query
from tcgdexsdk.enums import Quality, Extension

# Set SDK to Japanese
sdk = TCGdex(Language.EN)

def get_random_japanese_card_image():
    # Get all Japanese sets
    sets = sdk.set.listSync()

    # Pick a random set
    selected_set = random.choice(sets)

    print(f"📦 Set: {selected_set.name} ({selected_set.id})")

    card_list = sdk.card.listSync(Query().equal("set", selected_set.id))
    card = random.choice(card_list)

    print(f"🇯🇵 Set: {selected_set.name} ({selected_set.id}), Card #: {card.id}")

    # Get high quality PNG image
    response = card.get_image(Quality.HIGH, Extension.PNG)
    image_data = response.read()

    return image_data

DEST = "/home/developer/github/pokescreen/examples/7color/images/poke_card.png"
TMP  = "/home/developer/github/pokescreen/examples/7color/images/poke_card.tmp"
INTERVAL = 600  # seconds between card changes

if __name__ == "__main__":
    import os
    import time

    while True:
        try:
            image_data = get_random_japanese_card_image()
            if image_data:
                with open(TMP, "wb") as f:
                    f.write(image_data)
                os.replace(TMP, DEST)  # atomic — vbz3.py never sees a partial file
                print("✅ Card saved")
        except Exception as e:
            print(f"❌ Error fetching card: {e}")
        time.sleep(INTERVAL)
