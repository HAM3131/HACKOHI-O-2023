import interior
import pathfinding
# HTML Generating Functions #######################

def gen_base_html(space):
    html = ""
    html += """
<!DOCTYPE html>
<html>
<head>
    <title>Space Navigator</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body style="background-color: black; color: white;">
"""
    html += """
<!-- Dropdown for selecting start and end nodes -->
    <div> Where are you now? </div>
    <select id="start_node">
"""
    for node in space.get_nodes().keys():
        if space.get_node(node).get_type() == interior.NodeType.ROOM or space.get_node(node).get_type() == interior.NodeType.EXIT:
            html += f"""
        <option value="{node}">{node}</option>
"""
    html +="""
    </select>
    <div> Where would you like to go? </div>
    <select id="end_node">
"""
    for node in space.get_nodes().keys():
        if space.get_node(node).get_type() == interior.NodeType.ROOM or space.get_node(node).get_type() == interior.NodeType.EXIT:
            html += f"""
        <option value="{node}">{node}</option>
"""
    html += """
    </select>

    <!-- Checkbox for blacklisting NodeTypes -->
    <div>Blacklist node types</div>
"""
    for name in interior.NodeType.types:
        html += f"""
    <input type="checkbox" id="blacklist_{name}" value="{name}"> {name.capitalize()}
"""
    html += """
    <!-- Button to generate path -->
    <button onclick="generatePath()">Generate Path</button>
"""
    html += space.plot_space()
    html += f"""

    <script>
        function generatePath() {{
            const start_node = $('#start_node').val();
            const end_node = $('#end_node').val();
            const blacklist = [];"""
    for name in interior.NodeType.types:
        html += f"""
            if ($('#blacklist_{name}').is(":checked")) {{
                blacklist.push("{name}");
            }}
            """
            
    html += f"""
            $.ajax({{
                url: '/get_path',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({{ start_node, end_node, blacklist }}),
                success: function(response) {{
                    window.open(response.redirect, '_blank');
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    return html


def gen_result_html(space, path):
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Path Result</title>
    <script>
        function speak(text) {{
            const synth = window.speechSynthesis;
            const utterance = new SpeechSynthesisUtterance(text);
            synth.speak(utterance);
        }}
    </script>
</head>
<body style="background-color: black; color: white;">
    <h1>Shortest Path</h1>
    <p>{" -> ".join(path)}</p>
    <p>{space.path_to_string(path)}</p>
    {space.plot_space_highlight(path)}
</body>
</html>
"""
    return html

def gen_speak_button(text):
    # Escape single and double quotes in the text
    escaped_text = text.replace("'", "\\'").replace('"', '\\"')
    
    # Generate HTML with embedded JavaScript
    html = f"""
<button onclick="speak('{escaped_text}')">🔊 Speak</button>
<script>
    function speak(text) {{
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);
        synth.speak(utterance);
    }}
</script>
"""
    return html