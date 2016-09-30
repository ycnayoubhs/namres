# pylint: skip-file

from .models import CustomConverter

def convert_customizable(context, converter):
    if not isinstance(converter, CustomConverter):
        return 'The converter should be a CustomConverter instance.', ''

    output = converter.output
    converted = ''

    try:
        exec(converter.context)
        if converter.output_type == 'F':
            converted = eval('%s(context)' % output)
        elif converter.output_type == 'S':
            converted = eval(output)
        else:
            return 'Invalid output type of the converter.', ''
    except Exception as ex:
        print(ex.message)
        return 'Invalid custom converter configuration.', ''

    return converted, ''
