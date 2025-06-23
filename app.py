from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy import component, html, use_state
from reactpy.backend.fastapi import configure

# Import components
from src.header import Header
from src.footer import Footer
from src.home import Home
from src.interfaces import Interfaces
from src.about import About
from src.contact import Contact
from src.hub import Hub
from src.lighting import Lighting
from src.downloads import Downloads
from src.invoice_app import InvoiceApp  # This includes the PDF logic


@component
def App():
    route, set_route = use_state("home")

    def render_page():
        if route == "home":
            return Home()
        elif route == "interfaces":
            return Interfaces()
        elif route == "about":
            return About()
        elif route == "contact":
            return Contact()
        elif route == "lighting":
            return Lighting()
        elif route == "downloads":
            return Downloads()
        elif route == "hub":
            return InvoiceApp()
        return html.div("404 Page Not Found")

    return html.div(
        {
            "style": {
                "height": "100vh",
                "backgroundImage": "url('https://keus.able.do/cdn-cgi/image/width=2000,quality=65/assets/incognito/banner-p.jpg')",
                "backgroundSize": "cover",
                "backgroundPosition": "center",
                "backgroundAttachment": "fixed",
                "backgroundRepeat": "no-repeat",
                "display": "flex",
                "flexDirection": "column",
            }
        },
        Header(set_route),
        render_page(),
        Footer(),
    )


# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Serve static files for product images and invoices
app.mount("/products", StaticFiles(directory="products"), name="products")

# ✅ Connect ReactPy to FastAPI
configure(app, App)

# ✅ Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
