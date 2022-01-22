import random


def draw_card(self):
    '''Returns top card from deck and removes from stack '''
    return self.deck.pop(0)

def draw_card_facedown(self):
    card = self.draw_card
    card.set_visibility_off()
    return card

def new_shuffle(self): #self.deck shuffled on obj creation
    '''shuffles self.deck in place '''
    self.deck = self.ref_deck.copy()
    random.shuffle(self.deck)
    print("Deck has been shuffled.")