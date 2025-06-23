from reactpy import component, html

@component
def Footer():
    return html.footer(
        {
            "style": {
                "position": "fixed",
                "bottom": "0",
                "left": "0",
                "right": "0",
                "backgroundColor": "#282c34",
                "color": "white",
                "textAlign": "center",
                "padding": "10px",
            }
        },
        "© 2024 Company Name. All rights reserved.",
    )
