from flask import Blueprint, render_template
from datetime import date

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return 'Homepage'

