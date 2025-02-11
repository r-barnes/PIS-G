from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MatplotlibWidget import MatplotlibWidget

class DialogGrid(QDialog):
    def __init__(self, parent):
        super(DialogGrid, self).__init__(parent)
        self.father = parent
        
        layout = QVBoxLayout()
        
        label = QLabel(self)
        label.setText("Please Choose the Variable to Paint")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        
        tableWidget = self.father.tableWidget
        groupBox = QGroupBox("Variable")
        groupBox.setFlat(True)
        self.button=[]
        for i in range(1, tableWidget.lieCount+1):
            if tableWidget.item(0, i).text()=="X" or tableWidget.item(0, i).text()=="Y" or tableWidget.item(0, i).text()=="x" or tableWidget.item(0, i).text()=="y":
                continue
            bt = QRadioButton(tableWidget.item(0, i).text())
            self.button.append(bt)
        layoutCenter = QHBoxLayout()
        for i in range(0, len(self.button)):
            layoutCenter.addWidget(self.button[i])
        groupBox.setLayout(layoutCenter)
        layout.addWidget(groupBox, 3)
        layout.addStretch(1)
       
        label1 = QLabel()
        label1.setText("Color Bar Title：")
        label2 = QLabel()
        label2.setText("Show Isoline")
        label3 = QLabel()
        label3.setText("Show Value")
        label4 = QLabel()
        label4.setText("X axis unit:")
        label5 = QLabel()
        label5.setText("Y axis unit:")
        
        self.le = QLineEdit()
        self.cb1 = QComboBox(self)
        self.cbItems1 = ['No', 'Yes']
        self.cb1.addItems(self.cbItems1)
        self.cb2 = QComboBox(self)
        self.cbItems2 = ['No', 'Yes']
        self.cb2.addItems(self.cbItems2)
        self.cb3 = QComboBox(self)
        self.cbItems3 = ['m', 'km']
        self.cb3.addItems(self.cbItems3)
        self.cb4 = QComboBox(self)
        self.cbItems4 = ['m', 'km']
        self.cb4.addItems(self.cbItems4)
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(label1, 2)
        layout1.addWidget(self.le, 2)
        layout1.addStretch(1)
        layout2 = QHBoxLayout()
        layout2.addWidget(label2)
        layout2.addWidget(self.cb1)
        layout2.addWidget(label3)
        layout2.addWidget(self.cb2)
        layout3 = QHBoxLayout()
        layout3.addWidget(label4)
        layout3.addWidget(self.cb3)
        layout3.addWidget(label5)
        layout3.addWidget(self.cb4)
        layout.addLayout(layout1, 1)
        layout.addLayout(layout2, 1)
        layout.addLayout(layout3, 1)
        layout.addStretch(1)
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 10)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(cancel, 10)
        layoutBottom.addStretch(5)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Choose Variable to Paint")
        
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        ok.clicked.connect(self.on_ok_clicked)
        cancel.clicked.connect(self.on_cancel_clicked)
        
    def on_ok_clicked(self):
        
        position = self.father.tab.currentIndex()
        tableWidget = self.father.tableWidget
        index = self.father.index
        
        xposition=tableWidget.xcol
        yposition=tableWidget.ycol
        fileName=""
        x=[]
        y=[]
        z=[]
        vposition=0
        for i in range(0, len(self.button)):
            if self.button[i].isChecked()==True:
                
                for k in range(1, tableWidget.lieCount+1):
                    if tableWidget.item(0, k).text()==self.button[i].text():
                        vposition=k
                        break
                fileName += self.button[i].text()
                for j in range(0,  len(tableWidget.data)):
                    try:
                        z.append(float(tableWidget.data[j][vposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(vposition)+") cannot be converted into numbers")
                        return
                    try:
                        if float(tableWidget.data[j][yposition-1]) not in y:
                            y.append(float(tableWidget.data[j][yposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(yposition)+") cannot be converted into numbers")
                        return
                    try:
                        if float(tableWidget.data[j][xposition-1]) not in x:
                            x.append(float(tableWidget.data[j][xposition-1]))
                    except ValueError:
                        QMessageBox.information(self, "Error", "Variable "+str(int(j*tableWidget.lineNumber/len(tableWidget.data))+1)+" ("+\
                        str(int(j-int(j*tableWidget.lineNumber/len(tableWidget.data))*len(tableWidget.data)/tableWidget.lineNumber+1))+", "+\
                        str(xposition)+") cannot be converted into numbers")
                        return
        if fileName=="":
            return            
        
        xunit = self.cbItems3[self.cb3.currentIndex()]
        yunit = self.cbItems4[self.cb4.currentIndex()]
        colorbarTitle = self.le.text()
        flag1 = self.cb1.currentIndex()
        flag2 = self.cb2.currentIndex()
        if xunit == 'km':
            x = [i / 1000 for i in x]
        if yunit == 'km':
            y = [i / 1000 for i in y]
        
        mw = MatplotlibWidget()
        mw.mpl.gridPaint(fileName, x, y, z, xunit, yunit, colorbarTitle, flag1, flag2)
        
        finalName = fileName + " Grid"
        
        sub = QMdiSubWindow()
        sub.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub.setWidget(mw)
        
        self.father.tab.widget(position).addSubWindow(sub)
        self.father.tab.widget(position).setActiveSubWindow(sub)
        sub.show()
        
        root = self.father.tree.topLevelItem(position-1)
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        
        order = 1
        flag = 0
        name_temp = finalName
        while flag == 0:
            flag = 1
            for key, value in self.father.tree_record[root_name].items():
                if 'tree_name' not in self.father.tree_record[root_name][key]:
                    flag = 2
                    continue
                if name_temp == self.father.tree_record[root_name][key]['tree_name']:
                    flag = 0
                    break
            if flag ==2:    continue
            if flag == 1:    finalName = name_temp
            name_temp = finalName + '_' +str(order)
            order = order + 1
            
        sub.setWindowTitle(finalName)
        newItem = QTreeWidgetItem(root)
        newItem.setText(0, finalName)
        
        self.father.tree_record[root_name][child_name] ={'tree_name':finalName,'paint_name':fileName,'type':'Paint_Gird', \
        'color_Bar_Title':str(colorbarTitle), 'Show_Isoline':str(flag1), 'Show_Value':str(flag2), \
        'X_axis_unit':str(xunit), 'Y_axis_unit':str(yunit), 'Choose':str(vposition), 'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)
        newItem.setSelected(1)
        root.setSelected(0)
        self.close()

    def on_cancel_clicked(self):
        self.close()
