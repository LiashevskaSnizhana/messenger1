from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore

import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host='http://127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self)

        self.host = host

        # to run on button click:
        self.pushButton.pressed.connect(self.send_message)

        # to run by timer:
        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def show_messages(self, messages):
        for message in messages:
            dt = datetime.fromtimestamp(message['time'])
            dt = dt.strftime('%H:%M')
            self.textBrowser.append(dt + ' ' + message['name'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(
                self.host + '/messages',
                params={'after': self.after}
            )
        except:
            return

        messages = response.json()['messages']
        if len(messages) > 0:
            self.show_messages(messages)
            self.after = messages[-1]['time']

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                self.host + '/send',
                json={'name': name, 'text': text}
            )
        except:
            self.textBrowser.append('Сервер недоступен')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Сообщение не отправлено')
            self.textBrowser.append('Проверьте имя и текст')
            self.textBrowser.append('')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = ExampleApp('http://ee3b3f686502.ngrok.io/')
window.show()
app.exec()
