import sys
import os
import shutil
import re
import subprocess
import configparser
import urllib
import urllib.parse
import urllib.request
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QListWidget,
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QComboBox, QFileDialog, QCheckBox, QHeaderView, QTableView
)
from PySide6.QtGui import (QPixmap, QIcon)
from PySide6.QtCore import (Qt, QAbstractTableModel, QSize, Signal)

# Configure Paths
APP_DIR = Path.home() / ".local" / "share" / "applications"
APP_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = Path.home() / ".local" / "share" / "WebappManager"
PROFILES_DIR = DATA_DIR / "Profiles"
ICON_PATH = "/usr/lib/WebappManager/WebappManager.svg"
ICON = QIcon(ICON_PATH)
DESKTOP_PREFIX = "webapp-"

PROFILES_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure Logging
LOGGER = logging.getLogger("WebappManager")
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = RotatingFileHandler(
    LOG_DIR / "WebappManager.log",
    maxBytes = 5 * 1024 * 1024,
    backupCount = 3
)
LOGGER_FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() %(message)s")
LOGGER_HANDLER.setFormatter(LOGGER_FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)

#region Runtimes
class Runtime:
    def identifier(self) -> str:
        raise NotImplementedError

    def is_installed(self) -> bool:
        raise NotImplementedError

    def build_exec(self) -> str:
        raise NotImplementedError

class NativeRuntime(Runtime):
    def __init__(self, bin_name: str):
        self.bin_name = bin_name

    def identifier(self) -> str:
        return self.bin_name

    def is_installed(self) -> bool:
        return shutil.which(self.bin_name) is not None

    def build_exec(self) -> str:
        return f"{self.bin_name}"

class FlatpakRuntime(Runtime):
    def __init__(self, flatpak_id: str):
        self.flatpak_id = flatpak_id

    def identifier(self) -> str:
        return self.flatpak_id

    def is_installed(self) -> bool:
        try:
            subprocess.run(
                ["flatpak", "info", self.flatpak_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except Exception as e:
            return False

    def build_exec(self) -> str:
        return f"flatpak run {self.flatpak_id}"

class SnapRuntime(Runtime):
    def __init__(self, snap_name: str):
        self.snap_name = snap_name

    def identifier(self) -> str:
        return self.snap_name

    def is_installed(self) -> bool:
        try:
            subprocess.run(
                ["snap", "list", self.snap_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except Exception as e:
            return False

    def build_exec(self) -> str:
        return f"{self.snap_name}"

#region Browsers
def app_data_dir(app_id: str) -> Path:
    return PROFILES_DIR / app_id

# Abstract base class for different web-browsers
class Browser():
    def __init__(self, runtimes: list[Runtime]):
        super().__init__()
        self.runtimes = runtimes

    def pick_runtime(self) -> Runtime | None:
        for rt in self.runtimes:
            if rt.is_installed():
                return rt
        return None

    def generate_profile(self, app_id: str): 
        pass

    def is_installed(self) -> bool:
        return self.pick_runtime() is not None

    def fmt_args(self, app_id: str, url: str, hide_navigation: bool) -> str:
        raise NotImplementedError

    def fmt_dotdesktop(self, app_id: str, app_name: str, url: str, *, category:str, icon: str, hide_navigation: bool, comment: str) -> str :
        runtime = self.pick_runtime()
        if not runtime:
            raise RuntimeError("Browser not installed in any supported form")

        cmd = runtime.build_exec()
        args = self.fmt_args(app_id, url, hide_navigation)

        contents = f"""[Desktop Entry]
Type=Application
Icon={icon}
Name={app_name}
Comment={comment}
Exec={cmd} {args}
Terminal=false
Categories={category};WebBrowser;
StartupWMClass={app_id}"""
        return contents

class ChromiumBased(Browser):
    def __init__(self, runtimes: list[Runtime]):
        super().__init__(runtimes)

    def generate_profile(self, app_id: str): 
        #Maybe create actual data dir folder??
        #app_data_dir(app_id=app_id).mkdir(parents=True, exist_ok=True)
        pass

    def fmt_args(self, app_id: str, url: str, hide_navigation: bool) -> str:
        if hide_navigation:
            return f"--class={app_id} --user-data-dir={app_data_dir(app_id)} --app={url}"
        else:
            return f"--class={app_id} --user-data-dir={app_data_dir(app_id)} {url}"

class FirefoxBased(Browser):
    def __init__(self, runtimes: list[Runtime]):
        super().__init__(runtimes)

        self.PROFILE_TEMPLATE_PATH: Path = Path("/usr/lib/WebappManager/Profiles/Firefox")
        self.PROFILE_USER_PATH: Path = Path.home() / ".var" / "app" / "org.mozilla.firefox" / "WebappManager"

    def generate_profile(self, app_id: str):
        userPath: Path = self.PROFILE_USER_PATH
        
        if not userPath.exists():
            sourcePath: Path = self.PROFILE_TEMPLATE_PATH
            userPath.mkdir(parents=True, exist_ok=True)
            shutil.copytree(sourcePath, userPath, dirs_exist_ok = True)

    def fmt_args(self, app_id: str, url: str, hide_navigation: bool) -> str:
        if hide_navigation:
            profile_path: Path = self.PROFILE_USER_PATH
            return f"-no-remote --class={app_id} --name={app_id} -profile {str(profile_path)} --new-window {url}"
        else:
            return f"-no-remote --class={app_id} --name={app_id} --new-window {url}"

class Chrome(ChromiumBased):
    def __init__(self):
        super().__init__([NativeRuntime("google-chrome"), FlatpakRuntime("com.google.Chrome")])

class Chromium(ChromiumBased):
    def __init__(self):
        super().__init__([NativeRuntime("chromium"), FlatpakRuntime("org.chromium.Chromium"), SnapRuntime("chromium")])

class Edge(ChromiumBased):
    def __init__(self):
        super().__init__([NativeRuntime("microsoft-edge"), FlatpakRuntime("com.microsoft.Edge")])

class Brave(ChromiumBased):
    def __init__(self):
        super().__init__([NativeRuntime("brave-browser"), FlatpakRuntime("com.brave.Browser"), SnapRuntime("brave")])

class Helium(ChromiumBased):
    def __init__(self):
        super().__init__([FlatpakRuntime("net.imput.helium")])

class Firefox(FirefoxBased):
    def __init__(self):
        super().__init__([NativeRuntime("firefox"), FlatpakRuntime("org.mozilla.firefox"), SnapRuntime("firefox")])

class LibreWolf(FirefoxBased):
    def __init__(self):
        super().__init__([NativeRuntime("librewolf"), FlatpakRuntime("io.gitlab.librewolf-community")])
        self.PROFILE_USER_PATH: Path = Path.home() / ".var" / "app" / "io.gitlab.librewolf-community" / "WebappManager"


ALL_BROWSERS = [Firefox(), Chrome(), Chromium(), Edge(), Brave(), Helium(), LibreWolf()]
BROWSERS = [browser for browser in ALL_BROWSERS if browser.is_installed()]

#region Custom Widgets
class DesktopFile():
    def __init__(self, path: Path):
        self._path: Path = path
        self._name: str = path.name
        self._categories: list[str] = []
        self._browser = "?"
        self._icon_path = None

        try:
            config = configparser.ConfigParser()
            config.read(path)
            if (not config.has_section("Desktop Entry")):
                return

            entry = config["Desktop Entry"]
            self._name = entry.get("Name", self._name)
            self._categories = entry.get("Categories", "").split(";")
            self._icon_path = entry.get("Icon", "").strip()
            if self._icon_path == None or self._icon_path == "":
                self._icon_path = None

            exec_cmd = entry.get("Exec", self._name)
            for browser in ALL_BROWSERS:
                for runtime in browser.runtimes:
                    if runtime.identifier() in exec_cmd:
                        self._browser = type(browser).__name__
                        return
        except Exception as e:
            print(str(e))
            pass

    def delete(self) -> bool:
        if not self._path.exists() or not self._path.is_file():
            return False
        try:
            os.unlink(self._path)
            return True
        except:
            return False

    def app_name(self) -> str:
        return self._name

    def categories(self) -> list[str]:
        return self._categories

    def browser(self) -> str:
        return self._browser

    def icon(self) -> str | None:
        return self._icon_path
    
    def filepath(self) -> Path:
        return self._path

class ClickableLabel(QLabel):
    """A QLabel that emits a click event."""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked()
    
    def clicked(self):
        pass  # will be overridden

class IconPicker(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_path = None

        layout = QVBoxLayout()

        # Image preview
        self.icon_label = ClickableLabel()
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("border: 1px solid gray;")

        # Default placeholder
        self.icon_label.setText("Click to\nselect icon")

        # Override click behavior
        self.icon_label.clicked = self.open_file_dialog

        layout.addWidget(self.icon_label)

        # Optional button (alternative way to open dialog)
        self.button = QPushButton("Choose Icon")
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            "/usr/share/icons/hicolor/scalable/apps",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.ico *.svg)"
        )

        if file_path:
            self.set_icon(file_path)

    def set_icon(self, path):
        self.selected_path = path

        pixmap = QPixmap(path)

        # Scale to fit label nicely
        pixmap = pixmap.scaled(
            self.icon_label.width(),
            self.icon_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.icon_label.setPixmap(pixmap)


class RemoteIconFetcher():
    def try_fetch(self, url: str | Path) -> Path | None:
        return False

class DuckDuckGoFavicon(RemoteIconFetcher):
    def try_fetch(self, url: str | Path) -> Path | None:
        domain: str = urllib.parse.urlparse(url).netloc
        safe_url: str = urllib.parse.quote_plus(domain)
        duck_duck_go: str = f"https://icons.duckduckgo.com/ip3/{safe_url}.ico"
        local_filename: Path = APP_DIR / (safe_url + ".webp")

        try:
            urllib.request.urlretrieve(duck_duck_go, str(local_filename))

            if local_filename.exists():
                return local_filename
            return None
        except Exception as e:
            LOGGER.error(str(e))
            return None

class GoogleFavicon(RemoteIconFetcher):
    def try_fetch(self, url: str | Path) -> Path | None:
        domain: str = urllib.parse.urlparse(url).netloc
        safe_url: str = urllib.parse.quote_plus(domain)
        duck_duck_go: str = f"https://www.google.com/s2/favicons?domain={safe_url}"
        local_filename: Path = APP_DIR / (safe_url + ".png")

        try:
            urllib.request.urlretrieve(duck_duck_go, str(local_filename))

            if local_filename.exists():
                return local_filename
            return None
        except Exception as e:
            LOGGER.error(str(e))
            return None

#region Gui
# -----------------------------
# Add-Webapp Window
# -----------------------------
class AddWebappWindow(QWidget):
    closed = Signal()

    icon_fetchers = [DuckDuckGoFavicon(), GoogleFavicon()]
    category_list = [
        "AudioVideo",
        "Audio",
        "Video",  
        "Development",
        "Education",   
        "Game",    
        "Graphics",    
        "Network", 
        "Office",  
        "Settings",
        "Utility", 
    ]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Webapp")
        self.resize(640, 480)
        self.setWindowIcon(ICON)

        layout = QVBoxLayout()

        def make_row(*args):
            row_widget = QWidget()
            row_widget.setContentsMargins(0,0,0,0)
            row_layout = QHBoxLayout()
            row_widget.setLayout(row_layout)
            row_layout.setContentsMargins(0,0,0,0)

            for arg in args:
                arg.setContentsMargins(0,0,0,0)
                row_layout.addWidget(arg)

            return row_widget

        # Input fields
        self.icon_label = QLabel("Application Icon:")
        layout.addWidget(self.icon_label)

        self.icon_picker = IconPicker()
        layout.addWidget(self.icon_picker)

        self.name_label = QLabel("Application Name:")
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Website Name")
        layout.addWidget(self.name_input)

        self.desc_label = QLabel("Description:")
        layout.addWidget(self.desc_label)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("This Web App does...")
        layout.addWidget(self.desc_input)

        self.url_label = QLabel("Web URL:")
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.website.com")
        self.url_icon_button = QPushButton("Icon from url")
        self.url_icon_button.setMaximumWidth(160)
        self.url_icon_button.clicked.connect(self.download_icon_from_url)
        layout.addWidget(make_row(self.url_input, self.url_icon_button))

        self.browser_label = QLabel("Host Browser:")
        layout.addWidget(self.browser_label)

        self.browser_select = QComboBox()
        self.browser_select.addItems([type(browser).__name__ for browser in BROWSERS])
        layout.addWidget(self.browser_select)

        self.cat_label = QLabel("Category:")
        layout.addWidget(self.cat_label)

        self.cat_select = QComboBox()
        self.cat_select.addItems(self.category_list)
        self.cat_select.setCurrentIndex(self.category_list.index("Network"))
        layout.addWidget(self.cat_select)

        self.navigation_checkbox = QCheckBox()
        self.navigation_checkbox.setChecked(True)
        self.navigation_checkbox.setText("")
        layout.addWidget(make_row(QLabel("Hide Navigation Bar:"), self.navigation_checkbox))

        # Submit button
        self.submit_button = QPushButton("Create")
        self.submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def download_icon_from_url(self):
        url: str = self.url_input.text().strip()

        for strategy in self.icon_fetchers:
            local_filename = strategy.try_fetch(url)
            if local_filename != None:
                self.icon_picker.set_icon(str(local_filename))
                LOGGER.info(f"Icon fetched for URL '{url}' from {type(strategy).__name__}")
                return

        LOGGER.warning(f"No icon retrieval strategy worked for URL '{url}'")

    def handle_submit(self):
        name: str = self.name_input.text()
        url: str = self.url_input.text()
        comment: str = self.desc_input.text()
        icon_path: str = self.icon_picker.selected_path
        hide_nav: bool = self.navigation_checkbox.isChecked()
        browser: Browser = BROWSERS[self.browser_select.currentIndex()]
        cat: str = self.category_list[self.cat_select.currentIndex()]
        
        file_name = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F\s]", "-", name)
        file_path = APP_DIR / (DESKTOP_PREFIX + file_name + ".desktop")

        app_id = type(browser).__name__ + "-" + DESKTOP_PREFIX + file_name
        contents = browser.fmt_dotdesktop(app_id, name, url, category=cat, icon=icon_path, hide_navigation=hide_nav, comment=comment)

        try:
            if not APP_DIR.exists():
                APP_DIR.mkdir(parents=True)

            browser.generate_profile(app_id)

            with open(file_path, 'w') as file:
                file.write(contents)

            self.close()
            LOGGER.info(f"Application '{name}' created at '{file_path}'")

        except Exception as e:
            LOGGER.error(str(e))
            QMessageBox.information(self, "Error", "Something has gone wrong creating your application")

# -----------------------------
# Main Window
# -----------------------------
class AppListModel(QAbstractTableModel):
    headers: list[str] = ["Icon", "Name", "Browser", "Categories"]
    items: list[DesktopFile] = []

    def populate(self):
        directory = APP_DIR

        self.beginResetModel()
        if not directory.exists():
            self.items = []
        else:
            self.items = [DesktopFile(f) for f in directory.rglob(DESKTOP_PREFIX + "*.desktop") if f.is_file()]
        self.endResetModel()

    def get_file(self, index: int) -> DesktopFile | None:
        if index < 0 or index >= len(self.items):
            return None
        return self.items[index]

    def rowCount(self, parent=None):
        return len(self.items)

    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role):
        entry = self.items[index.row()]

        if index.column() == 0:
            if role == Qt.DecorationRole:
                return QIcon(entry.icon())
            elif role == Qt.DisplayRole:
                return None

        if role == Qt.DisplayRole:
            match index.column():
                case 1: 
                    return entry.app_name()
                case 2:
                    return entry.browser()
                case 3: 
                    return ", ".join(entry.categories())
                case _:
                    return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webapp Manager")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(ICON)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # List widget
        self.table_widget = QTableView()
        self.table_model = AppListModel()
        self.table_model.populate()
        self.table_widget.setModel(self.table_model)
        self.table_widget.setIconSize(QSize(24, 24))
        table_header = self.table_widget.horizontalHeader()
        table_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        table_header.setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.table_widget)

        # Button to open second window
        bottom_bar_widget = QWidget()
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_widget.setLayout(bottom_bar_layout)

        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setToolTip("Refresh App List")
        self.refresh_button.clicked.connect(self.refresh_list)
        bottom_bar_layout.addWidget(self.refresh_button)

        self.open_button = QPushButton("+")
        self.open_button.setToolTip("Create New App")
        self.open_button.clicked.connect(self.open_second_window)
        bottom_bar_layout.addWidget(self.open_button)

        self.delete_button = QPushButton("-")
        self.delete_button.setToolTip("Delete Selected App(s)")
        self.delete_button.clicked.connect(self.delete_item)
        bottom_bar_layout.addWidget(self.delete_button)

        layout.addWidget(bottom_bar_widget)
        central_widget.setLayout(layout)

        self.second_window = None  # keep reference

    def refresh_list(self):
        self.table_model.populate()

    def delete_item(self):
        selection = self.table_widget.selectionModel().selectedIndexes()
        if not selection:
            return 
        
        deletedAll = True
        for selected in selection:
            index = selected.row()
            if index is None or index < 0 or index >= self.table_model.rowCount():
                return

            item = self.table_model.get_file(index)
            if item is None:
                return

            didDelete = item.delete()
            if not didDelete:
                LOGGER.error(f"Failed to delete app '{item.filepath()}'")
            deletedAll = deletedAll and didDelete

        self.table_model.populate()

        if not deletedAll:
            QMessageBox.information(self, "Error", "One or more applications were unable to be deleted.")

    def open_second_window(self):
        self.second_window = AddWebappWindow()
        self.second_window.closed.connect(self.refresh_list)
        self.second_window.show()

#region Entrypoint
# -----------------------------
# App Entry Point
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())