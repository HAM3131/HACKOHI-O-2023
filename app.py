from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session  
import json
import interior
import pathfinding
from makeUnion import unionSpace as space
from web_generator import gen_base_html, gen_result_html

app = Flask(__name__)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
    
    # Store the path in the session
    session['path'] = path[0]

    return jsonify({'redirect': url_for('show_path')})

@app.route('/show_path')
def show_path():
    path = session.get('path', [])
    with open("templates/path_result.html", "w", encoding='utf-8') as f:
        f.write(gen_result_html(space, path))
    return render_template('path_result.html', path=path)

if __name__ == '__main__':
    app.run(debug=True)