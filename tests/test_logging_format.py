import io
import logging

from cairnml_agent.commands.worker import get_task_fields


class _FailingResult:
    def json(self):
        raise RuntimeError("task lookup failed")


class _FailingSession:
    def send_request(self, **kwargs):
        return _FailingResult()


def test_failed_task_field_lookup_logs_its_message():
    stream = io.StringIO()
    logger = logging.getLogger("test-task-fields")
    logger.handlers = [logging.StreamHandler(stream)]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    assert get_task_fields(_FailingSession(), "task-1", ["container.image"], log=logger) == {}

    text = stream.getvalue()
    assert "Failed obtaining values for task fields" in text
    assert "['container.image']" in text
    assert "task lookup failed" in text
