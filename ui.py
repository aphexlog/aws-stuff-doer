import TermTk as ttk


def initialize_frame_layout(root: ttk.TTk):
    main_box = ttk.TTkFrame(parent=root, layout=ttk.TTkVBoxLayout(), border=False)
    ttk.TTkFrame(
        parent=main_box,
        layout=ttk.TTkVBoxLayout(),
    )
    ttk.TTkFrame(
        parent=main_box,
        layout=ttk.TTkVBoxLayout(),
    )


def main():
    root = ttk.TTk()
    root.setLayout(ttk.TTkHBoxLayout())  # type: ignore
    initialize_frame_layout(root)
    root.mainloop()


if __name__ == "__main__":
    main()
