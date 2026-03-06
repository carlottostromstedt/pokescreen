from tcgdexsdk import Language, TCGdex
from tcgdexsdk.enums import Quality, Extension

tcgdex = TCGdex() # Initialize with default language (English)

# Initialize with language as string
tcgdex = TCGdex("en")

# Or using the Language enum
tcgdex = TCGdex(Language.EN)

sdk = TCGdex()

async def get_poke_card():
    # Open a smaller image
    card = await sdk.card.get("swsh3-136")

    # Get image URL with quality and format
    image_url = card.get_image_url(quality="high", extension="png")
    # Or using enums
    image_url_enum = card.get_image_url(Quality.HIGH, Extension.PNG)

    # Download image directly
    image_data = card.get_image(Quality.HIGH, Extension.PNG)

    return image_data

image = asyncio.run(get_poke_card)
