from typing import Any, Union

from marvin.types import CodeInterpreterTool, FunctionTool, RetrievalTool

Retrieval = RetrievalTool()
CodeInterpreter = CodeInterpreterTool()

AssistantTool = Union[RetrievalTool, CodeInterpreterTool, FunctionTool]


class CancelRun(Exception):
    """
    A special exception that can be raised in a tool to end the run immediately.
    """

    def __init__(self, data: Any = None):
        self.data = data
