#!/usr/bin/env python3

import json
import yaml
import argparse

#Convert query parameter types to OpenAPI types
def convert_type(param_type):
    if param_type == "int":
        return "integer", None
    elif param_type == "Boolean":
        return "boolean", None
    elif param_type == "String":
        return "string", None
    elif param_type == "UUID":
        return "string", "uuid"
    else:
        return param_type, None

#Convert requestBody types to OpenAPI schema
def convert_request_body(request_body):
    properties = {}
    for field, field_type in request_body.items():
        if isinstance(field_type, dict):
            # If it's a nested object, recursively convert it
            properties[field] = {
                "type": "object",
                "properties": convert_request_body(field_type)
            }
        else:
            type_converted, format_converted = convert_type(field_type)
            properties[field] = {
                "type": type_converted
            }
            if format_converted:
                properties[field]["format"] = format_converted
    return properties


#Generate Swagger paths
def generate_paths(json_data):
    paths = {}

    for endpoint in json_data:
        api_path = endpoint["apiPath"]
        http_method = endpoint["httpMethod"].lower()
        query_params = endpoint.get("queryParams", {})

        # Prepare query parameters
        parameters = []
        for param_name, param_type in query_params.items():
            param_type_converted, _ = convert_type(param_type)
            param_spec = {
                "in": "query",
                "name": param_name,
                "schema": {
                    "type": param_type_converted
                },
                "required": True
            }
            parameters.append(param_spec)

        # Check for requestBody and add it if present
        request_body = endpoint.get("requestBody", None)
        request_body_spec = {}
        if request_body:
            request_body_spec = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": convert_request_body(request_body)
                        }
                    }
                }
            }

        # Add to paths dictionary
        if api_path not in paths:
            paths[api_path] = {}

        paths[api_path][http_method] = {
            "summary": f"{http_method.upper()} {api_path}",
            "parameters": parameters,
            "requestBody": request_body_spec if request_body else None,
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object"
                            }
                        }
                    }
                },
                "400": {
                    "description": "Invalid request"
                },
                "404": {
                    "description": "Resource not found"
                }
            }
        }

        # Remove requestBody if not present, to avoid including an empty field
        if not request_body:
            del paths[api_path][http_method]["requestBody"]

    return paths


#Generate the Swagger structure
def generate_swagger_structure(json_data):
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "SwaggerWiz",
            "description": "API generated from JSON",
            "version": "1.0.0"
        },
        "paths": generate_paths(json_data)
    }

def read_json(input_path):
    with open(input_path, 'r') as file:
        return json.load(file)


def save_output(swagger_structure, output_path):
    with open(output_path, 'w') as yaml_file:
        yaml.dump(swagger_structure, yaml_file, sort_keys=False)
    print(f"Swagger YAML file generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert a JSON API definition to a Swagger YAML file.")
    parser.add_argument('-i', '--input-file', dest='json_file', help="Input JSON file", required=True)
    parser.add_argument('-o', '--output', dest='output_swagger_file', help="Output Swagger File path", required=True)    
    args = parser.parse_args()

    json_data = read_json(args.json_file)
    swagger_structure = generate_swagger_structure(json_data)
    save_output(swagger_structure, args.output_swagger_file)

if __name__ == "__main__":
    main()
