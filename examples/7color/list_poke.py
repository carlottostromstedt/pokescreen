import asyncio
import random
from tcgdexsdk import Language, TCGdex, Query

# Initialize SDK in desired language (EN or JA)
sdk = TCGdex(Language.JA)

sets =  sdk.set.listSync()

print(sets)

selected_set = random.choice(sets)
print(f"📦 Set: {selected_set.name} ({selected_set.id})")

card_list = sdk.card.listSync(Query().equal("set", selected_set.id))

card = random.choice(card_list)

print(card)

