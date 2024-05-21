from helpers.openai import OpenAI
import fastavro
import json


class OpenAISchemaConverter(OpenAI):

    def json_to_avro(
        self,
        json_schema: str,
    ):

        template = self.env.get_template("schemas_json_to_avro.jinja")
        prompt = template.render(json_schema=json_schema)

        print(prompt)
        return self._call_openapi(prompt)

    def avro_to_json(
        self,
        avro_schema: str,
    ):

        template = self.env.get_template("schemas_avro_to_json.jinja")
        prompt = template.render(avro_schema=avro_schema)

        print(prompt)
        return self._call_openapi(prompt)

    def sample_data(
        self,
        schema: str,
    ):

        template = self.env.get_template("schemas_sample_data.jinja")
        prompt = template.render(schema=schema)

        print(prompt)
        return self._call_openapi(prompt)
