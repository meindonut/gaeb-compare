from PySide6.QtWidgets import QMessageBox

def show_error_message(informative_text):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Kritischer Fehler")
    msg_box.setText("Ein Fehler ist aufgetreten!")
    msg_box.setInformativeText(informative_text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()

def show_user_question(question_text = "Wollen Sie fortfahren?"):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle("Bestätigung")
    msg_box.setText(question_text)

    # Create custom buttons
    yes_button = msg_box.addButton("Ja", QMessageBox.YesRole)
    msg_box.addButton("Nein", QMessageBox.NoRole)

    msg_box.exec()  # Show the message box
    return msg_box.clickedButton() == yes_button