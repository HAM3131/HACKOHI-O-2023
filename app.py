from flask import Flask, render_template, request, jsonify
import json
import interior
import pathfinding
from makeUnion import unionSpace as space
from web_generator import gen_base_html

app = Flask(__name__)

@app.route('/')
def index():
    html = gen_base_html(space)
    with open("templates/index.html", "w", encoding='utf-8') as f:
        f.write(html)

    return render_template('index.html')

@app.route('/get_path', methods=['POST'])
def get_path():
    data = request.json
    start_node = data['start_node']
    end_node = data['end_node']
    blacklist = data['blacklist']

    # Create a copy of the space with blacklisted NodeTypes removed
    space_copy = interior.blacklistedSpaceCopy(space, blacklist)

    # Find the shortest path
    path = pathfinding.pathFindingAlgorithm(space_copy, start_node, end_node)

    return jsonify({'path': path[0]})

if __name__ == '__main__':
    app.run(debug=True)