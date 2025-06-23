from reactpy import component, html

@component
def Interfaces():
    return html.div(
        {"style": {"position": "relative", "height": "100vh", "margin": "0", "padding": "0"}},
        # Video element that takes the full screen
        html.video(
            {
                "style": {
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "objectFit": "cover"
                },
                "controls": True,
            },
            html.source({"src": "http://localhost:8001/videos/home/video1.mp4", "type": "video/mp4"})
        ),
        # Overlay content (h1 and paragraph)
        html.div(
            {"style": {"position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "color": "white", "textAlign": "center"}},
            html.h1("Welcome to the Interfaces Page"),
            html.p("This is the Interfaces page of the website.")
        ),
    )
