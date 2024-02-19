# import unittest
# from unittest.mock import patch, MagicMock
# from aws_stuff_doer.uilib import TerminalUi


# class TestTerminalUI(unittest.TestCase):
#     def setUp(self):
#         self.title = "My CLI App"
#         self.term_ui = TerminalUI(title=self.title)

#     @patch("TermTk.TTk")
#     def test_ui_initialization(self, mock_terminal):
#         # This test checks if TerminalUI is correctly initializing with the specified title
#         term_ui = TerminalUI(title=self.title)
#         mock_terminal.assert_called_with(title=self.title)

#     @patch("TermTk.TTkVBoxLayout")
#     @patch("TermTk.TTkHBoxLayout")
#     @patch("TermTk.TTkFrame")
#     def test_initialize_frame_layout(
#         self, mock_frame, mock_hbox_layout, mock_vbox_layout
#     ):
#         # This test checks if the frames and layouts are being initialized properly
#         # Replace the real layout objects with mocks
#         self.term_ui._initialize_frame_layout()

#         # Assert if the main box is created with vertical layout
#         mock_frame.assert_called()
#         mock_vbox_layout.assert_called()

#         # You can add more assertions here to test other behaviors such as adding widgets


# if __name__ == "__main__":
#     unittest.main()
