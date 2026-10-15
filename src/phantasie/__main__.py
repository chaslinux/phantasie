"""Application entry point for Phantasie III."""

from phantasie.game import Game


def main() -> None:
    """Start the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
