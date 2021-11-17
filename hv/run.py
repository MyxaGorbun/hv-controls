import sys


def hv_controls_cmd():
    from hv.cmd_ui import HVShell
    HVShell().cmdloop()

def hv_controls_qt(args):
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    from hv.qt_ui import HVWindow
    window = HVWindow(args)
    window.show()
    return sys.exit(app.exec_())