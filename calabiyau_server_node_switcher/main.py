import sys
from PyQt6.QtWidgets import QApplication
import import_path
from views.screens.main_view import MainView

if __name__ == "__main__":
    import_path.pass_import_path()
    app = QApplication(sys.argv)
    main_view = MainView()
    main_view.show()
    sys.exit(app.exec())
