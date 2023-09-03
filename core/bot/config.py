from bot import handlers

COMMAND_HANDLERS = {
    "start": handlers.start,
}

HANDLERS = {
    handlers.echo: handlers.echo_filter,
}

CONVERSATION_HANDLERS = (
    handlers.register_conv_handler,
)

CALLBACK_QUERY_HANDLERS = {
    'check': handlers.check,
}
