from unittest.mock import Mock

import pytest

from kopf.reactor.callbacks import HandlerResult
from kopf.reactor.states import HandlerOutcome


@pytest.fixture()
def handler():
    return Mock(id='some-id', spec_set=['id'])


def test_creation_for_ignored_handlers(handler):
    outcome = HandlerOutcome(final=True, handler=handler)
    assert outcome.final
    assert outcome.delay is None
    assert outcome.result is None
    assert outcome.exception is None
    assert outcome.handler is handler


def test_creation_for_results(handler):
    result = HandlerResult(object())
    outcome = HandlerOutcome(final=True, result=result, handler=handler)
    assert outcome.final
    assert outcome.delay is None
    assert outcome.result is result
    assert outcome.exception is None
    assert outcome.handler is handler


def test_creation_for_permanent_errors(handler):
    error = Exception()
    outcome = HandlerOutcome(final=True, exception=error, handler=handler)
    assert outcome.final
    assert outcome.delay is None
    assert outcome.result is None
    assert outcome.exception is error
    assert outcome.handler is handler


def test_creation_for_temporary_errors(handler):
    error = Exception()
    outcome = HandlerOutcome(final=False, exception=error, delay=123, handler=handler)
    assert not outcome.final
    assert outcome.delay == 123
    assert outcome.result is None
    assert outcome.exception is error
    assert outcome.handler is handler
