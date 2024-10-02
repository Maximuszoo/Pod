import sys
from PyQt5.QtWidgets import QApplication
from model import PodcastModel
from view import PodcastView
from controller import PodcastController

def main():
    app = QApplication(sys.argv)

    model = PodcastModel()
    view = PodcastView()
    controller = PodcastController(model, view)

    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

