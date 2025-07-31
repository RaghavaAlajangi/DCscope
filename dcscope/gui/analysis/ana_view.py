import importlib.resources

from PyQt6 import uic, QtCore, QtWidgets


class AnalysisView(QtWidgets.QWidget):
    filter_changed = QtCore.pyqtSignal(dict)
    plot_changed = QtCore.pyqtSignal(dict)
    slot_changed = QtCore.pyqtSignal(dict)
    pipeline_changed = QtCore.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(AnalysisView, self).__init__(*args, **kwargs)
        ref = importlib.resources.files(
            "dcscope.gui.analysis") / "ana_view.ui"
        with importlib.resources.as_file(ref) as path_ui:
            uic.loadUi(path_ui, self)

        self._quickview_slot_index = 0
        self._quickview_filt_index = 0

        self.page_widgets = [
            self.widget_basins,
            self.widget_meta,
            self.widget_filter,
            self.widget_log,
            self.widget_meta,
            self.widget_plot,
            self.widget_slot,
            self.widget_tables
        ]

        self.setWindowTitle("Analysis View")
        self.setMinimumSize(self.sizeHint())
        # Signals
        self.widget_filter.filter_changed.connect(self.filter_changed)
        self.widget_filter.pipeline_changed.connect(self.pipeline_changed)
        self.widget_plot.plot_changed.connect(self.plot_changed)
        self.widget_plot.pipeline_changed.connect(self.pipeline_changed)
        self.widget_slot.slot_changed.connect(self.slot_changed)
        self.widget_slot.pipeline_changed.connect(self.pipeline_changed)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.update_content)

    @QtCore.pyqtSlot(int, int)
    def on_quickview(self, slot_index, filt_index):
        """Signal from the block matrix"""
        self._quickview_filt_index = filt_index
        self._quickview_slot_index = slot_index
        self.update_content()

    def set_pipeline(self, pipeline):
        self._quickview_filt_index = min(self._quickview_filt_index,
                                         len(pipeline.filters) - 1)
        self._quickview_slot_index = min(self._quickview_slot_index,
                                         len(pipeline.slots) - 1)
        for widget in self.page_widgets:
            widget.set_pipeline(pipeline)
        self.update_content()

    @QtCore.pyqtSlot()
    def update_content(self):
        cur_page = self.tabWidget.currentWidget()
        for widget in self.page_widgets:
            if widget.parent() is cur_page:
                widget.update_content(
                    slot_index=self._quickview_slot_index,
                    filt_index=self._quickview_filt_index)
                break
