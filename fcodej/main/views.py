import os

from starlette.responses import FileResponse, HTMLResponse
from minify_html import minify

from ..common.flashed import get_flashed, set_flashed

async def show_index(request):
    use = request.session.get('_uid', None)
    html = minify(
        request.app.jinja.get_template(
            'main/index.html').render(
            request=request, flashed=await get_flashed(request),
            use=use),
        minify_js=True, remove_processing_instructions=True,
        do_not_minify_doctype=True, keep_spaces_between_attributes=True)
    return HTMLResponse(html)


async def show_favicon(request):
    if request.method == 'GET':
        base = os.path.dirname(os.path.dirname(__file__))
        return FileResponse(
            os.path.join(base, 'static', 'images', 'favicon.ico'))
