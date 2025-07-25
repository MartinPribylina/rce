def get_button_style():
    return """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 15px;
        border: none;
        border-radius: 5px;
        font-size: 20px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """

def get_red_button_style():
    return """
    QPushButton {
        background-color: #f44336;
        color: white;
        padding: 15px;
        border: none;
        border-radius: 5px;
        font-size: 20px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #f95348;
    }
    """

def get_font_size_16_style():
    return """
    QLabel {
        font-size: 16px;
    }
    """