from reactpy import component, html

@component
def Contact():
    return html.div(
        {"style": {"marginTop": "100px", "textAlign": "center","color": "white"}},
        html.h1("Contact Us"),
        html.p("This is the contact page."),
    )
