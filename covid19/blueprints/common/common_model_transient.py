class ApplicationPage:

    def __init__(self, default_title, default_subtitle=None, default_subtitle_info=None):
        self.title = default_title
        self.subtitle = default_subtitle
        self.subtitle_info = default_subtitle_info
        if self.subtitle is None:
            self.subtitle = """This is a simple hero unit, a simple jumbotron-style component 
                            for calling extra attention to featured content or information."""
        if self.subtitle_info is None:
            self.subtitle_info = """It uses utility classes for typography and spacing 
                    to space content out within the larger container."""