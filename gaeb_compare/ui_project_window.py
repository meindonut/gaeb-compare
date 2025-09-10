# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTableView, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1293, 977)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionLinksCreate = QAction(MainWindow)
        self.actionLinksCreate.setObjectName(u"actionLinksCreate")
        self.actionLinksLoad = QAction(MainWindow)
        self.actionLinksLoad.setObjectName(u"actionLinksLoad")
        self.actionLinksSave = QAction(MainWindow)
        self.actionLinksSave.setObjectName(u"actionLinksSave")
        self.actionDifflib = QAction(MainWindow)
        self.actionDifflib.setObjectName(u"actionDifflib")
        self.actionDifflib.setCheckable(True)
        self.actionDifflib.setChecked(True)
        self.actionGoogle = QAction(MainWindow)
        self.actionGoogle.setObjectName(u"actionGoogle")
        self.actionGoogle.setCheckable(True)
        self.actionSynchron = QAction(MainWindow)
        self.actionSynchron.setObjectName(u"actionSynchron")
        self.actionSynchron.setCheckable(True)
        self.actionSynchron.setChecked(True)
        self.actionName = QAction(MainWindow)
        self.actionName.setObjectName(u"actionName")
        self.actionName.setCheckable(True)
        self.actionName.setChecked(False)
        self.actionSim = QAction(MainWindow)
        self.actionSim.setObjectName(u"actionSim")
        self.actionSim.setCheckable(True)
        self.actionSim.setEnabled(False)
        self.actionLinked = QAction(MainWindow)
        self.actionLinked.setObjectName(u"actionLinked")
        self.actionLinked.setCheckable(True)
        self.actionProperties = QAction(MainWindow)
        self.actionProperties.setObjectName(u"actionProperties")
        self.actionGoogle_2 = QAction(MainWindow)
        self.actionGoogle_2.setObjectName(u"actionGoogle_2")
        self.actionGoogle_2.setCheckable(True)
        self.actionDifflib_2 = QAction(MainWindow)
        self.actionDifflib_2.setObjectName(u"actionDifflib_2")
        self.actionDifflib_2.setCheckable(True)
        self.actionDifflib_2.setChecked(False)
        self.actionLv = QAction(MainWindow)
        self.actionLv.setObjectName(u"actionLv")
        self.actionLv_plus = QAction(MainWindow)
        self.actionLv_plus.setObjectName(u"actionLv_plus")
        self.actionLvImport = QAction(MainWindow)
        self.actionLvImport.setObjectName(u"actionLvImport")
        self.actionAsc = QAction(MainWindow)
        self.actionAsc.setObjectName(u"actionAsc")
        self.actionAsc.setCheckable(True)
        self.actionAsc.setChecked(False)
        self.actionDsc = QAction(MainWindow)
        self.actionDsc.setObjectName(u"actionDsc")
        self.actionDsc.setCheckable(True)
        self.actionDsc.setChecked(False)
        self.actionAutomatisch = QAction(MainWindow)
        self.actionAutomatisch.setObjectName(u"actionAutomatisch")
        self.actionAutomatisch.setCheckable(True)
        self.actionAutomatisch.setChecked(True)
        self.actionAlles_ausklappen = QAction(MainWindow)
        self.actionAlles_ausklappen.setObjectName(u"actionAlles_ausklappen")
        self.actionSuchen = QAction(MainWindow)
        self.actionSuchen.setObjectName(u"actionSuchen")
        self.actionSuchen_Alle = QAction(MainWindow)
        self.actionSuchen_Alle.setObjectName(u"actionSuchen_Alle")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.treeView = QTreeView(self.verticalLayoutWidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_3.addWidget(self.treeView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.pushButtonAdd = QPushButton(self.verticalLayoutWidget)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_2.addWidget(self.pushButtonAdd, 0, Qt.AlignmentFlag.AlignRight)

        self.pushButtonDelete = QPushButton(self.verticalLayoutWidget)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout_2.addWidget(self.pushButtonDelete, 0, Qt.AlignmentFlag.AlignRight)

        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.tableView = QTableView(self.verticalLayoutWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_3.addWidget(self.tableView)

        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout_3.setStretch(3, 1)
        self.splitter.addWidget(self.verticalLayoutWidget)
        self.horizontalLayoutWidget = QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title_left = QLabel(self.horizontalLayoutWidget)
        self.label_title_left.setObjectName(u"label_title_left")
        self.label_title_left.setFont(font)

        self.verticalLayout.addWidget(self.label_title_left)

        self.tableView_left = QTableView(self.horizontalLayoutWidget)
        self.tableView_left.setObjectName(u"tableView_left")

        self.verticalLayout.addWidget(self.tableView_left)

        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.textEdit_left = QPlainTextEdit(self.horizontalLayoutWidget)
        self.textEdit_left.setObjectName(u"textEdit_left")

        self.verticalLayout.addWidget(self.textEdit_left)

        self.pushButton_save = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.verticalLayout.addWidget(self.pushButton_save)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 3)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_title_right = QLabel(self.horizontalLayoutWidget)
        self.label_title_right.setObjectName(u"label_title_right")
        self.label_title_right.setFont(font)

        self.verticalLayout_2.addWidget(self.label_title_right)

        self.tableView_right = QTableView(self.horizontalLayoutWidget)
        self.tableView_right.setObjectName(u"tableView_right")

        self.verticalLayout_2.addWidget(self.tableView_right)

        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.textEdit_right = QPlainTextEdit(self.horizontalLayoutWidget)
        self.textEdit_right.setObjectName(u"textEdit_right")

        self.verticalLayout_2.addWidget(self.textEdit_right)

        self.verticalSpacer = QSpacerItem(10, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(3, 3)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.splitter.addWidget(self.horizontalLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1293, 33))
        self.menuProjekt = QMenu(self.menubar)
        self.menuProjekt.setObjectName(u"menuProjekt")
        self.menuAnsicht = QMenu(self.menubar)
        self.menuAnsicht.setObjectName(u"menuAnsicht")
        self.menuSortierung_Verkn_pfung = QMenu(self.menuAnsicht)
        self.menuSortierung_Verkn_pfung.setObjectName(u"menuSortierung_Verkn_pfung")
        self.menuDifferenz_Bibliothek = QMenu(self.menuAnsicht)
        self.menuDifferenz_Bibliothek.setObjectName(u"menuDifferenz_Bibliothek")
        self.menuBearbeiten = QMenu(self.menubar)
        self.menuBearbeiten.setObjectName(u"menuBearbeiten")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuProjekt.menuAction())
        self.menubar.addAction(self.menuBearbeiten.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menuProjekt.addAction(self.actionLvImport)
        self.menuProjekt.addAction(self.actionProperties)
        self.menuProjekt.addAction(self.actionExit)
        self.menuAnsicht.addAction(self.actionSynchron)
        self.menuAnsicht.addAction(self.menuSortierung_Verkn_pfung.menuAction())
        self.menuAnsicht.addAction(self.menuDifferenz_Bibliothek.menuAction())
        self.menuAnsicht.addAction(self.actionAlles_ausklappen)
        self.menuSortierung_Verkn_pfung.addAction(self.actionName)
        self.menuSortierung_Verkn_pfung.addAction(self.actionSim)
        self.menuSortierung_Verkn_pfung.addAction(self.actionLinked)
        self.menuSortierung_Verkn_pfung.addSeparator()
        self.menuSortierung_Verkn_pfung.addAction(self.actionAsc)
        self.menuSortierung_Verkn_pfung.addAction(self.actionDsc)
        self.menuDifferenz_Bibliothek.addAction(self.actionAutomatisch)
        self.menuDifferenz_Bibliothek.addAction(self.actionDifflib_2)
        self.menuDifferenz_Bibliothek.addAction(self.actionGoogle_2)
        self.menuBearbeiten.addAction(self.actionSuchen)
        self.menuBearbeiten.addAction(self.actionSuchen_Alle)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LV Pr\u00fcfer", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Ordner \u00f6ffnen", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Beenden", None))
        self.actionLinksCreate.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
        self.actionLinksLoad.setText(QCoreApplication.translate("MainWindow", u"Laden", None))
        self.actionLinksSave.setText(QCoreApplication.translate("MainWindow", u"Speichern", None))
        self.actionDifflib.setText(QCoreApplication.translate("MainWindow", u"difflibparser (schnell)", None))
        self.actionGoogle.setText(QCoreApplication.translate("MainWindow", u"google (pr\u00e4zise)", None))
        self.actionSynchron.setText(QCoreApplication.translate("MainWindow", u"Synchron scrollen", None))
        self.actionName.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.actionSim.setText(QCoreApplication.translate("MainWindow", u"\u00c4hnlichkeit", None))
        self.actionLinked.setText(QCoreApplication.translate("MainWindow", u"Verkn\u00fcpft", None))
        self.actionProperties.setText(QCoreApplication.translate("MainWindow", u"Eigenschaften", None))
        self.actionGoogle_2.setText(QCoreApplication.translate("MainWindow", u"google (pr\u00e4zise)", None))
        self.actionDifflib_2.setText(QCoreApplication.translate("MainWindow", u"difflibparser (schnell)", None))
        self.actionLv.setText(QCoreApplication.translate("MainWindow", u"1. Erzeuge \u00dcbersicht", None))
        self.actionLv_plus.setText(QCoreApplication.translate("MainWindow", u"2. Importiere LV", None))
        self.actionLvImport.setText(QCoreApplication.translate("MainWindow", u"LV importieren", None))
#if QT_CONFIG(shortcut)
        self.actionLvImport.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionAsc.setText(QCoreApplication.translate("MainWindow", u"Aufsteigend", None))
        self.actionDsc.setText(QCoreApplication.translate("MainWindow", u"Absteigend", None))
        self.actionAutomatisch.setText(QCoreApplication.translate("MainWindow", u"automatisch", None))
        self.actionAlles_ausklappen.setText(QCoreApplication.translate("MainWindow", u"Alles ausklappen", None))
        self.actionSuchen.setText(QCoreApplication.translate("MainWindow", u"Suchen", None))
#if QT_CONFIG(shortcut)
        self.actionSuchen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionSuchen_Alle.setText(QCoreApplication.translate("MainWindow", u"Suchen Alle", None))
#if QT_CONFIG(shortcut)
        self.actionSuchen_Alle.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+F", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Datenbank:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Verkn\u00fcpfungen:", None))
        self.pushButtonAdd.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_title_left.setText(QCoreApplication.translate("MainWindow", u"Basis:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Langtext:", None))
        self.pushButton_save.setText(QCoreApplication.translate("MainWindow", u"Speichern", None))
        self.label_title_right.setText(QCoreApplication.translate("MainWindow", u"Vergleich:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Langtext:", None))
        self.menuProjekt.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
        self.menuSortierung_Verkn_pfung.setTitle(QCoreApplication.translate("MainWindow", u"Sortierung Verkn\u00fcpfung", None))
        self.menuDifferenz_Bibliothek.setTitle(QCoreApplication.translate("MainWindow", u"Differenz-Bibliothek", None))
        self.menuBearbeiten.setTitle(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
    # retranslateUi

