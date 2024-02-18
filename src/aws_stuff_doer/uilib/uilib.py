import TermTk as ttk


class TerminalUi:
    def __init__(self):
        self.root = ttk.TTk(title="ASD")
        self.root.setLayout(ttk.TTkHBoxLayout())  # type: ignore
        self.initialize_frame_layout()

    def initialize_frame_layout(self):
        main_box = ttk.TTkFrame(
            parent=self.root,
            layout=ttk.TTkVBoxLayout(),
            border=False,
        )
        top_frame = ttk.TTkFrame(
            parent=main_box,
            layout=ttk.TTkVBoxLayout(),
        )
        bottom_frame = ttk.TTkFrame(
            parent=main_box,
            layout=ttk.TTkVBoxLayout(),
        )

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    term_ui = TerminalUi()
    term_ui.main()
