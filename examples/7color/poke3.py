import asyncio
import random
from tcgdexsdk import Language, TCGdex
from tcgdexsdk.enums import Quality, Extension

# Initialize SDK
sdk = TCGdex(Language.JA)

print(sdk.set.listSync())
set = sdk.set.getSync("PMCG5")
print(set.cards)
