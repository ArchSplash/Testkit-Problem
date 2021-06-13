# CONSTANTS
# Assuming we get the exact amount of materials every day
SWABS = 2000
CARDS = 1500
ANTIGENS = 2000


# Variables for usage (local)
swabs = SWABS
cards = CARDS
antigens = ANTIGENS


class Testkit:
    def __init__(self):
        global swabs, cards, antigens
        # "Add"; Each testkit gets 1
        self.swabs = 1
        self.cards = 1
        self.antigens = 1

        # Subtract from variables
        swabs -= self.swabs
        cards -= self.cards
        antigens -= self.antigens


# Sort testkits
def sort_testkits():
    testkits = []
    min_amount = min(swabs, cards, antigens)

    for i in range(min_amount):
        testkits.append(Testkit())

    # print(len(testkits))
    # print("Swabs:", swabs)
    # print("Cards:", cards)
    # print("Antigens:", antigens)

    return testkits


# Testkits
TESTKITS = sort_testkits()
TESTKIT_AMOUNT = len(TESTKITS)
