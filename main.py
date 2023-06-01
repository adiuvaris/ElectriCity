import arcade


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(1024, 800, "test", resizable=True)


def main():
    window = MainWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main()
