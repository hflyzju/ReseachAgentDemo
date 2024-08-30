import json


class Paper:

    def __init__(self, title, abstract, related_paper_titles, related_paper_abstract, entities):
        self.title = title
        self.abstract = abstract
        self.related_paper_titles = related_paper_titles
        self.related_paper_abstract = related_paper_abstract
        self.entities = entities


    def __str__(self):
        return json.dumps(
            {
                "title": self.title,
                "abstract": self.abstract,
                "related_paper_titles": self.related_paper_titles,
                "related_paper_abstract": self.related_paper_abstract,
                "entities": self.entities
            },
            ensure_ascii=False
        )

    def _to_dict(self):
        return {
                "title": self.title,
                "abstract": self.abstract,
                "related_paper_titles": self.related_paper_titles,
                "related_paper_abstract": self.related_paper_abstract,
                "entities": self.entities
            }

def load_paper_from_file(paper_file):
    """加载paper数据"""
    with open(paper_file, 'r') as fr:
        data = json.load(fr)
        return Paper(
            title=data['title'],
            abstract=data['abstract'],
            related_paper_titles=data['related_paper_titles'],
            related_paper_abstract=data['related_paper_abstract'],
            entities=data['entities'],
        )

def load_paper_from_dict(paper_dict):
    """加载paper数据"""
    return Paper(
        title=paper_dict['title'],
        abstract=paper_dict['abstract'],
        related_paper_titles=paper_dict['related_paper_titles'],
        related_paper_abstract=paper_dict['related_paper_abstract'],
        entities=paper_dict['entities'],
    )


