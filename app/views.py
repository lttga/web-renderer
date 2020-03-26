from flask import Flask, request, abort, jsonify, send_from_directory, send_file
import json
import logging

from app import app
from app.renderer import RenderDocxObject, File, TemplateFile
from app.constants import TEMPLATES_FOLDER
from app.utils import remove_temp_files, does_data_attached
from app.exceptions import (
    JSONNotFound,
    TemplateNotFound)


@app.route('/', methods=['POST'])
def post():
    json_data = request.form.get('json_data')
    template_file = request.files.get('template')
    does_data_attached(template_file, json_data)
    content = json.loads(json_data)
    docx_file = TemplateFile(template_file)
    renderer = RenderDocxObject(content, docx_file)
    renderer.render()
    generated_file = TEMPLATES_FOLDER + \
        renderer.generated_pdf_path.split("/")[-1]
    return send_file(generated_file,  as_attachment=True)


@app.after_request
def after_request_func(response):
    remove_temp_files()
    app.logger.info('Tempfiles are removed')
    app.logger.info('Request is finished')
    return response