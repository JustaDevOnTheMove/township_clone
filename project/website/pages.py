import json

from flask import render_template, send_from_directory, current_app, redirect, url_for, request

from . import pages_blueprint


columns = 20
rows = 32


#######################################################
# PAGES
#######################################################
@pages_blueprint.route('/')
def index(msg=''):
    # board = []
    # tile = ''
    # # data = {}
    # for i in range(rows):
    #     list = []
    #     for j in range(columns):
    #         tile = f'{i+1}'+'-'+f'{j+1}'
    #         data = {
    #             "row": i,
    #             "col": j,
    #             "tile": "grass",
    #         }
    #         list.append(data)
    #     board.append(list)

    with open('board.json', 'r') as file:
        data = json.load(file)

    return render_template('pages/index.html', cols=columns, rows=rows, board=data['board'], msg=request.args.get('msg'))



@pages_blueprint.route('/terraform/', methods=['GET'])
def terraform():
    if int(request.args.get('row')) > -1 or int(request.args.get('col')) > -1 or request.args.get('material') in ('grass, forest, sand, water, mountain'):
        file_path = 'board.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        data['board'][int(request.args.get('row'))][int(request.args.get('col'))] = {
                    "row": int(request.args.get('row')),
                    "col": int(request.args.get('col')),
                    "tile": request.args.get('material')
                }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        msg = f"updated {int(request.args.get('row'))} {int(request.args.get('col'))} to {request.args.get('material')}"
    else:
        msg = 'bad data'
    return redirect(url_for('pages.index', msg=msg))



@pages_blueprint.route('/re-generate/', methods=['GET'])
def regenerate():
    data = {
        'user':
        {
            'id': 1,
            'name': 'Jim',
            'level': 1,
        },
        'friends':
        [
            {
                'id': 2,
                'name': 'Amy',
                'level': 1,
            },
            {
                'id': 3,
                'name': 'John',
                'level': 1,
            },
        ],
    }
    board_data = []
    for i in range(rows):
        row_data = []
        for j in range(columns):
            tile_data = {
                "row": i,
                "col": j,
                "tile": "grass",
            }
            row_data.append(tile_data)
        board_data.append(row_data)
    data['board'] = board_data
    with open('board.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    msg = 'regenerated'
    return redirect(url_for('pages.index', msg=msg))



#######################################################
# IDEAS
#######################################################
# @pages_blueprint.route('/test/')
# def test():
#     return render_template('ideas/test.html')



#######################################################
# ERRORS
#######################################################
# This is specifically for netlify.com which is where the demo is currently hosted.
# Your hosting provider might need error pages handled differently.
# Please see the netlify.toml file in the root of the project for more info.
# The Flask Error pages are defined in `project/__init__.py`
@pages_blueprint.route('/404/')
def static_error_404():
    return render_template('error/404.html')
