# CONSTANTS
# Assuming we get the exact amount of materials every day
SWABS = 2000
CARDS = 1500
ANTIGENS = 2000


# Sort testkits
def sort_testkits():
    global SWABS, CARDS, ANTIGENS
    min_amount = min(SWABS, CARDS, ANTIGENS)
    SWABS -= min_amount
    CARDS -= min_amount
    ANTIGENS -= min_amount
    return min_amount
