from unittest import mock

import pytest


@pytest.fixture
def analyticsreporting():
    return mock.Mock()


@pytest.fixture
def google():
    with mock.patch("analytics.reports.google") as google:
        yield google
