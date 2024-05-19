import pkg_resources

def get_version():
    # Replace 'your_package_name' with the actual name of your package as specified in the 'pyproject.toml' file.
    package_name = "aws-stuff-doer"

    try:
        # Get the distribution based on the package name and return its version.
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        # Handle the case where the distribution could not be found
        return "unknown"
