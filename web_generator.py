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
<body>
"""
    html += """
<!-- Dropdown for selecting start and end nodes -->
    <div> Where are you now? </div>
    <select id="start_node">
"""
    for node in space.get_nodes().keys():
        if space.get_node(node).get_type() == interior.NodeType.ROOM:
            html += f"""
        <option value="{node}">{node}</option>
"""
    html +="""
    </select>
    <div> Where would you like to go? </div>
    <select id="end_node">
"""
    for node in space.get_nodes().keys():
        if space.get_node(node).get_type() == interior.NodeType.ROOM:
            html += f"""
        <option value="{node}">{node}</option>
"""
    html += """
    </select>

    <!-- Checkbox for blacklisting NodeTypes -->
    <div>Blacklist room types</div>
"""
    for name in interior.NodeType.types:
        html += f"""
    <input type="checkbox" id="blacklist_{name}" value="{name}"> {name.capitalize()}
"""
    html += """
    <!-- Button to generate path -->
    <button onclick="generatePath()">Generate Path</button>

    <!-- Div to display the path -->
    <div id="path"></div>

"""
    html += space.plot_space()
    html += """

    <script>
        function generatePath() {
            const start_node = $('#start_node').val();
            const end_node = $('#end_node').val();
            const blacklist = [];

            if ($('#blacklist_room').is(":checked")) {
                blacklist.push("room");
            }
            if ($('#blacklist_stairs').is(":checked")) {
                blacklist.push("stairs");
            }

            $.ajax({
                url: '/get_path',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ start_node, end_node, blacklist }),
                success: function(response) {
                    $('#path').html("Shortest Path: " + response.path.join(" -> "));
                }
            });
        }
    </script>
</body>
</html>
"""
    return html