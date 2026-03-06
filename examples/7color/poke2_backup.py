import asyncio
import random
from tcgdexsdk import Language, TCGdex
from tcgdexsdk.enums import Quality, Extension

# Initialize SDK
sdk = TCGdex(Language.EN)

async def get_poke_card():
    # Fetch card metadata

    rnumber = random.randint(1, 100)

    card = await sdk.card.get(f"swsh3-{rnumber}")

    # Download image: returns an HTTPResponse object
    response = card.get_image(Quality.HIGH, Extension.PNG)

    # Extract bytes from response
    image_data = response.read()  # or: response.read() depending on HTTP client
     
    print(type(response))
    return image_data

# Run and save
if __name__ == "__main__":
    image_data = asyncio.run(get_poke_card())

    with open("/home/developer/inky/examples/7color/images/poke_card.png", "wb") as f:
        f.write(image_data)

    print("✅ Image saved as poke_card.png")
