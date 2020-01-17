class BoxOfficeMojo:
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse(film):
        if film["Boxofficemojo"] is not None:
            bom = BoxOfficeMojo(film["Boxofficemojo"]['Link'])
            return bom
