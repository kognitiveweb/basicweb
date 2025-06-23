from reactpy import component, html

@component
def Downloads():
    return html.div(
        {"style": {"marginTop": "100px", "textAlign": "center","color": "white"}},
        html.h2("Downloads"),
        html.p("Download our apps and software from here."),
    )
