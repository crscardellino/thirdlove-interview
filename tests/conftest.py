# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from tests.utils import get_test_client


@pytest.fixture
def client():
    client = get_test_client()

    yield client

