from reactpy import component, html

@component
def Home():
    return html.div(
        {"style": {"marginTop": "100px", "textAlign": "center"}},
        html.h1("Welcome to the Home Page"),
        html.p("This is the home page of the website."),
    )
