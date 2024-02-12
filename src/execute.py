import inspect
import re as regex

from lightbulb import BotApp
from tcrutils import console as kon

from execute_p import aliases as exep_lookup
from imports import (
  Callable,
  S,
  _execute_embed,
  _execute_role_mentions,
  _execute_user_mentions,
  curly_filter,
  curly_unfilter,
  embed,
  hikari,
  run_sac,
)

UNKNOWN_EXECUTE_PLACEHOLDER = '`Unknown placeholder: %s`'

if True:  # \/ # Execute

  def has_arg(func):
    signature = inspect.signature(func)
    parameters = signature.parameters
    return any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in parameters.values())

  def valid_kwargs(func, kwargs: dict):
    signature = inspect.signature(func)
    parameters = signature.parameters
    return {k: v for k, v in kwargs.items() if k in parameters}

  def in_dms(event: hikari.MessageCreateEvent):
    return not hasattr(event, 'guild_id')

  async def evaluate_placeholder(placeholder: str, event: hikari.MessageCreateEvent) -> str:
    placeholder = curly_unfilter(placeholder)
    args = placeholder.split(S.EXECUTE_SPLITTER)
    name = args.pop(0).lower()

    try:
      func = exep_lookup[name]
    except KeyError:
      result = UNKNOWN_EXECUTE_PLACEHOLDER % curly_filter(repr(name))
    else:
      kwargs = {
        'event': event,
        'in_dms': in_dms(event),
        'execute': execute,
      }

      args = args if has_arg(func) else ()

      result = await run_sac(func, *args, **valid_kwargs(func, kwargs))

    return str(result)

  async def _exe(text: str, event: hikari.MessageCreateEvent):
    def get_innermost_placeholder(text: str) -> tuple[int, int]:
      end = text.find(S.EXECUTE_BRACKETS[1])
      start = text.rfind(S.EXECUTE_BRACKETS[0], 0, end)
      return start, end + len(S.EXECUTE_BRACKETS[1])

    while True:
      start, end = get_innermost_placeholder(text)
      if start == -1 or end == -1:
        break

      placeholder = text[start:end]
      placeholder_value = await evaluate_placeholder(
        placeholder[len(S.EXECUTE_BRACKETS[0]) : -len(S.EXECUTE_BRACKETS[1])],
        event,
      )  # Replace with get_placeholder_value(placeholder[2:-2])
      placeholder_value = curly_filter(placeholder_value)
      text = text[:start] + placeholder_value + text[end:]

    return curly_unfilter(text)

  class ExecuteParameterError(TypeError): ...

  class ExecuteBracketsError(ValueError): ...

  async def execute(
    text: str,
    event: hikari.Event,
    *,
    responder: Callable | None = None,
  ) -> hikari.Message | dict:
    """Return a `str` which contains executed text. If `responder` is specified, respond with that message and return the Message object instead.

    Raises:
      - hikari.errors.BadRequestError: One of message fields (eg. content, embed) violated discord's limit. (eg. cannot send an empty limit, embed title too long)
      - Any other error: Internal (execute's placeholder) exception

    hikari.errors.BadRequestError may also be caused by a placeholder
    """
    _execute_user_mentions.clear()
    _execute_role_mentions.clear()
    _execute_embed.clear()

    # fmt: off
    executed = {
      "content":       await _exe(text=text, event=event),
      "embed":         embed(**_execute_embed) if _execute_embed else hikari.UNDEFINED,
      "user_mentions": list(_execute_user_mentions),
      "role_mentions": list(_execute_role_mentions),
    }
    # fmt: on

    # hikari.GuildMessageCreateEvent.message.respond
    if responder:
      return await responder(**executed)
    return executed
