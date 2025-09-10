from PySide6.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QColor,
)

# globals
color_blanc = QColor(0, 0, 0, 0)
color_diff_red = QColor(255, 0, 0, 125)
color_diff_green = QColor(0, 176, 47, 125)
color_diff_grey_back = QColor(0, 0, 0, 25)

# ------------ google ----------------
import diff_match_patch as dmp_module  # Import Google's diff-match-patch

def google_diff(text1: str, text2: str):
    dmp = dmp_module.diff_match_patch()
    dmp.Diff_Timeout = 5.0
    diffs = dmp.diff_main(text1, text2, checklines=False)
    dmp.diff_cleanupSemantic(diffs)

    return diffs

def fill_text_google(diffs, text_edit_left, text_edit_right):
        left_cursor = text_edit_left.textCursor()
        right_cursor = text_edit_right.textCursor()

        for op, data in diffs:
            if op == dmp_module.diff_match_patch.DIFF_EQUAL:
                add_line_google(left_cursor, data, color_blanc)
                add_line_google(right_cursor, data, color_blanc)
            elif op == dmp_module.diff_match_patch.DIFF_INSERT:
                add_line_google(right_cursor, data, color_diff_red)
            elif op == dmp_module.diff_match_patch.DIFF_DELETE:
                add_line_google(left_cursor, data, color_diff_green)

def add_line_google(cursor, text, color):
    char_format = QTextCharFormat()
    char_format.setBackground(color)
    cursor.insertText(text, char_format)


# ------------ difflib ----------------
from difflibparser import (
    DifflibParser,
    DiffCode,
)
def difflib_diff(text1: str, text2: str):
    return DifflibParser(text1.splitlines(), text2.splitlines())

def fill_text_difflib(diff, text_edit_left, text_edit_right):
    for entry in diff:
        left_cursor = text_edit_left.textCursor()
        right_cursor = text_edit_right.textCursor()

        if entry["code"] == DiffCode.SIMILAR:
            add_line_difflib(left_cursor, entry["line"], color_blanc)
            add_line_difflib(right_cursor, entry["line"], color_blanc)
        elif entry["code"] == DiffCode.RIGHTONLY:
            add_line_difflib(right_cursor, entry["line"], color_diff_red)
        elif entry["code"] == DiffCode.LEFTONLY:
            add_line_difflib(left_cursor, entry["line"], color_diff_green)
        elif entry["code"] == DiffCode.CHANGED:
            # Add the full original line in blue and save the starting position
            left_start_pos = add_line_difflib(
                left_cursor, entry["line"], color_diff_grey_back
            )
            # Add the full new line in blue and save the starting position
            right_start_pos = add_line_difflib(
                right_cursor, entry["newline"], color_diff_grey_back
            )

            # Apply more specific highlights to show exactly which characters changed
            apply_specific_highlight_difflib(
                left_cursor,
                entry["line"],
                entry["leftchanges"],
                color_diff_green,
                left_start_pos,
            )
            apply_specific_highlight_difflib(
                right_cursor,
                entry["newline"],
                entry["rightchanges"],
                color_diff_red,
                right_start_pos,
            )

def add_line_difflib(cursor, text, color):
    char_format = QTextCharFormat()
    char_format.setBackground(color)
    start_position = cursor.position()  # Save the start position
    cursor.insertText(text + "\n", char_format)
    return start_position

def apply_specific_highlight_difflib(cursor, text, changes, highlight_color, start_pos):
    cursor.setPosition(start_pos)  # Move cursor to the start position of the text

    for index in changes:
        cursor.setPosition(
            start_pos + index, QTextCursor.MoveAnchor
        )  # Move to the specific changed character
        cursor.movePosition(
            QTextCursor.Right, QTextCursor.KeepAnchor, 1
        )  # Select the changed character

        char_format = cursor.charFormat()
        char_format.setBackground(highlight_color)
        cursor.setCharFormat(char_format)

