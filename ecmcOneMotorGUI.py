import epics
import sys
from PyQt5 import QtWidgets, QtGui
from ecmcArrayStat import *

#Define pvs
# Axis
ECMC_PV_AXIS_DIAG_ARRAY_SUFFIX =       '-Array-Stat'
ECMC_PV_AXIS_ERROR_RESET_SUFFIX =      '-ErrRst'
# Controller
ECMC_PV_CNTROLLER_ERROR_ID_SUFFIX =    'MCU-ErrId'
ECMC_PV_CNTROLLER_ERROR_MSG_SUFFIX =   'MCU-ErrMsg'
ECMC_PV_CNTROLLER_ERROR_RESET_SUFFIX = 'MCU-ErrRst'
ECMC_PV_CNTROLLER_ERROR_CND_SUFFIX =   'MCU-Cmd'

BLANK = ' '*4
BACKGROUND_DEFAULT = '#efefef'
#BACKGROUND_DONE_MOVING = 'beige'
BACKGROUND_DONE_MOVING = BACKGROUND_DEFAULT
BACKGROUND_MOVING = 'lightgreen'
BACKGROUND_LVIO_ON = 'yellow'
BACKGROUND_LIMIT_ON = 'red'
TOOLTIPS = {
        'DESC': 'DESC: short description',
        'NAME': 'NAME: EPICS PV name',
        'RBV':  'RBV: motor readback value',
        'VAL':  'VAL: motor target value',
        'EGU':  'EGU: engineering units',
        'STOP': 'STOP: command this motor to stop moving',
        'TWV':  'TWV: tweak value',
        'TWF':  'TWF: increment motor by tweak value',
        'TWR':  'TWR: decrement motor by tweak value',
        '*10':  'multiply tweak value by 10',
        '/10':  'divide tweak value by 10',
        'CNEN': 'enable/disable drive'
}
STYLES = {      ### http://doc.qt.digia.com/qt/stylesheet-reference.html
    'self': '''
             MotorPanel { 
                border-style: solid;
                border-color: black;
                border-width: 1px;
             }
            ''',
    'DESC': '''
             QLabel { 
                qproperty-alignment: AlignCenter;
                color: white; 
                background-color: blue;
                font: bold;
             }
            ''',
    'NAME': '''
             QLabel { 
                qproperty-alignment: AlignCenter;
                color: darkblue; 
                background-color: lightgray;
                font: bold;
             }
            ''',
    'RBV': '''
             QLabel { 
                qproperty-alignment: AlignCenter;
             }
            ''',
    'EGU': '''
             QLabel { 
                qproperty-alignment: AlignCenter;
             }
            ''',
    'VAL': '''
            QLineEdit { 
                   background-color: beige;
                   text-align: left;
                   }
           ''',
    'STOP': '''
            QPushButton { 
                   background-color: red;
                   color: black;
                   text-align: center;
                   }
            QPushButton:hover { 
                   background-color: red;
                   color: yellow;
                   font: bold;
                   text-align: center;
                   }
            ''',
    'CNEN': '''
            QPushButton { 
                   background-color: red;
                   color: black;
                   text-align: center;
                   }
            QPushButton:hover { 
                   background-color: red;
                   color: yellow;
                   font: bold;
                   text-align: center;
                   }
            ''',
    'TWV': '''
            QLineEdit { 
                   background-color: lightgray;
                   text-align: left;
                   }
           ''',
    'TWF': '''
            QPushButton { 
                   width: 20px;
                   min-width: 20px;
                   max-width: 20px;
                   }
           ''',
    'TWR': '''
            QPushButton { 
                   width: 20px;
                   min-width: 20px;
                   max-width: 20px;
                   }
           ''',
    '*10': '''
            QPushButton { 
                   width: 20px;
                   min-width: 20px;
                   max-width: 20px;
                   }
           ''',
    '/10': '''
            QPushButton { 
                   width: 20px;
                   min-width: 20px;
                   max-width: 20px;
                   }
           ''',
}

class MotorPanel(QtWidgets.QDialog):
    
    def __init__(self, parent=None,iocPrefix=None,axisName=None):
        super(MotorPanel, self).__init__(parent)
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.motorPv = None
        self.motorPvName = ""
        self.axisDiagPvName=""
        self.axisErrorResetPv = None
        self.axisErrorResetPvName = ""
        self.cntrlErrorIdPv = None
        self.cntrlErrorIdPvName = ""
        self.cntrlErrorResetPv = None
        self.cntrlErrorResetPvName = ""
        self.cntrlErrorMsgPv = None
        self.cntrlErrorMsgPvName = ""
        self.cntrlErrorMsg=""
        self.cntrlCmdPv = None
        self.cntrlCmdPvName = ""
        self.create_GUI()
        self.apply_styles()
        self.create_actions()

        if isinstance(axisName, str) and  isinstance(iocPrefix, str):
            self.connect(iocPrefix,axisName)

    def create_GUI(self):
        '''define controls AND set the layout'''    
        self.controls = {}
        for field in ['DESC', 'NAME', 'EGU', 'RBV']:
            self.controls[field] = QtWidgets.QLabel(BLANK)
        self.controls['VAL'] = QtWidgets.QLineEdit()
        self.controls['STOP'] = QtWidgets.QPushButton('STOP',default=False, autoDefault=False)
        self.controls['TWF'] = QtWidgets.QPushButton('&gt;',default=False, autoDefault=False)
        self.controls['TWV'] = QtWidgets.QLineEdit()
        self.controls['TWR'] = QtWidgets.QPushButton('&lt;',default=False, autoDefault=False)
        self.controls['*10'] = QtWidgets.QPushButton('*',default=False, autoDefault=False)
        self.controls['/10'] = QtWidgets.QPushButton('/',default=False, autoDefault=False)
        self.controls['CNEN'] = QtWidgets.QPushButton('CNEN',default=False, autoDefault=False)
        
        self.controls['RBV'].setAutoFillBackground(True)
        self.setLabelBackground(self.controls['RBV'], BACKGROUND_DONE_MOVING)
        
        main_frame= QtWidgets.QFrame(self)
        main_layout = QtWidgets.QHBoxLayout()
   
        sub_frame = QtWidgets.QFrame(self)
        sub_layout = QtWidgets.QVBoxLayout()
        for field in ['DESC', 'NAME', 'EGU', 'RBV', 'VAL']:
            sub_layout.addWidget(self.controls[field])
        
        tweak_frame = QtWidgets.QFrame(self)
        tweak_layout = QtWidgets.QHBoxLayout()
        for field in ['TWR', '/10', 'TWV', '*10', 'TWF']:
            tweak_layout.addWidget(self.controls[field])
        tweak_frame.setLayout(tweak_layout)
        sub_layout.addWidget(tweak_frame)
        
        sub_layout.addWidget(self.controls['STOP'])
        sub_layout.addWidget(self.controls['CNEN'])

        sub_frame.setLayout(sub_layout)

        main_layout.addWidget(sub_frame)

        self.arrayStat=ecmcArrayStat(self)        
        self.arrayStat.setMinimumSize(200,200)
        main_layout.addWidget(self.arrayStat)
        
        main_frame.setLayout(main_layout)


        

        self.setLayout(main_layout)
        self.setWindowTitle("ECMC Motor panel")
        

    def apply_styles(self):
        '''apply styles and tips'''     
        for field in ['DESC', 'NAME', 'EGU', 'RBV', 'VAL', 
                      'STOP','CNEN','TWV', 'TWF', 'TWR', '*10', '/10']:
            if field in STYLES:
                self.controls[field].setStyleSheet(STYLES[field])
            if field in TOOLTIPS:
                self.controls[field].setToolTip(TOOLTIPS[field])
        
        self.setStyleSheet(STYLES['self'])

    def create_actions(self):
        '''define actions'''
        self.controls['VAL'].returnPressed.connect(self.onReturnVAL)
        self.controls['TWV'].returnPressed.connect(self.onReturnTWV)
        self.controls['TWR'].clicked.connect(self.onPushTWR)
        self.controls['TWF'].clicked.connect(self.onPushTWF)
        self.controls['*10'].clicked.connect(self.onPush10x)
        self.controls['/10'].clicked.connect(self.onPush_1x)
        self.controls['STOP'].clicked.connect(self.onPushSTOP)
        self.controls['CNEN'].clicked.connect(self.onPushCNEN)

    def setPvNames(self,iocPrefix=None,axisName=None):
        self.motorPvName = (iocPrefix + axisName).split('.')[0]  # keep everything to left of first dot
        self.axisDiagPvName = self.motorPvName + ECMC_PV_AXIS_DIAG_ARRAY_SUFFIX
        self.axisErrorResetPvName = self.motorPvName + ECMC_PV_AXIS_ERROR_RESET_SUFFIX
        self.cntrlErrorIdPvName = iocPrefix + ECMC_PV_CNTROLLER_ERROR_ID_SUFFIX
        self.cntrlErrorResetPvName = iocPrefix + ECMC_PV_CNTROLLER_ERROR_RESET_SUFFIX
        self.cntrlErrorMsgPvName = iocPrefix + ECMC_PV_CNTROLLER_ERROR_MSG_SUFFIX
        self.cntrlCmdPvName = iocPrefix + ECMC_PV_CNTROLLER_ERROR_CND_SUFFIX

    def connect(self, iocPrefix=None,axisName=None):
        '''connect this panel with an EPICS motor PV'''
        if iocPrefix is None:            
            raise RuntimeError("iocPrefix must not be 'None'")
        if axisName is None:            
            raise RuntimeError("axisName must not be 'None'")
        
        self.setPvNames(iocPrefix,axisName)

        if len(iocPrefix) == 0 or len(axisName) == 0:
            raise RuntimeError("iocPrefix or axisName must not be ''")
        
        if self.motorPv is not None:
            self.disconnect()
        
        self.controls['NAME'].setText(self.motorPvName)
        self.motorPv = epics.Motor(str(self.motorPvName))   # verifies that self.motor_pv has RTYP='motor'

        callback_dict = {
            #field:  callback function
            'DESC': self.onChangeDESC,
            'EGU':  self.onChangeEGU,
            'RBV':  self.onChangeRBV,
            'VAL':  self.onChangeVAL,
            'TWV':  self.onChangeTWV,
            'DMOV': self.onChangeDMOV,
            'HLS':  self.onChangeHLS,
            'LLS':  self.onChangeLLS,
            'CNEN': self.onChangeCNEN,
        }
        for field, func in callback_dict.items():
            self.motorPv.set_callback(attr=field, callback=func)

        self.controls['DESC'].setText(self.motorPv.description)
        self.controls['EGU'].setText(self.motorPv.units)
        
        # display initial values
        self.onChangeRBV(value=self.motorPv.get('RBV'))
        self.onChangeVAL(value=self.motorPv.get('VAL'))
        self.onChangeTWV(value=self.motorPv.get('TWV'))
        self.onChangeDMOV(value=self.motorPv.get('DMOV'))
        self.onChangeCNEN(value=self.motorPv.get('CNEN'))
        
        # additional records
        self.axisErrorResetPv = epics.PV(self.axisErrorResetPvName)
        self.cntrlErrorIdPv = epics.PV(self.cntrlErrorIdPvName)
        self.cntrlErrorIdPv.add_callback(self.onChangeCntrlErrorIdPv)
        self.cntrlErrorResetPv = epics.PV(self.cntrlErrorResetPvName)
        self.cntrlErrorMsgPv = epics.PV(self.cntrlErrorMsgPvName)
        self.cntrlCmdPv = epics.PV(self.cntrlCmdPvName)
        self.cntrlCmdPv.add_callback(self.onChangeCntrlCmdPv)
        if self.arrayStat is not None:
          self.arrayStat.connect(self.axisDiagPvName)

    def disconnect(self):
        '''disconnect this panel from EPICS'''
        if self.motorPv is not None:
            for field in ['VAL', 'RBV', 'DESC', 'EGU', 'TWV', 'DMOV', 'HLS', 'LLS']:
                self.motorPv.clear_callback(attr=field)
            #self.motorPv.disconnect()   # There is no disconnect() method!
            self.motorPv = None
            for field in ['DESC', 'NAME', 'EGU', 'RBV', 'VAL', 'TWV']:
                self.controls[field].setText(BLANK)

        if self.cntrlErrorIdPv is not None:
            self.cntrlErrorIdPv.clear_callbacks()
        if self.cntrlCmdPv is not None:
            self.cntrlCmdPv.clear_callbacks()

        if self.arrayStat is not None:
          self.arrayStat.disconnect()



    def closeEvent(self, event):
        '''be sure to disconnect from EPICS when closing'''
        self.disconnect()

    def onPushSTOP(self):
        '''stop button was pressed'''
        if self.motorPv is not None:
            self.motorPv.stop()

    def onPushCNEN(self):
        '''cnen button was pressed'''
        if self.motorPv is not None:
            self.motorPv.put('CNEN',not self.motorPv.get('CNEN'))

    def onPushTWF(self):
        '''tweak forward button was pressed'''
        if self.motorPv is not None:
            self.motorPv.put('TWF', 1)

    def onPushTWR(self):
        '''tweak reverse button was pressed'''
        if self.motorPv is not None:
            self.motorPv.put('TWR', 1)

    def onPush10x(self):
        '''multiply TWV*10 button was pressed'''
        if self.motorPv is not None:
            self.motorPv.put('TWV', 10*self.motorPv.get('TWV'))

    def onPush_1x(self):
        '''multiply TWV*0.1 button was pressed'''
        if self.motorPv is not None:
            self.motorPv.put('TWV', 0.1*self.motorPv.get('TWV'))

    def onReturnTWV(self):
        '''new target value was entered in this panel'''
        if self.motorPv is not None:
            number = float(self.controls['TWV'].text())
            self.motorPv.put('TWV', number)

    def onReturnVAL(self):
        '''new target value was entered in this panel'''
        if self.motorPv is not None:
            number = float(self.controls['VAL'].text())
            self.motorPv.move(number)

    def onChangeCNEN(self, value = None, **kws):
        '''EPICS monitor on DESC called this'''
        if value:
            self.controls['CNEN'].setStyleSheet("background-color: green")
        else:
            self.controls['CNEN'].setStyleSheet("background-color: red")

    def onChangeDESC(self, char_value=None, **kws):
        '''EPICS monitor on DESC called this'''
        self.controls['DESC'].setText(char_value)

    def onChangeDMOV(self, value = None, **kws):
        '''EPICS monitor on DMOV called this, change the color of the RBV label'''
        if value is not None:
            color = {1: BACKGROUND_DONE_MOVING, 0: BACKGROUND_MOVING}[value]
            self.setLabelBackground(self.controls['RBV'], color)

    def onChangeHLS(self, value=None, **kws):
        '''EPICS monitor on HLS called this, change the color of the TWF button'''
        if value is not None:
            color = {0: BACKGROUND_DEFAULT, 0: BACKGROUND_LIMIT_ON}[value]
            self.setLabelBackground(self.controls['TWF'], color)

    def onChangeLLS(self, value=None, **kws):
        '''EPICS monitor on LLS called this, change the color of the TWR button'''
        if value is not None:
            color = {0: BACKGROUND_DEFAULT, 0: BACKGROUND_LIMIT_ON}[value]
            self.setLabelBackground(self.controls['TWR'], color)

    def onChangeEGU(self, char_value=None, **kws):
        '''EPICS monitor on EGU called this'''
        self.controls['EGU'].setText(char_value)

    def onChangeRBV(self, value=None, **kws):
        '''EPICS monitor on RBV called this'''
        if value is not None:
            fmt = "%%.%df" % self.motorPv.get('PREC')
            self.controls['RBV'].setText(fmt % value)

    def onChangeTWV(self, value=None, **kws):
        '''EPICS monitor on TWV called this'''
        if value is not None:
            fmt = "%%.%df" % self.motorPv.get('PREC')
            self.controls['TWV'].setText(fmt % value)

    def onChangeVAL(self, value=None, **kws):
        '''EPICS monitor on VAL called this'''
        if value is not None:
            fmt = "%%.%df" % self.motorPv.get('PREC')
            self.controls['VAL'].setText(fmt % value)

    def onChangeCntrlErrorIdPv(self,pvname=None, value=None, char_value=None, **kw):
        print("onChangeCntrlErrorIdPv"+ char_value )
        self.cntrlErrorMsg=self.cntrlErrorMsgPv.get(as_string=True)
        print("new Error message: " +str(self.cntrlErrorMsg))

    def onChangeCntrlErrorMsgPv(self,pvname=None, value=None, char_value=None, **kw):
        print("onChangeCntrlErrorMsgPv:" + char_value)

    def onChangeCntrlCmdPv(self,pvname=None, value=None, char_value=None, **kw):
        print("onChangeCntrlCmdPv")

    def setLabelBackground(self, widget = None, color = BACKGROUND_DEFAULT):
        '''change the background color of a Qt widget'''
        if widget is not None:
            palette = QtGui.QPalette()
            palette.setColor(widget.backgroundRole(), QtGui.QColor(color))
            widget.setPalette(palette)


def main():
    '''demo: display the named motors in a horizontal block'''
    if len(sys.argv) != 2:
        raise RuntimeError ("usage: %s motor".format(sys.argv[0]))
    app = QtWidgets.QApplication(sys.argv)
    panel = MotorPanel(pvname=sys.argv[1])
    #panel.connect()
    panel.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()