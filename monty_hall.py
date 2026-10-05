"""Monty Hall problem simulation: compare staying vs. switching.

Usage:
    python monty_hall.py                 # default seed 42, 1000 iterations each
    python monty_hall.py --seed 7        # different (but still repeatable) run
    python monty_hall.py --iterations 5000
"""

import argparse
import random

DOORS = (0, 1, 2)
STAY = "A"
SWITCH = "B"


def play_round(rng: random.Random, strategy: str) -> bool:
    """Play one game and return True if the player wins the car."""
    # Rule 1: one car, two goats.
    car = rng.choice(DOORS)

    # Rule 2: player picks a door at random.
    pick = rng.choice(DOORS)

    # Rule 3: host knowingly opens a goat door that is not the player's pick.
    goat_doors = [d for d in DOORS if d != pick and d != car]
    # If pick == car there are two goat doors -> host chooses randomly.
    # If pick != car there is exactly one -> host is forced to open it.
    opened = rng.choice(goat_doors)
    assert opened != car and opened != pick

    # Rule 4: apply strategy.
    if strategy == STAY:
        final = pick
    elif strategy == SWITCH:
        final = next(d for d in DOORS if d != pick and d != opened)
    else:
        raise ValueError(f"Unknown strategy: {strategy!r}")

    return final == car


def run_strategy(strategy: str, iterations: int, seed: int) -> int:
    """Run a strategy independently with its own seeded RNG; return win count."""
    rng = random.Random(seed)
    return sum(play_round(rng, strategy) for _ in range(iterations))


def main() -> None:
    parser = argparse.ArgumentParser(description="Monty Hall simulation")
    parser.add_argument("--seed", type=int, default=42,
                        help="base random seed for repeatable results (default: 42)")
    parser.add_argument("--iterations", type=int, default=1000,
                        help="games per strategy (default: 1000)")
    args = parser.parse_args()

    n = args.iterations
    # Each strategy gets its own independent RNG stream derived from the seed.
    wins_a = run_strategy(STAY, n, args.seed)
    wins_b = run_strategy(SWITCH, n, args.seed + 1)
    pct_a = 100 * wins_a / n
    pct_b = 100 * wins_b / n

    print("=" * 52)
    print(" MONTY HALL SIMULATION")
    print(f" Iterations per strategy: {n:,}   Seed: {args.seed}")
    print("=" * 52)
    print(f" {'Strategy':<26}{'Wins':>10}{'Win %':>14}")
    print("-" * 52)
    print(f" {'A: Always stay':<26}{wins_a:>10,}{pct_a:>13.2f}%")
    print(f" {'B: Always switch':<26}{wins_b:>10,}{pct_b:>13.2f}%")
    print("-" * 52)
    print(" Theoretical:  stay = 33.33%   switch = 66.67%")
    print("=" * 52)

    if wins_b > wins_a:
        print(f"CONCLUSION: Strategy B (ALWAYS SWITCH) yielded higher success "
              f"({pct_b:.2f}% vs {pct_a:.2f}%).")
        print("Switching won about "
              f"{wins_b / max(wins_a, 1):.2f}x as often as staying.")
    elif wins_a > wins_b:
        print(f"CONCLUSION: Strategy A (ALWAYS STAY) yielded higher success "
              f"({pct_a:.2f}% vs {pct_b:.2f}%).")
    else:
        print(f"CONCLUSION: Both strategies tied at {pct_a:.2f}%.")


if __name__ == "__main__":
    main()
