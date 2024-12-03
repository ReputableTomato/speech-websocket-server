import copy

from Erebus.Generic.Networking.NetworkValidation import NetworkValidation
from Erebus.Generic.Utilities.Email import Email

class Comparison:

    @staticmethod
    def validate_dictionary_values(template, dictionary):
        """A method to compare a template and an input dictionary.
        If there is a value mismatch between the template and
        the dictionary, an error will be returned.

        Args:
            template (dictionary): The template dictionary.
            dictionary (dictionary): The dictionary containing the data.

        Returns:
            dictionary: The result of the comparison.
        """
        response = None
        original = copy.deepcopy(dictionary)

        while True:
            try:
                # Remove the item from the template dictionary.
                item = template.popitem()
                parameter_name = item[0]
                value = item[1]

                if parameter_name in dictionary.keys():
                    parameter_value = dictionary[parameter_name]

                    if type(parameter_value) == value:
                        dictionary.pop(parameter_name)

                    # If the value we're checking is a dictionary, we will loop around.
                    elif isinstance(parameter_value, dict):
                        response = __class__.validate_dictionary_values(value, dictionary.get(parameter_name))

                        # If the response of that loop is failure, we will return here.
                        if response and not response["result"]:
                            break
                    # If we have specified further requirements for a parameter, we will process them here.
                    elif isinstance(value, dict) and "route_options" in value:
                        route_options = value["route_options"]

                        if "validate_params" in route_options:
                            response = __class__.process_additional_requirements(value, parameter_name, parameter_value, dictionary, original)

                            if not response:
                                dictionary.pop(parameter_name)
                            else:
                                break
                    # The value in our dictionary is not the same as the template requirement.
                    else:
                        response = __class__.comparison_response(False, parameter_name, value)
                        break
                elif isinstance(value, dict) and "route_options" in value:
                    route_options = value["route_options"]

                    if "optional" in route_options:
                        continue
                    else:
                        response = __class__.comparison_response(False, parameter_name, value["type"])
                        break
                # The template key is not in our dictionary.
                else:
                    if isinstance(value, dict) and "validate_params" in value:
                        response = __class__.comparison_response(False, parameter_name, value["type"])
                    else:
                        response = __class__.comparison_response(False, parameter_name, value)
                    break
            except KeyError:
                response = __class__.comparison_response(True, original = original)
                break

        return response

    @staticmethod
    def comparison_response(result, attribute_name = None, attribute_type = None, original = None, error = None):
        """A method to return a comparison.

        Args:
            result (boolean): Whether or not the result was successful.
            attribute_name (string): The attribute name. Default is none.
            attribute_type (string): The attribute type. Default is none.

        Returns:
            dictionary: The dictionary containing the parameters passed.
        """
        if attribute_type:
            if attribute_type == "ip_address":
                pass
            elif attribute_type == "email_address":
                pass
            elif isinstance(attribute_type, dict):
                attribute_type = "dict"
            elif isinstance(attribute_type, int):
                attribute_type = "int"
            elif isinstance(attribute_type, str):
                attribute_type = "string"
            elif isinstance(attribute_type, list):
                attribute_type = "list"
            else:
                attribute_type = attribute_type.__name__

        return {
            "result": result,
            "attribute_name": attribute_name,
            "attribute_type": attribute_type,
            "original": original,
            "error": error
        }

    @staticmethod
    def validate_keys(required_keys, data) -> dict:
        response = {
            "result": True
        }

        for key in required_keys:
            if key not in data:
                response["result"] = False
                response["key"] = key

                return response

        return response

    @staticmethod
    def process_additional_requirements(requirements, parameter_name, parameter_value, dictionary, original):
        requirement_type = requirements["type"]

        if requirement_type is int:
            if not isinstance(parameter_value, int):
                return __class__.comparison_response(False, parameter_name, requirements["type"])
        elif requirement_type is str:
            if not isinstance(parameter_value, str):
                return __class__.comparison_response(False, parameter_name, requirements["type"])
        elif requirement_type is "ip_address":
            if not NetworkValidation.valid_ipv4_address(parameter_value):
                return __class__.comparison_response(False, parameter_name, requirement_type)
        elif requirement_type is "email_address":
            if not Email.validate_email(parameter_value):
                return __class__.comparison_response(False, parameter_name, requirement_type)
        else:
            print("{} has not been handled.".format(requirements["type"]))

            return False

        if "min" in requirements:
            if parameter_value < requirements["min"]:
                return __class__.comparison_response(False, parameter_name, parameter_value, error = "The parameter value does not meet the minimum value ({})".format(requirements["min"]))

        if "min_length" in requirements:
            if len(parameter_value) < requirements["min"]:
                return __class__.comparison_response(False, parameter_name, parameter_value, error = "The parameter value does not meet the minimum length ({})".format(requirements["min"]))

        if "max" in requirements:
            if parameter_value > requirements["max"]:
                return __class__.comparison_response(False, parameter_name, parameter_value, error = "The parameter value exceeds the maximum value ({})".format(requirements["max"]))

        if "max_len" in requirements:
            if len(parameter_value) > requirements["max_len"]:
                return __class__.comparison_response(False, parameter_name, parameter_value, error = "The parameter value exceeds the maximum length ({})".format(requirements["max_len"]))

        if "in" in requirements:
            if parameter_value not in requirements["in"]:
                return __class__.comparison_response(False, parameter_name, parameter_value, error = "This value can only be any of the following: {}".format(", ".join(requirements["in"])))