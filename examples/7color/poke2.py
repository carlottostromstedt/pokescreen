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

if __name__ == "__main__":
    image_data = get_random_japanese_card_image()

    if image_data:
        with open("/home/developer/inky/examples/7color/images/poke_card.png", "wb") as f:
            f.write(image_data)
        print("✅ Japanese card image saved as poke_card.png")
