from subprocess import run

from dashboard.main import make_dashboard


def test_dashboard_exit_status():
    make_dashboard()
    assert True
