from reactpy import component, html

@component
def Lighting():
    return html.div(
        {"style": {"padding": "100px", "textAlign": "center"}},
        html.h2("Our Lighting details"),
        html.p("Details about our products will be here."),
    )
