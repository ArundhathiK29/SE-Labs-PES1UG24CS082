from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def round(self, bet):
        deck = Deck()
        player = []
        dealer = []

        # Initial player cards
        for _ in range(2):
            card = deck.draw()
            if card is None:
                print("Deck is empty.")
                break
            player.append(card)
            print(f"You drew {card[0]}{card[1]}")

        # Initial dealer cards
        for _ in range(2):
            card = deck.draw()
            if card is None:
                print("Deck is empty.")
                break
            dealer.append(card)
            

        self.show(player, dealer)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Natural blackjack
        if pv == 21 and len(player) == 2:
            self.show(player, dealer, hide=False)

            if dv == 21 and len(dealer) == 2:
                print("Push, bet returned")
            else:
                winnings = bet * 3 // 2
                self.chips += winnings
                print("Blackjack!")
                print(f"You win {winnings}")

            print("Chips:", self.chips)
            return True

        if dv == 21 and len(dealer) == 2:
            self.chips -= bet
            self.show(player, dealer, hide=False)
            print("Dealer blackjack.")
            print(f"You lose {bet}")
            print("Chips:", self.chips)
            return True

        # Player turn
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                return False

            if key == "s":
                break

            if key == "h":
                card = deck.draw()

                if card is None:
                    print("Deck is empty.")
                    break

                player.append(card)
                print(f"You drew {card[0]}{card[1]}")
                self.show(player, dealer)

                if hand_value(player) > 21:
                    self.chips -= bet
                    print("Bust.")
                    print(f"You lose {bet}")
                    print("Chips:", self.chips)
                    return True
            else:
                print("Invalid command. Enter h, s, or q.")

        # Dealer turn
        while hand_value(dealer) < 17:
            card = deck.draw()

            if card is None:
                print("Deck is empty.")
                break

            dealer.append(card)
            print(f"Dealer draws {card[0]}{card[1]}")

        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if dv > 21 or pv > dv:
            self.chips += bet
            print(f"You win {bet}")
        elif pv < dv:
            self.chips -= bet
            print(f"You lose {bet}")
        else:
            print("Push, bet returned")

        print("Chips:", self.chips)
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)

        while self.chips > 0:
            while True:
                entry = input(f"Chips: {self.chips}. Bet: ").strip().lower()

                if entry == "q":
                    return

                try:
                    bet = int(entry)

                    if 1 <= bet <= self.chips:
                        break

                    print(f"Invalid bet. Enter a whole number from 1 to {self.chips}.")

                except ValueError:
                    print(f"Invalid bet. Enter a whole number from 1 to {self.chips}.")

            if not self.round(bet):
                return

            if self.chips == 0:
                print("Out of chips. Game over.")
                return

            if input("Play again? [y/n]: ").strip().lower() != "y":
                return


if __name__ == "__main__":
    Blackjack().run()