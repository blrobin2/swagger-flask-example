import uuid

from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

measurements = []

shared_measurement_fields = dict(
    timestamp=fields.Integer(
        description='Timestamp of measurement',
        required=True,
        example=1606509272
    ),
    temperature=fields.Float(
        description='Measured temperature',
        required=True,
        example=22.3
    ),
    notes=fields.String(
        description='Additional notes',
        required=False,
        example='Strange day'
    ),
)

add_measurement_request_body = api.model(
    'AddMeasurementRequestBody',
    shared_measurement_fields
)

measurement_model = api.model(
    'Measurement', dict(
        id=fields.String(
            description='Unique ID',
            required=False,
            example='83ccd7e7-06ca-48dc-91de-8ae8cd5103ac'
        ),
        **shared_measurement_fields
    )
)


@api.route('/measurements')
class Measurements(Resource):
    @api.doc(model=[measurement_model])
    def get(self):
        return measurements

    @api.doc(model=[measurement_model], body=add_measurement_request_body)
    def post(self):
        measurement = dict(
            id=str(uuid.uuid4()),
            timestamp=request.json['timestamp'],
            temperature=request.json['temperature'],
            notes=request.json.get('notes'),
        )
        measurements.append(measurement)

        return measurement


if __name__ == '__main__':
    app.run()
