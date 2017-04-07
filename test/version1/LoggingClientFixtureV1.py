# -*- coding: utf-8 -*-
"""
    tests.persistence.LoggingClientFixtureV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import pytest
import datetime

from pip_services_commons.log import LogLevel
from pip_services_commons.errors import ErrorDescriptionFactory
from pip_services_commons.data import FilterParams, PagingParams
from pip_clients_logging.version1 import LogMessageV1

class LoggingClientFixtureV1:
    _client = None

    def __init__(self, client):
        self._client = client


    def test_crud_operations(self):
        message = self._client.write_message(
            None, 
            LogMessageV1(LogLevel.Info, None, "123", None, "AAA")
        )
        assert None != message

        message1 = LogMessageV1(LogLevel.Debug, None, "123", None, "BBB")
        message2 = LogMessageV1(LogLevel.Error, None, "123", ErrorDescriptionFactory.create(Exception('Test error')), "AAB")
        message2.time = datetime.datetime(1975, 1, 1, 0, 0, 0, 0)
        self._client.write_messages(
            None,
            [message1, message2]
        )

        page = self._client.read_messages(
            None, 
            FilterParams.from_tuples("search", "AA"), 
            None
        )
        assert 2 == len(page.data)

        page = self._client.read_errors(
            None, 
            None, 
            None
        )
        assert 1 == len(page.data)

