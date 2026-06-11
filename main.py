import arcade

from game import Process


def main():
    window = Process()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()