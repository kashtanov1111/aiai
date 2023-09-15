import os
import sys

sys.path.insert(0, "/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
import django

django.setup()

import openai

from django_project import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

        Animal: Cat
        Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
        Animal: Dog
        Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
        Animal: {}
        Names:""".format(
        animal.capitalize()
    )


def call_openai(animal):
    openai.api_key = OPENAI_API_KEY

    response = openai.Completion.create(
        engine="text-davinci-003", prompt="How are you?", temperature=1
    )
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {
    #             "role": "assistant",
    #             "content": "The Los Angeles Dodgers won the World Series in 2020.",
    #         },
    #         {"role": "user", "content": "Where was it played?"},
    #     ],
    # )

    # return response.choices[0].text.strip()
    # response['choices'][0]['message']['content']
    return response


print(call_openai("horse"))
