must_commands = [
    CommandHandler("start", start),
    CommandHandler("stop", stop_bot),
    CommandHandler("admin", admin_menu),
]

states = {
    State.ASK_LOCATION: [MessageHandler(Filters.text, ask_location)],
    State.ASK_TYPE: [MessageHandler(Filters.text, ask_type)],
    State.ASK_AGE: [MessageHandler(Filters.text, ask_age)],
    State.ASK_PROPS: [MessageHandler(Filters.text, ask_props)],
    State.RESULT: [MessageHandler(Filters.text, result)],
    State.ANSWER: [MessageHandler(Filters.text, final_answer)],
    State.BACK_ANSWER: [MessageHandler(Filters.text, back_answer)],
    State.ADMIN: [MessageHandler(Filters.text, admin_handler)],
    State.PUSH_WHO: [MessageHandler(Filters.text, push_who)],
    State.PUSH_WHAT: [MessageHandler(Filters.text, push_text)],
    State.PUSH_SUBMIT: [MessageHandler(Filters.text, push_handler)],
}

for key, value in states.items():
    states[key] = must_commands + value

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start), CommandHandler("admin", admin)],
    states=states,
    fallbacks=[CommandHandler("stop", stop_bot)],
)
