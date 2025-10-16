import re

from ..logger import logger


def transform_string_function_style(name: str) -> str:
    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Replace non-alphanumeric characters with underscores
    transformed_name = re.sub(r"[^a-zA-Z0-9_]", "_", name)

    if transformed_name != name:
        final_name = transformed_name.lower()
        logger.warning(
            f"Tool name {name!r} contains invalid characters for function calling and has been "
            f"transformed to {final_name!r}. Please use only letters, digits, and underscores "
            "to avoid potential naming conflicts."
        )

    return transformed_name.lower()


def validate_agent_name(name: str) -> None:
    """Validate agent name and provide helpful guidance.

    Agent names are used in handoffs, tracing, and debugging. This function ensures
    that agent names follow good conventions and will work well throughout the system.

    Args:
        name: The agent name to validate

    Raises:
        ValueError: If the name has issues that should be fixed
    """
    if not name:
        raise ValueError("Agent name cannot be empty")

    if not name.strip():
        raise ValueError("Agent name cannot be only whitespace")

    # Check for common problematic patterns
    if name != name.strip():
        raise ValueError(
            f"Agent name {name!r} has leading/trailing whitespace. "
            f"Consider using {name.strip()!r} instead."
        )

    # Check for problematic special characters (but allow Unicode letters)
    # We allow: letters (including Unicode), numbers, spaces, hyphens, underscores
    problematic_chars = []
    for char in name:
        # Allow letters (any Unicode letter), digits, spaces, hyphens, underscores
        if not (char.isalnum() or char in (" ", "-", "_")):
            problematic_chars.append(char)

    if problematic_chars:
        unique_chars = sorted(set(problematic_chars))
        raise ValueError(
            f"Agent name {name!r} contains special characters {unique_chars} that may cause issues "
            f"in handoffs or function calls. Consider using only letters, numbers, spaces, "
            f"hyphens, and underscores."
        )

    # Check for very long names that might be unwieldy
    if len(name) > 100:
        raise ValueError(
            f"Agent name {name!r} is {len(name)} characters long. "
            f"Consider using a shorter, more concise name (under 100 characters)."
        )

    # Check for names that start with numbers (can cause issues in some contexts)
    if name[0].isdigit():
        raise ValueError(
            f"Agent name {name!r} starts with a number. Consider starting with a letter instead."
        )
