import sympy
from sympy.parsing.latex import parse_latex

functions = [
    # {
    #     "name": "request_method_selection",
    #     "description": "Returns the users' chosen method to solve the problem.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "values": {
    #                 "type": "array",
    #                 "description": "A list of methods to choose from.",
    #                 "items": {
    #                     "type": "string",
    #                     "description": "A method to choose from.",
    #                 },
    #                 "example": ["Shell Method", "Disk Method", "Washer Method"]
    #             }
    #         },
    #         "required": ["values"]
    #     }
    # },
    {
        "name": "use_formula",
        "description": "Solves problems using a provided formula.",
        "parameters": {
            "type": "object",
            "properties": {
                "friendly_name": {
                    "type": "string",
                    "description": "The name of the formula to use.",
                    "example": "Volume of Solid of Revolution (Shell Method)"
                },
                "formula": {
                    "type": "string",
                    "description": "The formula to substitute values into, as an expression in valid LaTeX format. Use quadruple backslashes to escape backslashes.",
                    "example": r"2\\\\pi\\\\int_{a}^{b}xf\\\\left(x\\\\right)dx"
                },
                "values": {
                    "type": "array",
                    "description": "A list of values to substitute into the formula.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "variable": {
                                "type": "string",
                                "description": "The variable or function to substitute the value into.",
                                "example": r"f\\\\left(x\\\\right)"
                            },
                            "value": {
                                "type": "string",
                                "description": "The value to substitute into the variable, as an expression in valid LaTeX format. Use quadruple backslashes to escape backslashes.",
                                "example": r"\\\\frac{1}{2}\\\\left(x\\\\right)^{2}"
                            }
                        }
                    }
                },
            },
            "required": ["friendly_name", "formula", "values"]
        }
    }
]


def use_formula(formula, values):
    parsed = parse_latex(formula)

    for value in values:
        parsed = parsed.subs(parse_latex(value["variable"]), parse_latex(value["value"]))
    print(parsed.evalf())
    return sympy.printing.latex(parsed.evalf())


def parse_expr(expression):
    return parse_latex(expression)
