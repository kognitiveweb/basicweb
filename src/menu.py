from reactpy import component, html

@component
def Menu():
    return html.div(
        {"class": "menu"},
        html.a({"href": "/"},"Home"),
        html.div(
            {"class": "dropdown"},
            html.a({"href": "/interfaces"}, "Interfaces"),
            html.div(
                {"class": "dropdown-content"},
                html.a({"href": "/interfaces/m1"}, "m1"),
                html.a({"href": "/interfaces/m2"}, "m2"),
                html.a({"href": "/interfaces/m3"}, "m3"),
            ),
        ),
        html.div(
            {"class": "dropdown"},
            html.a({"href": "/about"}, "About Us"),
            html.div(
                {"class": "dropdown-content"},
                html.a({"href": "/about/m4"}, "m4"),
                html.a({"href": "/about/m5"}, "m5"),
            ),
        ),
        html.div(
            {"class": "dropdown"},
            html.a({"href": "/contact"}, "Contact"),
            html.div(
                {"class": "dropdown-content"},
                html.a({"href": "/contact/m6"}, "m6"),
                html.a({"href": "/contact/m7"}, "m7"),
                html.a({"href": "/contact/m8"}, "m8"),
            ),
        ),
    )
