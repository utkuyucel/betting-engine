import random
from enum import Enum, auto


class ElectionOutcome(Enum):
    """Enumeration for possible election outcomes."""
    TRUMP_WIN = auto()
    BIDEN_WIN = auto()


class Election:
    """Represents an election with bet amounts for each possible outcome."""

    def __init__(self):
        self.bet_amounts = {outcome: 0 for outcome in ElectionOutcome}


class Bet:
    """Represents a single bet made by a user."""

    def __init__(self, user, election_outcome, amount):
        self.user = user
        self.election_outcome = election_outcome
        self.amount = amount

    def __str__(self):
        return f'{self.user} bets {self.amount} on {self.election_outcome.name}'


class BettingSystem:
    """Manages bets and calculates odds for an election."""

    def __init__(self, election: Election):
        self.election = election
        self.bets = []

    def place_bet(self, user: str, election_outcome: ElectionOutcome, amount: float) -> None:
        """Places a bet on a given election outcome."""
        bet = Bet(user, election_outcome, amount)
        self.bets.append(bet)
        self.election.bet_amounts[election_outcome] += amount

    def calculate_odds(self) -> dict[ElectionOutcome, float]:
        """Calculates the odds for each election outcome based on total bet amounts."""
        total_bet_amounts = sum(self.election.bet_amounts.values())
        odds = {
            outcome: total_bet_amounts / amount if amount > 0 else 1
            for outcome, amount in self.election.bet_amounts.items()
        }
        return odds

    def settle_bets(self, actual_outcome: ElectionOutcome) -> list[tuple[str, float]]:
        """Settles bets based on the actual election outcome and returns the winnings for each winner."""
        winners = [bet for bet in self.bets if bet.election_outcome == actual_outcome]
        total_correct_bets = sum(bet.amount for bet in winners)
        total_bet_amounts = sum(self.election.bet_amounts.values())
        results = [(winner.user, (winner.amount / total_correct_bets) * total_bet_amounts) for winner in winners]
        return results

    @staticmethod
    def print_odds(odds):
        print("\nOdds for each outcome:")
        for outcome, odd in odds.items():
            print(f'{outcome.name}: {odd:.2f}')

    @staticmethod
    def print_winners(results):
        if results:
            print('\nWinners and their winnings:')
            for user, winnings in results:
                print(f'{user}: ₺{winnings:.2f}')
        else:
            print("\nNo winners this time.")

    def place_and_print_bets(self, bet_placements):
        for user, outcome, amount in bet_placements:
            self.place_bet(user, outcome, amount)
            print(f'{user} placed ₺{amount} bet on {outcome.name}.')


def main() -> None:
    """Main function to simulate the betting system for an election."""
    election = Election()
    betting_system = BettingSystem(election)

    bet_placements = [
        ('UXXX', ElectionOutcome.TRUMP_WIN, 50),
        ('BXXX', ElectionOutcome.TRUMP_WIN, 50),
        ('HXXX', ElectionOutcome.TRUMP_WIN, 50),
        ('MXXX', ElectionOutcome.TRUMP_WIN, 50),
        ('GXXX', ElectionOutcome.TRUMP_WIN, 50),
        ('DXXX', ElectionOutcome.BIDEN_WIN, 500),
    ]


    betting_system.place_and_print_bets(bet_placements)  

    odds = betting_system.calculate_odds()
    betting_system.print_odds(odds)

    actual_outcome = ElectionOutcome.BIDEN_WIN
    results = betting_system.settle_bets(actual_outcome)

    print(f'\nElection outcome is: {actual_outcome.name}')
    betting_system.print_winners(results)


if __name__ == "__main__":
    main()
