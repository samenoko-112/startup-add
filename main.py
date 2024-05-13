# Let the user specify the exe file and add it to startup.

from flet import *
import os
import winreg

def main(page:Page):
    page.title = "Add to startup"
    page.vertical_alignment = 'center'
    page.window_width = 500
    page.window_height = 230
    page.window_resizable = False
    page.window_center()

    def pick_file_result(e:FilePickerResultEvent):
        file_path.value = e.files[0].path
        file_path.update()

    file_picker = FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    def add_to_startup_click(e):
        if file_path.value != "":
            key = winreg.HKEY_CURRENT_USER
            key_value = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
            try:
                key = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, f"{os.path.basename(file_path.value)}", 0, winreg.REG_SZ, file_path.value)
                winreg.CloseKey(key)
                page.snack_bar = SnackBar(content=Text("Added to startup"))
                page.snack_bar.open = True
                page.update()
            except Exception as e:
                page.snack_bar = SnackBar(content=Text(str(e)))
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = SnackBar(content=Text("Please select a file"))
            page.snack_bar.open = True
            page.update()

    file_path = TextField(label="File path")
    pick_file = ElevatedButton("Pick file", on_click=lambda _:file_picker.pick_files(allowed_extensions=["exe"],dialog_title="追加するexeファイルを選択"))
    add_to_startup = ElevatedButton("Add to startup",on_click=add_to_startup_click)
    page.add(
        Column([
            file_path,
            pick_file,
            add_to_startup
        ])
    )

app(target=main)
