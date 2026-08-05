from itertools import product


class ParameterGrid:
    """
    Generates every parameter combination.
    """

    @staticmethod
    def generate(parameter_space):

        parameter_names = list(parameter_space.keys())

        parameter_values = [
            parameter_space[name]["values"]
            for name in parameter_names
        ]

        combinations = []

        for combination in product(*parameter_values):

            combinations.append(
                dict(zip(parameter_names, combination))
            )

        return combinations