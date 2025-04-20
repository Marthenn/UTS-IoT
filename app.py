import os
import threading
from dotenv import load_dotenv

from PyQt5 import QtCore, QtGui, QtWidgets

from utils.mongodb import MongoDBHandler
from utils.mqtt import MQTTHandler
from utils.image import ImageReconstructor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1780, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(1780, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1780, 1000))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1780, 1000))
        self.centralwidget.setMaximumSize(QtCore.QSize(1780, 1000))
        self.centralwidget.setObjectName("centralwidget")
        self.image_original = QtWidgets.QLabel(self.centralwidget)
        self.image_original.setGeometry(QtCore.QRect(120, 100, 640, 480))
        self.image_original.setObjectName("image_original")
        self.image_received = QtWidgets.QLabel(self.centralwidget)
        self.image_received.setGeometry(QtCore.QRect(1000, 100, 640, 480))
        self.image_received.setObjectName("image_received")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 10, 641, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1000, 10, 631, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 630, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 690, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.loops_input = QtWidgets.QComboBox(self.centralwidget)
        self.loops_input.setGeometry(QtCore.QRect(30, 870, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.loops_input.setFont(font)
        self.loops_input.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.loops_input.setObjectName("loops_input")
        self.loops_input.addItem("")
        self.loops_input.addItem("")
        self.loops_input.addItem("")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(30, 930, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.send_button.setFont(font)
        self.send_button.setObjectName("send_button")
        self.interval_label = QtWidgets.QLabel(self.centralwidget)
        self.interval_label.setGeometry(QtCore.QRect(640, 630, 781, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.interval_label.setFont(font)
        self.interval_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.interval_label.setObjectName("interval_label")
        self.latency_esp_db_label = QtWidgets.QLabel(self.centralwidget)
        self.latency_esp_db_label.setGeometry(QtCore.QRect(640, 690, 781, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.latency_esp_db_label.setFont(font)
        self.latency_esp_db_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.latency_esp_db_label.setObjectName("latency_esp_db_label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 750, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.latency_db_dashboard_label = QtWidgets.QLabel(self.centralwidget)
        self.latency_db_dashboard_label.setGeometry(QtCore.QRect(640, 750, 781, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.latency_db_dashboard_label.setFont(font)
        self.latency_db_dashboard_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.latency_db_dashboard_label.setObjectName("latency_db_dashboard_label")
        self.latency_total_label = QtWidgets.QLabel(self.centralwidget)
        self.latency_total_label.setGeometry(QtCore.QRect(640, 810, 781, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.latency_total_label.setFont(font)
        self.latency_total_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.latency_total_label.setObjectName("latency_total_label")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 810, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dashboard UTS IoT"))
        self.image_original.setText(_translate("MainWindow", "Original Image"))
        self.image_received.setText(_translate("MainWindow", "Received Image"))
        self.label.setText(_translate("MainWindow", "Original Image"))
        self.label_2.setText(_translate("MainWindow", "Received Image"))
        self.label_3.setText(_translate("MainWindow", "Avg. Interval"))
        self.label_4.setText(_translate("MainWindow", "Avg. Latency ESP --> DB"))
        self.loops_input.setItemText(0, _translate("MainWindow", "10"))
        self.loops_input.setItemText(1, _translate("MainWindow", "20"))
        self.loops_input.setItemText(2, _translate("MainWindow", "100"))
        self.send_button.setText(_translate("MainWindow", "Kirim Perintah"))
        self.interval_label.setText(_translate("MainWindow", "xxx ms"))
        self.latency_esp_db_label.setText(_translate("MainWindow", "xxx ms"))
        self.label_5.setText(_translate("MainWindow", "Avg. Latency DB --> Dashboard"))
        self.latency_db_dashboard_label.setText(_translate("MainWindow", "xxx ms"))
        self.latency_total_label.setText(_translate("MainWindow", "xxx ms"))
        self.label_6.setText(_translate("MainWindow", "Avg. Latency Total"))

        image_pixmap_original = QtGui.QPixmap("images/img.jpg")
        self.image_original.setPixmap(image_pixmap_original)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    load_dotenv()

    # MongoDB connection
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_db = os.getenv("MONGODB_DB")
    mongo_collection = os.getenv("MONGODB_COLLECTION")
    mongo_handler = MongoDBHandler(mongo_uri, mongo_db, mongo_collection)
    mongo_handler.connect()

    # MQTT connection
    mqtt_broker = os.getenv("MQTT_URL")
    mqtt_port = int(os.getenv("MQTT_PORT"))
    mqtt_pub_topic = os.getenv("MQTT_PUB_TOPIC")
    mqtt_sub_topic = os.getenv("MQTT_SUB_TOPIC")
    mqtt_username = os.getenv("MQTT_USERNAME")
    mqtt_password = os.getenv("MQTT_PASSWORD")
    mqtt_handler = MQTTHandler(
        mqtt_broker,
        mqtt_port,
        mqtt_username,
        mqtt_password,
        mongo_handler
    )
    mqtt_handler.subscribe(mqtt_sub_topic)

    # Image reconstruction
    xor_key = int(os.getenv("XOR_KEY"), 16)
    image_reconstructor = ImageReconstructor(mongo_handler, xor_key)
    image_reconstructor.image_reconstructed.connect(lambda pixmap: ui.image_received.setPixmap(pixmap))
    image_reconstructor.avg_latency_updated.connect(lambda esp, db, total: (
        ui.latency_esp_db_label.setText(f"{esp} s"),
        ui.latency_db_dashboard_label.setText(f"{db} s"),
        ui.latency_total_label.setText(f"{total} s")
    ))
    image_reconstructor.interval_between_loops_emitted.connect(lambda interval: ui.interval_label.setText(f"{interval} s"))

    ui.send_button.clicked.connect(lambda: (
        mqtt_handler.publish(
            mqtt_pub_topic,
            payload=ui.loops_input.currentText(),
            qos=1
        ),
        ui.image_received.setText("Received Image")
    ))

    mongo_handler.observe_changes(image_reconstructor.process_new_document)
    mqtt_thread = threading.Thread(target=mqtt_handler.start)
    mqtt_thread.start()

    MainWindow.show()
    sys.exit(app.exec_())
