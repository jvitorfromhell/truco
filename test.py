# Imports
import pygame, sys
import cards, player, game

p = player.Player("Eu")
g = player.Player("Ele")

d = cards.Deck()

d.shuffle()
d.deal([p, g])

truco = game.Game()

for card in p.cards:
    print card.getSuit(), card.getValue()

print ""

for card in g.cards:
    print card.getSuit(), card.getValue()