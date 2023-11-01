from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template


def render_to_pdf(template_src, context_dict={}, filename=None, download=False):  # noqa
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

    pdf_name = filename if filename else 'invoice.pdf'

    if pdf.err:
        return HttpResponse('Invalid PDF', status_code=400, content_type='text/plain')  # noqa
    response = HttpResponse(
        result.getvalue(),
        content_type='application/pdf' if not download else f'document/pdf;',  # noqa
    )

    response['Content-Disposition'] = f'filename={pdf_name}'

    return response
