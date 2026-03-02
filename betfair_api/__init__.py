"""
Betfair API service module.
Provides access to either real or mock services based on app config.
"""

def get_login_service(app):
    """Returns the login service (real or mock based on TEST_MODE)."""
    if app.config.get('TEST_MODE'):
        from . import mock
        return mock
    else:
        from . import login
        return login


def get_markets_service(app):
    """Returns the markets service (real or mock based on TEST_MODE)."""
    if app.config.get('TEST_MODE'):
        from . import mock
        return mock
    else:
        from . import markets
        return markets