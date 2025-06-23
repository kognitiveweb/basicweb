from reactpy import component, html

@component
def Header(on_route_change,):
    return html.header(
        {
            "style": {
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",  # Space out items evenly
                "padding": "10px",
                "position": "fixed",
                "top": "0", #if is_visible else "-100px",  # Hide header when scrolling down
                "left": "0",
                "right": "0",
                "backgroundColor": "rgba(0, 0, 0, 0)",  # Fully transparent
                "color": "white",
                "zIndex": "10",
                "transition": "top 0.3s ease",  # Smooth transition for header hide/show
            }
        },
        # Company Name (top-left)
        html.div(
            {"style": {"fontSize": "20px", "fontWeight": "bold", "marginLeft": "10px"}},
            "Kiot",
        ),
        # Navigation Menu (centered)
        html.nav(
            {
                "style": {
                    "display": "flex",
                    "justifyContent": "center",
                    "gap": "20px",
                    "flexGrow": "1",
                    "marginLeft": "50px",
                    "marginRight": "50px",
                    "backgroundColor": "rgba(0, 0, 0, 0)"  # Transparent background for menu
                }
            },
            html.button(
                {"onClick": lambda event: on_route_change("home"), "style": menu_style()},
                "Home",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("interfaces"), "style": menu_style()},
                "Interfaces",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("hub"), "style": menu_style()},
                "Hub",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("lighting"), "style": menu_style()},
                "Lighting",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("about"), "style": menu_style()},
                "About",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("contact"), "style": menu_style()},
                "Contact",
            ),
            html.button(
                {"onClick": lambda event: on_route_change("downloads"), "style": menu_style()},
                "Downloads",
            ),
        ),
        # Phone Number (top-right)
        html.div(
            {
                "style": {
                    "fontSize": "18px",
                    "marginRight": "10px",
                }
            },
            "Call us: +91-9550007464",
        ),
    )

def menu_style():
    return {
        "margin": "5px",
        "backgroundColor": "transparent",  # Transparent background for menu items
        "border": "none",
        "padding": "10px",
        "cursor": "pointer",
        "fontSize": "16px",
        "color": "white",  # White text color for visibility
    }
