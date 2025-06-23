from reactpy import component, html

@component
def About():
    return html.div(
        {"style": {"marginTop": "100px", "textAlign": "center","color": "white"}},
        html.h1("About Us"),
        html.p("Learn more about our company."),
    )
