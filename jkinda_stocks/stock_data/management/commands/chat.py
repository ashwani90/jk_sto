from django.core.management.base import BaseCommand, CommandError
from chatterbot import ChatBot

class Command(BaseCommand):
    help = "Chat the app"

    def add_arguments(self, parser):
        parser.add_argument("--query", nargs="+", type=str)
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        query = "Hello"
        if options['query']:
            query = options["query"][0]
        
        chatbot = ChatBot("Chatpot")
        print(f"🪴 {chatbot.get_response(query)}")