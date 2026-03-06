import asyncio
import random
from tcgdexsdk import Language, TCGdex
from tcgdexsdk.enums import Quality, Extension

# Initialize SDK
sdk = TCGdex(Language.EN)

async def get_random_card_image():
    # Get all sets
    sets = await sdk.set.list()

    # Pick a random set
    selected_set = random.choice(sets)
    set_id = selected_set.id
    total_cards = selected_set.cardCount.total

    # Pick a random card number within this set
    random_number = random.randint(1, total_cards)

    # Some sets use leading zeros, so try both formats if necessary
    card_id = f"{set_id}-{random_number}"
    print(card_id)
    print(f"📦 Selected Set: {selected_set.name} ({set_id}), Card #: {random_number}")

    try:
        card = await sdk.card.get(card_id)
    except Exception as e:
        print(f"⚠️ Failed to fetch {card_id}: {e}")
        return None

    response = card.get_image(Quality.HIGH, Extension.PNG)
    image_data = response.read()

    return image_data

if __name__ == "__main__":
    image_data = asyncio.run(get_random_card_image())

    if image_data:
        with open("/home/developer/inky/examples/7color/images/poke_card.png", "wb") as f:
            f.write(image_data)
        print("✅ Image saved as poke_card.png")
