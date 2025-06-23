import os
import uuid
import pandas as pd
from reactpy import component, html, use_state
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import (
    Table, TableStyle, SimpleDocTemplate, Spacer,
    Paragraph, Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Load product data from Excel
df = pd.read_excel("products/doch_products.xlsx")
products = df.to_dict("records")

invoice_dir = "products/invoices"
os.makedirs(invoice_dir, exist_ok=True)
letterhead_path = "products/letter_head.pdf"  # Make sure this file exists


@component
def InvoiceApp():
    selected_quantities, set_selected_quantities = use_state({})
    view, set_view = use_state("grid")
    invoice_id, set_invoice_id = use_state(None)

    def handle_quantity_change(product_id, delta):
        def change(event):
            new_quantities = selected_quantities.copy()
            new_quantities[product_id] = max(0, new_quantities.get(product_id, 0) + delta)
            set_selected_quantities(new_quantities)
        return change

    def handle_submit(event):
        invoice_uuid = str(uuid.uuid4())
        generate_invoice_pdf(invoice_uuid, selected_quantities)
        set_invoice_id(invoice_uuid)
        set_view("summary")

    def ProductGrid():
        return html.div(
            {"style": {"padding": "20px", "width": "100vw"}},
            html.h2("Product Catalog"),
            html.div(
                {"style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(4, 1fr)",
                    "gap": "20px",
                    "maxHeight": "80vh",
                    "overflowY": "scroll",
                }},
                [
                    html.div(
                        {"style": {
                            "border": "1px solid #ccc",
                            "borderRadius": "10px",
                            "padding": "10px",
                            "textAlign": "center",
                            "backgroundColor": "#ffffff"
                        }},
                        html.img({
                            "src": f"/products/product_images/{product['Product ID']}.png",
                            "alt": product["Product name"],
                            "style": {"width": "100%", "height": "150px", "objectFit": "contain"}
                        }),
                        html.h4(product["Product name"]),
                        html.p(f"{product['MRP(EX GST)']:.2f}"),
                        html.p(product["Product Description"]),
                        html.div(
                            {"style": {"display": "flex", "justifyContent": "center", "gap": "10px"}},
                            html.button({"onClick": handle_quantity_change(product["Product ID"], -1)}, "-"),
                            html.span(str(selected_quantities.get(product["Product ID"], 0))),
                            html.button({"onClick": handle_quantity_change(product["Product ID"], 1)}, "+")
                        )
                    )
                    for product in products
                ]
            ),
            html.div(
                {"style": {"textAlign": "center", "marginTop": "20px"}},
                html.button(
                    {"style": {
                        "padding": "10px 20px", "fontSize": "16px",
                        "cursor": "pointer", "backgroundColor": "green", "color": "white",
                        "border": "none", "borderRadius": "8px"
                    }, "onClick": handle_submit},
                    "Submit"
                )
            )
        )

    def InvoiceSummary():
        selected_items = []
        total = 0
        for product in products:
            pid = product["Product ID"]
            qty = selected_quantities.get(pid, 0)
            if qty > 0:
                name = product["Product name"]
                price = product["MRP(EX GST)"]
                subtotal = qty * price
                total += subtotal
                selected_items.append((name, pid, qty, price, subtotal))

        gst = total * 0.18
        grand_total = total + gst

        return html.div(
            {"style": {"padding": "20px", "maxWidth": "900px", "margin": "auto","color":"white"}},
            html.h2("Invoice Summary"),
            html.table(
                {"border": "1", "cellPadding": "10", "style": {"width": "100%", "borderCollapse": "collapse"}},
                html.thead(
                    html.tr([
                        html.th("Product Name"),
                        html.th("Product ID"),
                        html.th("Qty"),
                        html.th("Unit Price (INR)"),
                        html.th("Subtotal (INR)")
                    ])
                ),
                html.tbody([
                    html.tr([
                        html.td(name),
                        html.td(pid),
                        html.td(str(qty)),
                        html.td(f"{price:.2f}"),
                        html.td(f"{subtotal:.2f}")
                    ])
                    for name, pid, qty, price, subtotal in selected_items
                ])
            ),
            html.p(f"Total (before GST): {total:.2f}"),
            html.p(f"GST (18%): {gst:.2f}"),
            html.h3(f"Grand Total: {grand_total:.2f}"),
            html.p("Instructions: Please verify all quantities and prices. Contact support for discrepancies."),
            html.div(
                {"style": {"textAlign": "center", "marginTop": "20px"}},
                html.a(
                    {
                        "href": f"/products/invoices/invoice_{invoice_id}.pdf",
                        "download": "invoice.pdf",
                        "target": "_blank",
                        "style": {
                            "marginRight": "10px", "padding": "10px 20px", "fontSize": "16px",
                            "cursor": "pointer", "backgroundColor": "#03039E", "color": "white",
                            "textDecoration": "none", "borderRadius": "8px"
                        }
                    },
                    "Download Invoice as PDF"
                ),
                html.button(
                    {"onClick": lambda e: set_view("grid"), "style": {
                        "padding": "10px 20px", "fontSize": "16px",
                        "cursor": "pointer", "backgroundColor": "#333", "color": "#fff",
                        "border": "none", "borderRadius": "8px"
                    }},
                    "Back to Products"
                )
            )
        )

    return ProductGrid() if view == "grid" else InvoiceSummary()


def generate_invoice_pdf(invoice_id, selected_quantities):
    selected_items = []
    total = 0
    for product in products:
        pid = str(product["Product ID"])
        qty = selected_quantities.get(pid, 0)
        if qty > 0:
            name = product["Product name"]
            price = product["MRP(EX GST)"]
            subtotal = qty * price
            total += subtotal
            img_path = f"products/product_images/{pid}.png"
            selected_items.append((name, img_path, qty, price, subtotal))

    gst = total * 0.18
    grand_total = total + gst

    overlay_path = os.path.join(invoice_dir, f"overlay_{invoice_id}.pdf")
    final_path = os.path.join(invoice_dir, f"invoice_{invoice_id}.pdf")

    doc = SimpleDocTemplate(overlay_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Header row
    header_row = ["Product Name", "Image", "Qty", "Unit Price ()", "Subtotal ()"]
    table_data = [header_row]

    for name, img_path, qty, price, subtotal in selected_items:
        try:
            img = Image(img_path, width=25 * mm, height=25 * mm)
        except Exception:
            img = Paragraph("N/A", styles["Normal"])
        table_data.append([name, img, str(qty), f"{price:.2f}", f"{subtotal:.2f}"])

    rows_per_page = 20
    for start in range(1, len(table_data), rows_per_page):
        chunk = [header_row] + table_data[start:start + rows_per_page]
        table = Table(chunk, colWidths=[50*mm, 30*mm, 20*mm, 30*mm, 30*mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (2, 1), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(Spacer(1, 30))
        elements.append(table)
        if start + rows_per_page < len(table_data):
            elements.append(PageBreak())

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total (before GST): {total:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"GST (18%): {gst:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Grand Total: {grand_total:.2f}</b>", styles["Heading3"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "Instructions: Please verify all quantities and prices. Contact support for discrepancies.",
        styles["Normal"]
    ))

    doc.build(elements)

    # Merge overlay and letterhead
    reader_overlay = PdfReader(overlay_path)
    reader_letterhead = PdfReader(letterhead_path)
    writer = PdfWriter()

    for overlay_page in reader_overlay.pages:
        background_page = reader_letterhead.pages[0]
        new_page = background_page.__class__.create_blank_page(
            None,
            width=background_page.mediabox.width,
            height=background_page.mediabox.height
        )
        new_page.merge_page(background_page)
        new_page.merge_page(overlay_page)
        writer.add_page(new_page)

    with open(final_path, "wb") as f:
        writer.write(f)
