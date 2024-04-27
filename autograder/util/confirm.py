def confirm(prompt, default="no"):
    """
    Prompts the user for a confirmation and returns a boolean value based on their response.

    Args:
        prompt (str): The prompt message to display to the user.
        default (str, optional, "yes" or "no"): The default answer if no input is provided. Defaults to "no".

    Returns:
        bool: True if the user confirms with 'yes' or 'y', False if the user hits enter or enters 'no' or 'n'.
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}

    if default not in valid:
        raise ValueError(
            "Invalid default answer: '{}', expected 'yes' or 'no'.".format(default)
        )

    # Set the default response in the prompt message
    if default == "yes":
        prompt += " [Y/n] "
    else:
        prompt += " [y/N] "

    while True:
        choice = input(prompt).strip().lower()

        # If no input is provided, use the default value
        if choice == "":
            return valid[default]

        if choice in valid:
            return valid[choice]

        print("Please answer with 'yes' or 'no'.")
