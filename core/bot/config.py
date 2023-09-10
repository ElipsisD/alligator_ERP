from bot import handlers

COMMAND_HANDLERS = {
    'start': handlers.start,
}

HANDLERS = {
    handlers.echo: handlers.echo_filter,
}

CONVERSATION_HANDLERS = (
    handlers.transfer_conv_handler,
    handlers.register_conv_handler,
)

CALLBACK_QUERY_HANDLERS = {
    'check': handlers.check,
}
