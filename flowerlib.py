import maya.cmds as cmds
from PySide2 import QtCore, QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import math  


def get_maya_main_win():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class FlowerWin(QtWidgets.QDialog):
    """Flower Window Class"""

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.flower_generator = Flower()
        self.setWindowTitle("Flower Generator")
        self.resize(500, 300)
        self._mk_main_layout()
        self._connect_signals()

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_name_layout()
        self._mk_form_layout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _mk_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        self._add_stem_height()
        self._add_stem_width()  
        self._add_bud_size()
        self._add_petal_count()
        self._add_petal_scale()
        self.main_layout.addLayout(self.form_layout)

    def _add_stem_height(self):
        self.stem_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.stem_height_dspnbx.setValue(5.0)
        self.stem_height_dspnbx.setSingleStep(0.5)
        self.form_layout.addRow("Stem Height", self.stem_height_dspnbx)

    def _add_stem_width(self):  
        self.stem_width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.stem_width_dspnbx.setValue(0.1)
        self.stem_width_dspnbx.setSingleStep(0.01)
        self.form_layout.addRow("Stem Width", self.stem_width_dspnbx)

    def _add_bud_size(self):
        self.bud_size_dspnbx = QtWidgets.QDoubleSpinBox()
        self.bud_size_dspnbx.setValue(1.0)
        self.bud_size_dspnbx.setSingleStep(0.1)
        self.form_layout.addRow("Bud Size", self.bud_size_dspnbx)

    def _add_petal_count(self):
        self.petal_count_spnbx = QtWidgets.QSpinBox()
        self.petal_count_spnbx.setValue(5)
        self.form_layout.addRow("Petal Count", self.petal_count_spnbx)

    def _add_petal_scale(self):
        self.petal_scale_dspnbx = QtWidgets.QDoubleSpinBox()
        self.petal_scale_dspnbx.setValue(1.2)
        self.petal_scale_dspnbx.setSingleStep(0.1)
        self.form_layout.addRow("Petal Scale", self.petal_scale_dspnbx)

    def _mk_name_layout(self):
        self.name_lbl = QtWidgets.QLabel("Flower Generator")
        self.name_lbl.setAlignment(QtCore.Qt.AlignHCenter)
        self.name_lbl.setStyleSheet("font: bold 24px; color: #FFFFFF")
        self.main_layout.addWidget(self.name_lbl)

    def _mk_btn_layout(self):
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.btn_layout.addWidget(self.build_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.build_btn.clicked.connect(self.build)

    @QtCore.Slot()
    def build(self):
        self._set_flower_gen_properties()
        self.flower_generator.build()

    def _set_flower_gen_properties(self):
        self.flower_generator.stem_height = self.stem_height_dspnbx.value()
        self.flower_generator.stem_width = self.stem_width_dspnbx.value()  
        self.flower_generator.bud_size = self.bud_size_dspnbx.value()
        self.flower_generator.petal_count = self.petal_count_spnbx.value()
        self.flower_generator.petal_scale = self.petal_scale_dspnbx.value()


class Flower:

    def __init__(self):
        self.stem_height = 5.0
        self.stem_width = 0.2 
        self.bud_size = 0.6
        self.petal_count = 5
        self.petal_scale = 1.5

    def build(self):
        stem = self.create_stem()
        bud = self.create_bud()
        petals = self.create_petals(bud)

        cmds.group(stem, bud, *petals, name="flower")

    def create_stem(self):
        stem_name = cmds.polyCylinder(height=self.stem_height, 
                                      radius=self.stem_width, name="stem")[0]
        cmds.move(0, self.stem_height / 2, 0, stem_name, absolute=True)
        return stem_name

    def create_bud(self):
        bud_name = cmds.polySphere(radius=self.bud_size, name="bud")[0]
        cmds.move(0, self.stem_height, 0, bud_name, absolute=True)
        return bud_name

    def create_petals(self, bud):
        angle_step = 360 / self.petal_count
        petal_radius = self.bud_size * 1.5
        petals = []
        for i in range(self.petal_count):
            petal_name = cmds.polySphere(radius=self.bud_size * 
                                         self.petal_scale, 
                                         name=f"petal_{i + 1}")[0]
            cmds.scale(1, 0.5, 1, petal_name)  
            
            angle_deg = angle_step * i
            angle_rad = math.radians(angle_deg)  
            x_pos = petal_radius * math.sin(angle_rad) 
            z_pos = petal_radius * math.cos(angle_rad)  
            cmds.move(x_pos, self.stem_height, z_pos, 
                           petal_name, absolute=True)
            
            petals.append(petal_name)

        return petals


def main():
    win = FlowerWin()
    win.show()


if __name__ == "__main__":
    main()