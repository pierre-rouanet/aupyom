import pkg_resources

def example_audio_file():
    return pkg_resources.resource_filename(__name__, "example_data/Tom's Dinner.wav")
