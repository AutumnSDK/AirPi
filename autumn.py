# -*- coding: utf-8 -*-

import output
import requests
import json
import datetime


class Autumn(output.Output):
    requiredData = ["host", "organization_key", "api_key", "element_id"]
    optionalData = []

    def __init__(self, data):

        self.name = type(self).__name__
        self.params = {}
        for key, value in data.items('Autumn'):
            setattr(self, key, value)
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.000Z"

    def _generate_body(self, point):

        today = datetime.datetime.now()

        return json.dumps({
            "data": {
                "type": "SensorData",
                "id": self.element_id,
                "attributes": {
                    "is_public": false,
                    "timestamp": today.strftime(self.datetime_format),
                    "value": str(point.get['value'])
                },
                "relationships": {
                    "sensor": {
                        "data": {
                            "type": "Sensor",
                            "id": self.element_id
                        }
                    }
                }
            }
        })

    def _generate_headers(self):

        return {
            'ORGANIZATION-ID': self.organization_key,
            'ORGANIZATION-API-KEY': self.api_key,
            'Content-Type': 'application/vnd.api+json'
        }

    def _generate_path(self):
        return '/api/external/v1/sensors/%s/sensordata/' % self.element_id

    def output_data(self, datapoints, *args, **kwargs):

        for i in datapoints:
            try:

                response = requests.post(
                    self._generate_path(), headers=self._generate_headers(), data=self._generate_body(i))
                if response.status_code != 201:
                    return False

            except Exception:
                return False

        return True
