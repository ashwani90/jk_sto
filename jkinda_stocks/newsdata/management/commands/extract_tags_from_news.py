# extract nouns from the news
# classify nouns to what they are
# and save them to db

# !pip install -U spacy
# !python -m spacy download en_core_web_sm
from django.core.management.base import BaseCommand, CommandError
from newsdata.models import NewsData
import spacy

nlp = spacy.load("en_core_web_sm")

class Command(BaseCommand):
    help = "Download and save news"
    headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # get news data
        news_data = NewsData.objects.filter(processed=False)
        for news in news_data:
            self.parse_news_data(news)
            self.stdout.write(
                self.style.SUCCESS('Processed id: "%s" ' % news.id)
            )
            
        
    def parse_news_data(self, news_data):
        data = news_data.data
        id = news_data.id
        data = data.replace("  ", "")
        data = data.replace("\n", "")
        data = data.split(".")
        tags = []
        generic_nouns = []
        nouns_phrases = []
        all_tags = ""
        all_generic_nouns = ""
        all_nouns_phrases = ""
        for da in data:
            da = da.strip()
            doc = nlp(da)
            if (da):
                generic_nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
                nouns_phrases = [chunk.text for chunk in doc.noun_chunks]
                tags = self.extract_proper_nouns(doc)
                all_tags = self.remove_extra_and_convert_to_string(tags, all_tags)
                all_generic_nouns = self.remove_extra_and_convert_to_string(generic_nouns, all_generic_nouns)
                all_nouns_phrases = self.remove_extra_and_convert_to_string(nouns_phrases, all_nouns_phrases)
            
        NewsData.objects.filter(id=id).update(tags=all_tags, generic_nouns=all_generic_nouns, nouns_phrases=all_nouns_phrases, processed=True)
           
    def remove_extra_and_convert_to_string(self, tags, all_tags):
        for tag in tags:
            if (str(tag).strip()):
                tag = str(tag).replace("\n", "")
                all_tags = all_tags + tag + ","
        return all_tags
    
    def extract_proper_nouns(self, doc):
        pos = [tok.i for tok in doc if tok.pos_ == "PROPN"]
        consecutives = []
        current = []
        for elt in pos:
            if len(current) == 0:
                current.append(elt)
            else:
                if current[-1] == elt - 1:
                    current.append(elt)
                else:
                    consecutives.append(current)
                    current = [elt]
        if len(current) != 0:
            consecutives.append(current)
        return [doc[consecutive[0]:consecutive[-1]+1] for consecutive in consecutives]