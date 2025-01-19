from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files import File

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return File(result, name='invoice.pdf')
    return None
