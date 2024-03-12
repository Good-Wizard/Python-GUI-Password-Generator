from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFrame, QSlider, QHBoxLayout, QMessageBox, QLineEdit, QTableWidgetItem, QTableWidget, QInputDialog
from PyQt5.QtGui import QFont, QPalette, QColor, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits, punctuation
from plyer import notification
from sqlite3 import connect
from pyperclip import copy
from urllib.parse import urlparse
from validators import url as URL

slider_style = ("""
            QSlider::groove:horizontal {
                height: 3px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f67280, stop:0.5 #c06c84, stop:1 #355c7d);
            }
            QSlider::handle:horizontal {
                background: #222;
                border: 2px solid #f8b195;
                width: 20px;
                margin: -9px 0; /* handle is positioned by the top left corner, move it to the middle */
                border-radius: 10px;
            }
            """)

entry_style = ("""
    QLineEdit {
        width: 200px;
        height: 40px;
        border-radius: 5px;
        border: 2px solid #B2302D;
        background-color: #111111;
        font-size: 15px;
        font-weight: 600;
        color: #fefefe;
        padding: 5px 10px;
        outline: none;
    }
    QLineEdit:placeholder-text {
        color: #7e7e7e;
        opacity: 0.8;
    }
    QLineEdit:focus {
        border: 2px solid #3A8E3E;
    }
""")

button_style = ("""
            QPushButton {
                background-color: #0f1923;
                color: #ff4655;
                font-size: 15px;
                font-weight: 900;
                text-align: center;
                text-decoration: none;
                position: relative;
                margin: 10px 0;
                border: 3px solid #ff4655;
            }
            QPushButton:hover {
                color: #0f1923;
                background-color: #ff4655;
                border: 3px solid #0f1923;
                border: 3px solid #0f1923;
            }
        """)

button_style3 = ("""
            QPushButton {
                height: 50px;
            }
            QPushButton {
                background-color: #0f1923;
                color: #ff4655;
                font-size: 15px;
                font-weight: 900;
                text-align: center;
                text-decoration: none;
                position: relative;
                margin: 10px 0;
                border: 3px solid #ff4655;
            }
            QPushButton:hover {
                color: #0f1923;
                background-color: #ff4655;
                border: 3px solid #0f1923;
                border: 3px solid #0f1923;
            }
        """)

button_style2 = ("""
            QPushButton {

                height: 50px;
            }
            QPushButton {
                background-color: #0f1923;
                color: #ff4655;
                font-size: 15px;
                font-weight: 900;
                text-align: center;
                text-decoration: none;
                position: relative;
                margin: 10px 0;
                border: 3px solid #ff4655;
                height: 50px;
            }
            QPushButton:hover {
                color: #000000;
                background-color: #429D46;
                border: 3px solid #0f1923;
                border: 3px solid #0f1923;
            }
        """)

checkbox_style = ("""
    QCheckBox {
        color: #EBEBEB;
        font-size: 16px;
        font-weight: bold;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        margin: 5;
        border: 2px solid #BCD100;
        border-radius: 5px;
        background-color: #8F0000;
    }
    QCheckBox::indicator:checked {
        background-color: #006600;
        border: 2px solid #BCD100;
    }
    QCheckBox::indicator:hover {
        border: 2px solid #FFFFFF;
    }
    QCheckBox::indicator:disabled {
        background-color: #ddd;
        border: 2px solid #ddd;
    }
""")

class PasswordGenerator(QWidget):
    def __init__(self):
            super().__init__()
            # Set window properties
            self.setWindowTitle("Password Generator 1.4")
            self.setAutoFillBackground(True)
            self.generated_password = None
            def notify(self):
                    # Send a notification
                    notification.notify(
                        title='Password Copied',
                        message=f'Password Has Been Copied To Clipboard',
                        app_name='Password Manager'
                    )
                    QMessageBox.information(None, "Copied", "Password Successfully Copied!")
            def line():
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                return line
            
            def copy_to_clipboard():
                # Get the password from the label
                password = password_label.text()
                # Check if password is generated
                if not password:
                    QMessageBox.warning(None, 'Error', 'Please generate a password first.')
                    return
                # Copy the password to clipboard
                copy(password)
                # Play a sound (assuming you have a 'sound.wav' file in your directory) and Send a notification
                notify(self)

            def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, begin_letter):
                if not (use_lowercase or use_uppercase or use_symbols or use_numbers):
                    QMessageBox.critical(None, "Error", "Please Select at Least One Of The First 4 Options!")
                    return None
                else:
                    password = ""
                    if begin_letter:
                        password += choice(ascii_lowercase)
                        length -= 1  # Adjust the length after adding the beginning letter
                    characters = ""
                    if use_uppercase:
                        characters += ascii_uppercase
                    if use_lowercase:
                        characters += ascii_lowercase
                    if use_numbers:
                        characters += digits
                    if use_symbols:
                        characters += punctuation

                    for _ in range(length):
                        password += choice(characters)
                    password_label.setText(f"{password}")
                    return password, True

            def on_generate_button_clicked(self):
                # Get the current settings from the checkboxes and slider
                length = length_slider.value()
                use_uppercase = checkboxes[0].isChecked()
                use_lowercase = checkboxes[1].isChecked()
                use_numbers = checkboxes[2].isChecked()
                use_symbols = checkboxes[3].isChecked()
                begin_letter = checkboxes[4].isChecked()
                # Call the generate_password function
                generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, begin_letter)
            
            # Set Fusion style
            QApplication.setStyle("Fusion")

            # Set dark theme
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(15, 15, 15))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(palette)
            
            # Create layoutV
            layoutV = QVBoxLayout()
            layoutH = QHBoxLayout()
            layoutButton = QHBoxLayout()  # New layout for the buttons
            layoutV.setSpacing(10)  # Adjust spacing between widgets
            layoutV.setContentsMargins(10, 10, 10, 10)  # Adjust padding around the layoutV

            def update_slider(value, label, slider):
                if value < 12:
                    color = '#FF0505'  # Weak - Red
                    strength = 'Weak'
                elif value < 18:
                    color = '#FF8A05'  # Medium - Orange
                    strength = 'Medium'
                else:
                    color = '#00B312'  # Strong - Green
                    strength = 'Strong'
                
                # Update the label text with colored strength
                label.setText(f"<i><b>                      Password Length: <font color={color}>{value}</font> | Strength: <font color={color}>{strength}</font></b></i>")
                
                slider.setStyleSheet(slider_style)

            # Create password length label
            length_label = QLabel("Password Length (6 - 50):")
            length_label.setFont(QFont('Arial', 10))
            
            label1 = QLabel("<b>   Options 🔽</b>")
            label1.setFont(QFont("Arial", 12, ))

            # Create a horizontal slider for password length
            length_slider = QSlider(Qt.Horizontal)
            length_slider.setMinimum(6)  # Set minimum value
            length_slider.setMaximum(50)  # Set maximum value

            # Set tick position and interval
            length_slider.setTickPosition(QSlider.TicksBothSides)
            length_slider.setTickInterval(1)

            # Connect the slider to the update function
            length_slider.valueChanged.connect(lambda value: update_slider(value, length_label, length_slider))

            # Set initial value and trigger the update function manually to set the initial color
            length_slider.setValue(18)
            update_slider(18, length_label, length_slider)

            
            # Create options frame
            options_frame = QFrame()
            options_layout = QVBoxLayout(options_frame)
            options_layout.setSpacing(8)  # Adjust spacing between widgets
            options_layout.setContentsMargins(10, 10, 10, 10)  # Adjust padding around the layoutV

            checkboxes = [
                QCheckBox('UpperCase [ ABC ]'),
                QCheckBox('LowerCase [ abc ]'),
                QCheckBox('Number [ 123 ]'),
                QCheckBox('Symbols [ #$% ]'),
                QCheckBox('Begin With Letter'),
            ]

            for checkbox in checkboxes:
                checkbox.setStyleSheet(checkbox_style)

            # Add checkboxes to the options layoutV
            for checkbox in checkboxes:
                options_layout.addWidget(checkbox)
                
            generate_button = QPushButton("Generate 🛠")
            generate_button.setFont(QFont('Arial', 12))
            generate_button.setStyleSheet(button_style)
            generate_button.setFixedSize(200, 60)
            generate_button.clicked.connect(on_generate_button_clicked)

            self.save_passwords_button = QPushButton("Save Password 📩")
            self.save_passwords_button.setFont(QFont('Arial', 12))
            self.save_passwords_button.setStyleSheet(button_style)
            self.save_passwords_button.setFixedSize(200, 60)
            self.save_passwords_button.clicked.connect(self.save_to_db)
            
            # Create password label
            password_label = QLabel(f"")
            password_label.setFont(QFont('Arial', 13))  # Set font for label

            # Create buttons
            copy_button = QPushButton("📑")
            copy_button.setFont(QFont('Arial', 5))
            copy_button.setStyleSheet(button_style)
            copy_button.setFixedSize(50, 60)  # Make the copy button smaller
            copy_button.clicked.connect(copy_to_clipboard)

            # Create Button For Show Passwords
            show_passwords_button = QPushButton("Show Passwords 👀")
            show_passwords_button.setFont(QFont('Arial', 13))
            show_passwords_button.setStyleSheet(button_style3)
            show_passwords_button.clicked.connect(self.call_class_show_passwords)

            # Add widgets to layoutH
            layoutH.addWidget(password_label)  # Then add the password label
            layoutH.addWidget(copy_button)  # Add the copy button first

            # Add buttons to layoutButton
            layoutButton.addWidget(generate_button)
            layoutButton.addWidget(self.save_passwords_button)
            
            # Add widgets to layoutV
            layoutV.addWidget(length_label)
            layoutV.addWidget(length_slider)
            layoutV.addWidget(label1)
            layoutV.addWidget(options_frame)
            layoutV.addLayout(layoutH)  # Add the horizontal layout here
            layoutV.addWidget(line())  # Add the line here
            layoutV.addLayout(layoutButton)  # Add the new button layout here
            layoutV.addWidget(show_passwords_button)
            self.setLayout(layoutV)
    def save_to_db(self):
        self.save_window = SaveWindow()
        self.save_window.show()
    def call_class_show_passwords(self):
        self.show_passwords = ShowPassword(PasswordGenerator)
        self.show_passwords.show()
        
class ShowPassword(QWidget):
    def __init__(self, PasswordGenerator):
        self.password_generator = PasswordGenerator
        super().__init__()
        self.setWindowTitle("Show Passwords")
        self.setAutoFillBackground(True)
        # Create the table widget and set the column count
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["URL", "Email", "Password", "INFO"])
        self.table.setColumnWidth(0, 210)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 200)
        self.table.cellClicked.connect(self.cell_clicked)
        # Apply the updated stylesheet with a dark theme and improved spacing
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #333;  /* Dark background for the entire table */
                color: #FFF;  /* White text for better readability on dark background */
                font-size: 15px;
                border: none;  /* Remove border for a cleaner look */
            }
            QHeaderView::section {
                background-color: #555;  /* Slightly lighter shade for headers */
                padding: 12px;
                color: #FFF;
                font-size: 18px;
            }
            QTableCornerButton::section {
                background-color: #555;  /* Match header background */
            }
            QTableWidgetItem {
                padding: 20px 10px;  /* Increase vertical padding to 20px and horizontal to 10px */
                color: #FFF;  /* White text for items */
                font-size: 15px;
            }
            /* Alternating row colors for better readability */
            QTableWidget::item:nth-child(odd) {
                background-color: #444;  /* Darker shade for odd rows */
            }
            QTableWidget::item:nth-child(even) {
                background-color: #333;  /* Dark background for even rows */
            }
            /* Increase line spacing */
            QTableWidget::item {
                line-height: 1.6;  /* Increase line height for more space between lines */
            }
        """)
        
        # Create a layout
        layout = QVBoxLayout()
        # Add the table to the layout
        layout.addWidget(self.table)
        # Set the layout on the widget
        self.setLayout(layout)

        # Call the method to view data
        self.view_data()

        # Set a fixed size for the widget
        self.setFixedSize(900, 500)  # Adjust the size as needed
        
        
    def view_data(self):
        # Connect to the database
        conn = connect('passwords.db')
        cursor = conn.cursor()

        # Execute the query
        try:
            cursor.execute("SELECT * FROM passwords")
            data = cursor.fetchall()
            if not data:
                QMessageBox.warning(self, "Error", "Database Is Empty ❌")
                return
        except:
            QMessageBox.warning(self, "Error", "Database Is Empty ❌")
            return

        # Add the data to the table
        for i, row in enumerate(data):
            self.table.insertRow(i)
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)  # Disable editing
                self.table.setItem(i, j, table_item)
        # Show the table
        self.table.show()
        # Close the connection
        conn.close()



    def cell_clicked(self, row, column):
        item = self.table.item(row, column)
        if column == 2:  # Password column
            master_password, ok = QInputDialog.getText(self, 'Master Password', 'Enter the master password:')
            if ok and self.check_master_password(master_password):  # Replace with your master password checking logic
                real_password = self.get_real_password(item.text())  # Replace with your logic to get the real password
                # Copy the password to clipboard and Show the real password
                copy(real_password)
                QMessageBox.information(self, 'Copied', f'Password : {real_password}\nPassword has been copied to clipboard.')
            else:
                QMessageBox.warning(self, 'Error', 'Incorrect master password.')
        elif column == 0:  # URL column
            opening_link = QMessageBox.question(self, "LINK", "Wanna Open it?")
            if opening_link == QMessageBox.Ok:
                QDesktopServices.openUrl(QUrl(item.text()))
            elif opening_link == QMessageBox.Cancel:
                pass
        elif column == 1:  # Email column
            opening_email = QMessageBox.question(self, "LINK", "Wanna Copy it?")
            if opening_email == QMessageBox.Ok:
                copy(item.text())
                QMessageBox.information(self, 'Copied', 'Email has been copied to clipboard.')
            elif opening_email == QMessageBox.Cancel:
                pass
        elif column == 3:  # Description column
            QMessageBox.information(self, 'Description', item.text())

    def check_master_password(self, password):
        # Replace with your logic to check the master password
        return password == 'arash'

    def get_real_password(self, password):
        # Replace with your logic to get the real password
        return password
        
        
class SaveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save Password")
        self.setAutoFillBackground(True)

        # Create QLineEdit objects
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL 🔗")
        self.url_input.setStyleSheet(entry_style)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email 📧")
        self.email_input.setStyleSheet(entry_style)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password 🔑")
        self.password_input.setStyleSheet(entry_style)
        self.description_input = QLineEdit()
        self.description_input.setStyleSheet(entry_style)
        self.description_input.setPlaceholderText("Description 📝")

        # Create a button for saving the data
        self.save_button = QPushButton("Save It ✅")
        self.save_button.setStyleSheet(button_style2)
        self.save_button.clicked.connect(self.save_to_db)

        # Create a layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.save_button)
        self.setLayout(layout)



    def save_to_db(self):
        # Get the URL, Email, Password, and Description from the input fields
        url = self.url_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        description = self.description_input.text()

        # Check if the URL and Password fields are empty
        if not url or not password:
            QMessageBox.warning(self, 'Error', 'Please fill up both the URL and Password fields ❌')
            return

        # Check if the URL is valid
        try:
            if not url.startswith('www.'):
                url = 'www.' + url
            if not url.endswith('.com'):
                url = url + '.com'
            url = 'https://' + url if not url.startswith('https://') else url
            result = urlparse(url)
            if not all([result.scheme, result.netloc]) or not URL(url):
                QMessageBox.warning(self, 'Error', 'The URL is not valid. Please enter a valid URL ❌')
                return
        except ValueError:
            QMessageBox.warning(self, 'Error', 'The URL is not valid. Please enter a valid URL ❌')
            return

        # Connect to the database
        conn = connect('passwords.db')
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                url TEXT,
                email TEXT,
                password TEXT,
                description TEXT
            )
        ''')

        # Insert the data into the table
        cursor.execute('''
            INSERT INTO passwords (url, email, password, description) VALUES (?, ?, ?, ?)
        ''', (url, email, password, description))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Clear the input fields
        self.url_input.clear()
        QMessageBox.information(self, "Saved", "Password Successfully Saved ✅")


if __name__ == "__main__":
    app = QApplication(argv)
    window = PasswordGenerator()
    window.show()
    exit(app.exec_())
