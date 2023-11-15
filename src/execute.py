from imports import *

BRACKETS = ('{{', '}}')

if True:  # \/ # Execute

  @tcr.convert.stringify
  async def evaluate_placeholder(*args, event: hikari.MessageCreateEvent):
    # Replace this with your actual evaluation function
    print(args)
    if args[0] != 'uwu':
      return '{uwu|owo}'
    return len(args)

  async def _exe(text, event: hikari.MessageCreateEvent):
    _exe = partial(globals()['_exe'], event=event)
    start_index = text.find('{')
    if start_index == -1:
      return text

    end_index = -1
    level = 0
    for i in range(start_index, len(text)):
      if text[i] == '{':
        level += 1
      elif text[i] == '}':
        level -= 1
        if level == 0:
          end_index = i
          break

    if end_index == -1:
      return text

    inner_text = text[start_index + 1 : end_index]
    placeholder = text[start_index : end_index + 1]

    inner_value = _exe(inner_text)
    evaluated_value = await evaluate_placeholder(*inner_value.split('|'), event=event)

    return _exe(text.replace(placeholder, evaluated_value, 1))

  class ExecuteParameterError(TypeError): ...

  class ExecuteBracketsError(ValueError): ...

  async def execute(
    text: str, event: hikari.Event, responder: Callable | None = None
  ) -> hikari.Message | str:
    """Return a `str` which contains executed text. If `responder` is specify, respond with that message and return the Message object instead.

    Raises:
      - ExecuteParameterError: if any of passed in parameters are wrong
      - ExecuteBracketsError: if there are mismatched [[brackets]]
      - Any other error: Internal (execute's placeholder) exception
    """
    executed = await _exe(text=text, event=event)
    if responder:
      return await responder(**executed)
    return executed
