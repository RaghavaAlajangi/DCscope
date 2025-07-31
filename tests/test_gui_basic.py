import io
import pathlib
from unittest import mock
import sys

import dcscope
from dcscope.gui.main import DCscope
from dcscope import session
import pytest


data_path = pathlib.Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:
    session.clear_session()
    # A test function will be run at this point
    yield
    # Code that will run after your test, for example:
    session.clear_session()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python>=3.8")
def test_init_print_version(qtbot):
    mock_stdout = io.StringIO()
    mock_exit = mock.Mock()

    with mock.patch("sys.exit", mock_exit):
        with mock.patch('sys.stdout', mock_stdout):
            mw = DCscope("--version")
            mw.close()

    assert mock_exit.call_args.args[0] == 0
    assert mock_stdout.getvalue().strip() == dcscope.__version__


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python>=3.8")
def test_init_load_session(qtbot):
    mw = DCscope(data_path / "version_2_1_0_basic.so2")
    assert len(mw.pipeline.slots) == 1
    assert len(mw.pipeline.filters) == 1
    mw.close()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python>=3.8")
def test_init_load_dataslot(qtbot):
    mw = DCscope(data_path / "calibration_beads_47.rtdc")
    assert len(mw.pipeline.slots) == 1
    assert len(mw.pipeline.filters) == 1
    mw.close()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python>=3.8")
def test_on_action_about(qtbot):
    with mock.patch("PyQt6.QtWidgets.QMessageBox.about") as mock_about:
        mw = DCscope()
        mw.on_action_about()
        mw.close()

        assert mock_about.call_args.args[1] == \
            f"DCscope {dcscope.__version__}"
        assert "DCscope" in mock_about.call_args.args[2]


def test_simple(qtbot):
    """Open the main window and close it again"""
    main_window = DCscope()
    main_window.close()
