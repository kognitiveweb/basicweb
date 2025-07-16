from reactpy import component, html, run, use_state, use_effect
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import asyncio

fastapi_app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

images = [
    {
        "left_color": "red",
        "right_color": "black",
        "left_content": "Smart Living Begins Here",
        "right_content": {"type": "img", "src": "static/images/1.png"},
    },
    {
        "left_color": "black",
        "right_color": "red",
        "left_content": {"type": "img", "src": "static/images/2.png"},
        "right_content": "Control at Your Fingertips",
    },
    {
        "left_color": "red",
        "right_color": "black",
        "left_content": "Your Home, Smarter",
        "right_content": {"type": "img", "src": "static/images/3.png"},
    },
]

@component
def FadeText(text):
    style = {
        "opacity": 0,
        "animation": "fadeIn 2s forwards",
        "color": "white",
        "padding": "20px",
        "borderRadius": "10px",
        "fontSize": "2em",
        "textAlign": "center",
        "maxWidth": "80%",
    }
    return html.div(
        {"style": style},
        text,
        html.style("""
            @keyframes fadeIn {
                to {opacity: 1;}
            }
        """),
    )

@component
def TypingText(text):
    displayed, set_displayed = use_state("")

    async def type_text():
        for i in range(len(text) + 1):
            set_displayed(text[:i])
            await asyncio.sleep(0.05)

    use_effect(lambda: asyncio.create_task(type_text()), [text])

    return html.div({
        "style": {
            "color": "white",
            "padding": "20px",
            "borderRadius": "10px",
            "fontSize": "2em",
            "textAlign": "center",
            "maxWidth": "80%",
            "whiteSpace": "pre-wrap",
            "fontFamily": "monospace",
        }
    }, displayed)

@component
def SlideInText(text, direction="right"):
    style = {
        "transform": "translateX(100%)" if direction == "right" else "translateX(-100%)",
        "animation": "slideIn 1.5s forwards",
        "color": "white",
        "padding": "20px",
        "borderRadius": "10px",
        "fontSize": "2em",
        "textAlign": "center",
        "maxWidth": "80%",
    }
    return html.div({"style": style}, text, html.style("""
        @keyframes slideIn {
            to {transform: translateX(0);}
        }
    """))

effects = [FadeText, TypingText, SlideInText]

@component
def Slide(index: int):
    slide = images[index % len(images)]

    def render_text(content, pos):
        if isinstance(content, dict) and content.get("type") == "img":
            return html.img({"src": "/" + content["src"], "style": {"width": "100%", "height": "100%", "objectFit": "cover"}})
        elif isinstance(content, str):
            effect_index = (index + (0 if pos == "left" else 1)) % len(effects)
            return effects[effect_index](content)
        return html.div(str(content))

    return html.div({"style": {"display": "flex", "height": "100vh", "width": "100vw"}},
        html.div({
            "style": {
                "flex": 1, "backgroundColor": slide["left_color"],
                "display": "flex", "alignItems": "center", "justifyContent": "center"
            }},
            render_text(slide["left_content"], "left")
        ),
        html.div({
            "style": {
                "flex": 1, "backgroundColor": slide["right_color"],
                "display": "flex", "alignItems": "center", "justifyContent": "center"
            }},
            render_text(slide["right_content"], "right")
        )
    )

def arrow_style():
    return {
        "backgroundColor": "transparent",
        "color": "white",
        "fontSize": "2em",
        "border": "none",
        "cursor": "pointer",
        "padding": "10px",
    }

@component
def Arrows(on_next, on_prev):
    return html.div({
        "style": {
            "position": "absolute",
            "bottom": "20px",
            "width": "100%",
            "display": "flex",
            "justifyContent": "center",
            "gap": "30px",
            "zIndex": 10,
        }},
        html.button({"onClick": lambda e: on_prev(), "style": arrow_style()}, "⟨"),
        html.button({"onClick": lambda e: on_next(), "style": arrow_style()}, "⟩")
    )

@component
def VideoSection():
    return html.div({
        "style": {
            "height": "100vh", "width": "100vw",
            "display": "flex", "alignItems": "center", "justifyContent": "center",
            "backgroundColor": "#000"
        }},
        html.video({
            "controls": True, "autoPlay": True,
            "style": {"width": "100%", "border": "4px solid white"},
            "src": "/static/sample.mp4"
        })
    )

@component
def BlackInfoPage():
    return html.div({
        "style": {
            "height": "100vh", "width": "100vw", "backgroundColor": "black",
            "color": "white", "display": "flex", "flexDirection": "column",
            "alignItems": "center", "justifyContent": "center",
            "padding": "40px", "boxSizing": "border-box",
        }},
        html.h1({"style": {"color": "red", "textAlign": "center", "marginBottom": "40px"}}, "Welcome to the Future of Living"),
        html.div({"style": {"display": "flex", "width": "100%", "maxWidth": "1200px", "gap": "40px", "textAlign": "justify"}},
            html.div({"style": {"flex": 1}}, html.p("Experience cutting-edge automation that transforms your living space into a hub of convenience, security, and efficiency.")),
            html.div({"style": {"flex": 1}}, html.p("Our smart systems learn your preferences and adapt to your lifestyle. Enjoy seamless control via your phone, voice, or sensors."))
        )
    )

@component
def MainPage():
    current_slide, set_slide = use_state(0)

    def next_slide():
        set_slide((current_slide + 1) % 3)

    def prev_slide():
        set_slide((current_slide - 1) % 3)

    # Properly cancel auto-slide loop on unmount
    def start_loop():
        task = asyncio.create_task(slider_loop(set_slide))
        def cleanup():
            task.cancel()
        return cleanup

    use_effect(start_loop, [])

    return html.div(
        {
            "style": {
                "overflowY": "scroll",
                "scrollbarWidth": "none",
                "height": "100vh",
            }
        },
        # Hide scrollbars using global style
        html.style("""
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
            }
            ::-webkit-scrollbar {
                display: none;
            }
        """),

        # Main auto-slide section with arrows
        html.div(
            {
                "style": {
                    "position": "relative",
                    "height": "100vh",
                    "width": "100vw",
                }
            },
            Slide(current_slide),
            Arrows(on_next=next_slide, on_prev=prev_slide),
        ),

        # Other sections (without arrows)
        BlackInfoPage(),
        Slide(0),
        Slide(1),
        Slide(2),
        VideoSection(),
    )

async def slider_loop(set_slide):
    try:
        while True:
            await asyncio.sleep(3)
            set_slide(lambda s: (s + 1) % 3)
    except asyncio.CancelledError:
        pass

configure(fastapi_app, MainPage)

if __name__ == "__main__":
    import asyncio
    import uvicorn

    uvicorn.run("app:fastapi_app", host="0.0.0.0", port=8000, reload=False)


# if __name__ == "__main__":
#     run(fastapi_app, host="0.0.0.0", port=8000)
