from reactpy import component, html

@component
def ChatButton():
    return html.div(
        {"class": "chat-button", "on_click": lambda: toggle_chat_window()},
        "Chat",
    )

@component
def ChatWindow(show_chat_window):
    return html.div(
        {"class": f"chat-window {'show' if show_chat_window else ''}"},
        html.div({"class": "chat-header"}, "Chat with us!"),
        html.textarea({"class": "chat-input", "placeholder": "Ask a question..."}),
        html.button({"class": "send-btn"}, "Send"),
    )
