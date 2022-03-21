from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np
import yaml
import csv
import re


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 173)
        self.data_progress = QtWidgets.QProgressBar(MainWindow)
        self.data_progress.setGeometry(QtCore.QRect(10, 130, 511, 23))
        self.data_progress.setProperty("value", 0)
        self.data_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.data_progress.setObjectName("data_progress")
        self.calc_data_button = QtWidgets.QPushButton(MainWindow)
        self.calc_data_button.setGeometry(QtCore.QRect(160, 70, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.calc_data_button.setFont(font)
        self.calc_data_button.setStyleSheet("background-color: rgb(57, 177, 20);\n"
"color: rgb(255, 255, 255);")
        self.calc_data_button.setObjectName("calc_data_button")
        self.multiple_check = QtWidgets.QCheckBox(MainWindow)
        self.multiple_check.setGeometry(QtCore.QRect(10, 30, 111, 31))
        self.multiple_check.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.multiple_check.setChecked(True)
        self.multiple_check.setObjectName("multiple_check")
        self.template_box = QtWidgets.QComboBox(MainWindow)
        self.template_box.setGeometry(QtCore.QRect(400, 70, 121, 31))
        self.template_box.setObjectName("template_box")
        self.file_start_select = QtWidgets.QToolButton(MainWindow)
        self.file_start_select.setGeometry(QtCore.QRect(490, 10, 31, 21))
        self.file_start_select.setObjectName("file_start_select")
        self.file_start = QtWidgets.QLineEdit(MainWindow)
        self.file_start.setGeometry(QtCore.QRect(10, 10, 471, 21))
        self.file_start.setReadOnly(True)
        self.file_start.setObjectName("file_start")
        self.template_label = QtWidgets.QLabel(MainWindow)
        self.template_label.setGeometry(QtCore.QRect(400, 40, 121, 21))
        self.template_label.setAlignment(QtCore.Qt.AlignCenter)
        self.template_label.setObjectName("template_label")
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 60, 121, 48))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.SN_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.SN_layout.setContentsMargins(0, 0, 0, 0)
        self.SN_layout.setObjectName("SN_layout")
        self.last_SN_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.last_SN_label.setEnabled(True)
        self.last_SN_label.setObjectName("last_SN_label")
        self.SN_layout.addWidget(self.last_SN_label, 1, 0, 1, 1)
        self.first_SN_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.first_SN_label.setEnabled(True)
        self.first_SN_label.setObjectName("first_SN_label")
        self.SN_layout.addWidget(self.first_SN_label, 0, 0, 1, 1)
        self.first_SN_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.first_SN_input.setEnabled(True)
        self.first_SN_input.setObjectName("first_SN_input")
        self.SN_layout.addWidget(self.first_SN_input, 0, 1, 1, 1)
        self.last_SN_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.last_SN_input.setEnabled(True)
        self.last_SN_input.setObjectName("last_SN_input")
        self.SN_layout.addWidget(self.last_SN_input, 1, 1, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Custom Functions are below here
        self.file_start_select.clicked.connect(lambda: f.loaded_file())
        self.calc_data_button.clicked.connect(lambda: f.start())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "S2P --> Data"))
        self.calc_data_button.setText(_translate("MainWindow", "Calculate Data"))
        self.multiple_check.setToolTip(_translate("MainWindow", "<html><head/><body><p>Once checked the program wil iterate through each folder until the last SN</p></body></html>"))
        self.multiple_check.setText(_translate("MainWindow", "Mulitple S/N"))
        self.file_start_select.setText(_translate("MainWindow", "..."))
        self.file_start.setPlaceholderText(_translate("MainWindow", "Starting File..."))
        self.template_label.setText(_translate("MainWindow", "Template Selection:"))
        self.last_SN_label.setText(_translate("MainWindow", "Last SN:"))
        self.first_SN_label.setText(_translate("MainWindow", "First SN:"))


class archive():
    folder = ""
    masterList = []
    filterPass = True
    iL = 0.0
    middle = []


class funcs():
    def loaded_file(self):
        username = os.getlogin()
        base_d = "C:/Users/" + username + "/Desktop/"
        filename = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption="Select the Source Folder", directory=base_d)
        archive.folder = filename
        ui.file_start.setText(filename)

    def start(self):
        template_r = ui.template_box.currentText()
        template = temp_dict + template_r + ".yaml"
        with open(template, "r") as yam:
            key = yaml.safe_load(yam)
        yam.close()
        filt = key["filter"]
        location = os.path.abspath(os.path.dirname(__file__))
        folderArchive = location + "/data/" + str(filt) + ".csv"
        file_list = os.listdir(archive.folder)
        ui.data_progress.setMaximum(len(file_list))
        prog = 0
        limits = key["limits"]
        labels = key["labels"]
        for i in limits:
            archive.masterList.append([]) #First scalable factor. For the formatting at the end with the CSV this is needed
        archive.masterList.append([]) #This one is soley for adding the SN's to the top of the list
        archive.masterList[0].append("")
        archive.masterList.append([])
        archive.masterList[-1].append("")
        for test in limits:
            archive.masterList[test + 1].append(labels[test])
        for file in file_list:
            plot = re.search(r".s2p|.s3p|.s4p", file)
            if plot:
                archive.filterPass = True
                archive.iL = 0.0
                serial = self.serialGet(file)
                archive.masterList[0].append(serial)
                processedData = self.data_cleaner(file)
                for test in limits:
                    #finish in the morning. Make seperate func to handle all tests, pass them in ya dork
                    test_dict = key["limits"][test]
                    passed = self.limitTests(test_dict, test, processedData)
                    if not passed:
                        archive.filterPass = False
                    elif passed:
                        if not archive.filterPass:
                            continue
                        else:
                            continue
                if archive.filterPass:
                    passing = "PASS"
                else:
                    passing = "FAIL"
                archive.masterList[-1].append(passing)
            else:
                pass
            prog += 1
            ui.data_progress.setValue(prog)
        self.data_write(folderArchive)
        
    def limitTests(self, key, test, data):
        limitType = key['limitType']
        result = False
        if limitType == '1dB':
            result = self.test1dB(key, test, data)
        elif limitType == 'Slope':
            result = self.testSlope(key, test, data)
        elif limitType == 'FCROSS':
            result = self.testFCROSS(key, test, data)
        elif limitType == 'Min' or 'Max':
            result = self.testMinMax(key, test, data)
        return result

    def testMinMax(self, key, test, data):
        passing = False
        values = key['vals']
        limitType = key['limitType']
        keeper = [] #Holds the first columns data
        if values == 1:
            stop1 = 0
            stop2 = key['val1'] * 1000000
        if values == 2:
            stop1 = key['val1'] * 1000000
            stop2 = key['val2'] * 1000000
        limit = float(key['limit'])
        column = key['column']
        placeList = []
        for col in column: #scaling factor for number of columns selected. Works for all SP files
            keeper.append(placeList.copy())
        placeList.clear()
        dbcCheck = key['dBc']
        for line in data:
            lineData = float(line[0])
            if lineData > stop1 and lineData < stop2:
                for col in column:
                    ind = column.index(col)
                    keeper[ind].append(abs(float(line[col])))
        #Everything should be set up for the final calculation
        if limitType == "Max":
            resultList = []
            for col in column:
                ind = column.index(col)
                loopResult = max(keeper[ind])
                resultList.append(loopResult)
            result = round(abs(max(resultList)), 2)
            resultList.clear()
            if dbcCheck == "template":
                archive.iL = result
            if dbcCheck == "use":
                result = round(result - archive.iL, 2)
            if result < limit:
                archive.masterList[test + 1].append(result)
                passing = True
            else:
                archive.masterList[test + 1].append("*" + (str(result) + "*"))
                passing = False
        if limitType == "Min":
            resultList = []
            for col in column:
                ind = column.index(col)
                loopResult = min(keeper[ind])
                resultList.append(loopResult)
            result = round(abs(min(resultList)), 2)
            resultList.clear()
            if dbcCheck == "template":
                archive.iL = result
            if dbcCheck == "use":
                result = round(result - archive.iL, 2)
            if result > limit:
                archive.masterList[test + 1].append(result)
                passing = True
            else:
                archive.masterList[test + 1].append("*" + (str(result) + "*"))
                passing = False
        return passing

    def test1dB(self, key, test, data):
        values = key['vals']
        keeper1 = [] #Holds the first columns data
        keeper2 = [] #Holds the second used columns data
        ilKeeper1 = []
        ilKeeper2 = []
        limit = key["limit"] * 1000000
        stop1 = key["val1"] * 1000000
        column = key['column']
        keeper = 1
        passing = False
        placeList = []
        for col in column: #scaling factor for number of columns selected. Works for all SP files
            keeper1.append(placeList.copy())
            keeper2.append(placeList.copy())
        placeList.clear()
        for line in data:
            keeper[len(column) + 1].append(float(line[0]))
        freq = self.minimumFind(keeper[len(column) + 1], limit)
        keeper[len(column) + 1].clear()
        for line in data:
            if keeper == 1:
                keeper1.append(line)
                resultList = []
                for col in column:
                    ind = column.index(col)
                    loopResult = float(line[ind])
                    resultList.append(loopResult)
                il = round(min(resultList), 2)
                ilKeeper1.append(abs(il))
                resultList.clear()
            elif keeper == 2:
                resultList = []
                for col in column:
                    ind = column.index(col)
                    loopResult = float(line[ind])
                    resultList.append(loopResult)
                il = round(min(resultList), 2)
                ilKeeper2.append(abs(il))
                resultList.clear()
            lineData = float(line[0])
            if lineData == freq:
                resultList = []
                for col in column:
                    ind = column.index(col)
                    loopResult = float(line[ind])
                    resultList.append(loopResult)
                insertLoss = round(min(resultList), 2)
                archive.middle = [line[0], insertLoss]
                keeper = 2
        ilKeeper1.reverse()
        keeper1.reverse()
        if stop1 < limit:
            tempLoss = abs(archive.middle[1] - 1)
            check = self.minimumFind(ilKeeper1, tempLoss)
            for line in keeper1:
                resultList = []
                for col in column:
                    ind = column.index(col)
                    loopResult = float(line[ind])
                    resultList.append(loopResult)
                insertLoss = abs(round(min(resultList), 2))
                if insertLoss == check:
                    result = float(line[0])
                    if result <= stop1:
                        result = round(result / 1000000, 0)
                        archive.masterList[test + 1].append(result)
                        passing = True
                        break
                    else:
                        result = round(result / 1000000, 0)
                        archive.masterList[test + 1].append("*" + (str(result) + "*"))
                        passing = False
                        break
            return passing
        if stop1 > limit:
            tempLoss = abs(archive.middle[1] - 1)
            check = self.minimumFind(ilKeeper2, tempLoss)
            for line in keeper2:
                resultList = []
                for col in column:
                    ind = column.index(col)
                    loopResult = float(line[ind])
                    resultList.append(loopResult)
                insertLoss = abs(round(min(resultList), 2))
                if insertLoss == check:
                    result = float(line[0])
                    if result >= stop1:
                        result = round(result / 1000000, 0)
                        archive.masterList[test + 1].append(result)
                        passing = True
                        break
                    else:
                        result = round(result / 1000000, 0)
                        archive.masterList[test + 1].append("*" + (str(result) + "*"))
                        passing = False
                        break
            return passing

    def testSlope(self, key, test, data):
        keeper = []
        limit = float(key['limit'])
        stop1 = key["val1"] * 1000000
        stop2 = key["val2"] * 1000000
        column = key['column']
        placeList = []
        for col in column: #scaling factor for number of columns selected. Works for all SP files
            keeper.append(placeList.copy())
        placeList.clear()
        for line in data:
            lineData = float(line[0])
            if lineData > stop1 and lineData < stop2:
                for col in column:
                    ind = column.index(col)
                    keeper[ind].append(float(line[col]))
        resultList = []
        for col in column:
            ind = column.index(col)
            loopResult1 = abs(max(keeper[ind]))
            loopResult2 = abs(min(keeper[ind]))
            loopResult = loopResult1 - loopResult2
            resultList.append(loopResult)
        result = round(abs(max(resultList)), 2)
        if result <= limit:
            archive.masterList[test + 1].append(result)
            passing = True
        else:
            archive.masterList[test + 1].append("*" + (str(result) + "*"))
            passing = False
        return passing
    
    def testFCROSS(self, key, test, data):
        passing = False
        keeper = []
        column = key['column']
        placeList = []
        for col in column: #scaling factor for number of columns selected. Works for all SP files
            keeper.append(placeList.copy())
        placeList.clear()
        resultList = []
        for line in data:
            for col in column:
                loopResult = float(line[col])
                resultList.append(loopResult)
        finder = max(resultList)
        resultList.clear()
        for line in data:
            for col in column:
                loopResult = float(line[col])
                if loopResult == finder:
                    result = float(line[0]) / 1000000000
                    result = round(result, 1)
                    archive.masterList[test + 1].append(result)
                    passing = True
                    return passing
        return passing


    def minimumFind(self, list, value):
        array = np.asarray(list)
        result = (np.abs(array - value)).argmin()
        return array[result]

    def serialGet(self, filename):
        serial = re.findall(r"SN\d+\d", filename)
        serial = re.sub("SN", "", serial[0])
        return serial

    def data_cleaner(self, file):
        processed_data = []
        with open(archive.folder + "/" + file, "r", encoding="UTF-8") as raw:
            lines = raw.readlines()
            raw.close()
        full = []
        if re.search(r".s3p", file): #used for s3p only, s2p and s1p are in the else section
            for line in lines:
                if re.search(r"#|!", line): #checks to see if any of the header information is in the line, if so it skips
                    continue
                sorted = line.split(" ")
                if len(full) == 0 and len(sorted) == 7:
                    for item in sorted:
                        full.append(item)
                    continue
                elif len(full) == 7:
                    for item in sorted:
                        full.append(item)
                    continue
                elif len(full) == 13:
                    for item in sorted:
                        full.append(item)
                    processed_data.append(full.copy())
                    full.clear() #I dont even want to know how difficult s4p files are going to be
                    continue
        else:
            for line in lines:
                if re.search(r"#|!", line):
                        continue
                sorted = line.split(" ")
                processed_data.append(sorted)
        return processed_data

    def data_write(self, savedata):
        with open(savedata, "a", encoding="UTF-8") as csv_output:
            writer = csv.writer(csv_output)
            for dataList in archive.masterList:
                writer.writerow(dataList)
        csv_output.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    f = funcs()
    temp_dict = os.path.abspath(os.path.dirname(__file__)) + "/templates/"
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    temps = os.listdir(temp_dict)
    for items in temps:
        items = items.split(".")
        ui.template_box.addItem(items[0])
    MainWindow.show()
    sys.exit(app.exec_())