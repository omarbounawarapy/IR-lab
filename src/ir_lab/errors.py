"""The failure-category taxonomy every IR Lab error should belong to.

A researcher hitting a failure should be able to tell, from the message
alone and without reading a stack trace, which of these four things went
wrong. Raise the most specific of these that applies -- never a bare
Exception/KeyError/AttributeError for anything an experiment can trigger.
"""


class IRLabError(Exception):
    """Base class for every experiment-facing error IR Lab raises."""


class ConfigError(IRLabError):
    """An experiment config is malformed or references a component,
    dataset, or parameter that does not exist."""


class DataError(IRLabError):
    """A config is well-formed and references something real, but the
    underlying data (a file, a field) is missing or doesn't match what
    was declared."""


class UnsupportedFeatureError(IRLabError):
    """The request is well-formed and the referenced components exist,
    but the specific combination or construct isn't implemented yet."""


class ExecutionError(IRLabError):
    """Something failed during a run for reasons unrelated to the
    researcher's config or data -- a genuine framework bug."""
