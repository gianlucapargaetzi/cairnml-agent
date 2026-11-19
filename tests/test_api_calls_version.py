"""The API version a call goes out at, and what the agent's feature checks ask about the definition a call uses.

Every request goes out at the negotiated level (the SDK's request_version). A feature is available when the definition
the call is sent with declares what the feature sends, or when the action is served at all; the tests fix those
answers at a few server levels.
"""

import pytest
from cairnml.backend_api.services import API_LEVEL

from cairnml_agent.session import Session


@pytest.fixture
def server_level(monkeypatch):
    """The server reports the level the test names; the SDK's negotiated level follows it."""

    def set_level(level):
        monkeypatch.setattr(Session, "max_api_version", level)

    return set_level


def test_a_request_goes_out_at_the_servers_level_when_it_is_older_than_the_client(server_level):
    server_level("2.9")
    assert Session.request_version("tasks", "get_all") == "2.9"


def test_a_request_goes_out_at_the_clients_level_when_the_server_is_newer(server_level):
    server_level("9.9")
    assert Session.request_version("tasks", "get_all") == API_LEVEL


def test_an_action_is_served_from_the_level_of_its_first_definition(server_level):
    server_level("2.8")
    assert not Session.serves("debug", "ping")
    server_level("2.9")
    assert Session.serves("debug", "ping")


def test_the_container_of_a_task_is_declared_from_the_definition_that_added_it(server_level):
    server_level("2.12")
    assert not Session.declares("tasks", "edit", "container")
    server_level("2.13")
    assert Session.declares("tasks", "edit", "container")


def test_search_hidden_is_declared_from_the_definition_that_added_it(server_level):
    server_level("2.13")
    assert not Session.declares("tasks", "get_all", "search_hidden")
    server_level("2.14")
    assert Session.declares("tasks", "get_all", "search_hidden")


def test_an_action_that_is_not_served_declares_nothing(server_level):
    server_level("2.8")
    assert not Session.declares("debug", "ping", "anything")


def test_the_definition_is_the_newest_one_at_or_below_the_level(server_level):
    server_level("2.14")
    request_cls, response_cls = Session.definition("tasks", "get_all")
    assert request_cls._version == "2.14"
    assert response_cls is not None
