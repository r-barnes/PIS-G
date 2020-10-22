from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MatplotlibWidget import MatplotlibWidget

class Dialog(QDialog):
    def __init__(self, parent):
        super(Dialog, self).__init__(parent)
        self.father = parent
        #绘制
        layout = QVBoxLayout()
        label = QLabel(self)
        label.setText("Please Choose Variable to Paint")#请选择需要绘制的测线
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1)
        #获取表格
        tableWidget = self.father.tableWidget
        groupBox = QGroupBox("Variable")
        groupBox.setFlat(True)
        self.button=[]
        for i in range(1, tableWidget.lieCount+1):
            if tableWidget.item(0, i).text()=="X" or tableWidget.item(0, i).text()=="Y" or tableWidget.item(0, i).text()=="x" or tableWidget.item(0, i).text()=="y":
                continue
            bt = QCheckBox(tableWidget.item(0, i).text())
            self.button.append(bt)
        layoutCenter = QHBoxLayout()
        for i in range(0, len(self.button)):
            layoutCenter.addWidget(self.button[i])
        groupBox.setLayout(layoutCenter)
        layout.addWidget(groupBox, 3)
        #添加选项
        label1 = QLabel()
        label1.setText("X axis unit:")
        label2 = QLabel()
        label2.setText("V axis unit:")
        label3 = QLabel()
        label3.setText("Show Symbol:")#是否标注测点
        
        self.cb1 = QComboBox(self)
        self.cbItems1 = ["m", 'km']
        self.cb1.addItems(self.cbItems1)#添加下拉选项
        self.cb2 = QComboBox(self)
        self.cbItems2 = ['g.u.', 'E', 'mGal']
        self.cb2.addItems(self.cbItems2)#添加下拉选项
        self.cb3 = QComboBox(self)
        cbItems3 = ['No', 'Yes']
        self.cb3.addItems(cbItems3)#添加下拉选项
        layout1 = QHBoxLayout()
        layout1.addWidget(label1)
        layout1.addWidget(self.cb1)
        layout1.addWidget(label2)
        layout1.addWidget(self.cb2)
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(label3, 2)
        layout2.addWidget(self.cb3, 1)
        layout2.addStretch(2)
        
        #添加按钮
        layoutBottom = QHBoxLayout()
        layoutBottom.addStretch(5)
        ok = QPushButton("OK", self)
        cancel = QPushButton("Cancel", self)
        layoutBottom.addWidget(ok, 10)
        layoutBottom.addStretch(20)
        layoutBottom.addWidget(cancel, 10)
        layoutBottom.addStretch(5)
        layout.addLayout(layout1, 1)
        layout.addLayout(layout2, 1)
        layout.addStretch(1)
        layout.addLayout(layoutBottom, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Choose Variable to Paint")
        #去掉问号
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        #信号槽
        ok.clicked.connect(self.on_ok_clicked)
        cancel.clicked.connect(self.on_cancel_clicked)
        
    #ok
    def on_ok_clicked(self):
        position = self.father.tab.currentIndex()#当前Tab页索引
        tableWidget = self.father.tableWidget
        index = self.father.index
        #绘制剖面图
        #获取X的位置
        xposition=tableWidget.xcol
        fileName=[]
        y=[]
        for i in range(0, len(self.button)):
            if self.button[i].isChecked()==True:
                fileName.append(self.button[i].text())
                #获取当前侧线的位置
                vposition=0
                for k in range(1, tableWidget.lieCount+1):
                    if tableWidget.item(0, k).text()==self.button[i].text():
                        vposition=k
                        break
                for j in range(1, tableWidget.hangCount+1):
                    try:
                        y.append(float(tableWidget.item(j, vposition).text()))
                    except ValueError:
                        QMessageBox.information(self, "Error", "("+str(j)+", "+str(vposition)+") cannot be converted into numbers")
                        return
        if len(fileName)==0:
            return
        x=[]
        for i in range(1, tableWidget.hangCount+1):
            try:
                x.append(float(tableWidget.item(i, xposition).text()))
            except ValueError:
                QMessageBox.information(self, "Error", "("+str(i)+", "+str(xposition)+") cannot be converted into numbers")
                return
        #此处获得的数据：1、x列表；2、y列表；3、图名；4、x单位；5、V轴单位;6、是否测点
        xunit = self.cbItems1[self.cb1.currentIndex()]
        vunit = self.cbItems2[self.cb2.currentIndex()]
        flag = self.cb3.currentIndex()#显示测点，1为显示，0为不显示
        
        if xunit == 'km':
            x = [i / 1000 for i in x]
        
        mw = MatplotlibWidget()
        mw.mpl.section(tableWidget.cb.currentIndex()+1, fileName, x, y, xunit, vunit, flag)
        
        stringName = ""
        for i in range(0, len(fileName)-1):
            stringName = stringName + fileName[i] + "+"
        stringName += fileName[len(fileName)-1]
        finalName = stringName + " Profile"
        #更改 tree_record 的值
        root = self.father.tree.topLevelItem(position-1)
        child_name = 'view_'+str(self.father.paintCount[position-1]) 
        root_name = root.text(0)
        # 判断重名
        order = 1
        flag_0 = 0
        name_temp = finalName
        while flag_0 == 0:
            flag_0 = 1
            for key, value in self.father.tree_record[root_name].items():
                if 'tree_name' not in self.father.tree_record[root_name][key]:
                    flag_0 = 2
                    continue
                if name_temp == self.father.tree_record[root_name][key]['tree_name']:
                    flag = 0
                    break
            if flag_0 ==2:    continue
            if flag_0 == 1:    finalName = name_temp
            name_temp = finalName + '_' +str(order)
            order = order + 1
        
        self.father.tree_record[root_name][child_name] = {'tree_name':finalName,'paint_name':fileName,'type':'Paint_Section', \
        'currentIndex':str(tableWidget.cb.currentIndex()+1),  'X_axis_unit':xunit, 'V_axis_unit':vunit, 'Show_Symbol':flag, \
        'index':index}
        self.father.paintCount[position-1] = self.father.paintCount[position-1] +1
        #添加绘图信息
        #添加子树
        
        newItem = QTreeWidgetItem(root)
        newItem.setText(0, finalName)
        #设置子窗口
        sub = QMdiSubWindow()
        sub.setWindowIcon(QIcon(".\\image\\logo.png"))
        sub.setWidget(mw)
        sub.setWindowTitle(finalName)
        self.father.tab.widget(position).addSubWindow(sub)
        self.father.tab.widget(position).setActiveSubWindow(sub)
        sub.show()
        #设置树上root为选中状态
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)
        newItem.setSelected(1)
        root.setSelected(0)
        self.close()
        
        
    #cancel
    def on_cancel_clicked(self):
        self.close()
        
        
        
        
        
        
        
        
        
