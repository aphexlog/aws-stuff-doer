import pkg_resources

def get_version():
    package_name = "aws-stuff-doer"

    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return "unknown"
