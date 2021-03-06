# Copyright (c) 2014-2015, NVIDIA CORPORATION.  All rights reserved.

import flask
import werkzeug.exceptions

from digits.webapp import app, scheduler, autodoc
from digits.utils.routing import request_wants_json
import images.views
import images as dataset_images

NAMESPACE = '/datasets/'

@app.route(NAMESPACE + '<job_id>.json', methods=['GET'])
@app.route(NAMESPACE + '<job_id>', methods=['GET'])
@autodoc(['datasets', 'api'])
def datasets_show(job_id):
    """
    Show a DatasetJob

    Returns JSON when requested:
        {id, name, directory, status}
    """
    job = scheduler.get_job(job_id)
    if job is None:
        raise werkzeug.exceptions.NotFound('Job not found')

    if request_wants_json():
        return flask.jsonify(job.json_dict(True))
    else:
        if isinstance(job, dataset_images.ImageClassificationDatasetJob):
            return dataset_images.classification.views.show(job)
        else:
            raise werkzeug.exceptions.BadRequest('Invalid job type')

@app.route(NAMESPACE + 'summary', methods=['GET'])
@autodoc('datasets')
def dataset_summary():
    """
    Return a short HTML summary of a DatasetJob
    """
    job = scheduler.get_job(flask.request.args['job_id'])
    if job is None:
        raise werkzeug.exceptions.NotFound('Job not found')

    return flask.render_template('datasets/summary.html', dataset=job)

