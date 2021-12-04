from flask import Flask, request
from source_parsers.yummy_parser import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    obj_parser = YummyParser()
    anime_titles = obj_parser.parse(request.args.get('title'))
    i = 1
    anime_list_ongoing = ""
    anime_list_not_ongoing = ""
    for anime in anime_titles:
        if int(anime["ongoing"]) == 1:
            anime_list_ongoing += str(i)+') '+anime['name'] + '<br>'
        else:
            anime_list_not_ongoing += str(i)+') '+anime['name'] + '<br>'
            i += 1
    anime_list_string = "Уже вышли:<br>" + anime_list_not_ongoing + "Ещё выходят:<br>" + anime_list_ongoing
    return anime_list_string


json_string = """
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        ]
    }
}
"""

data = json.loads(json_string)

json_string = """

{
    [
        finished: 
        [
            {
                "title": "Наруто ураганные додики",
                "series": "600"
            }
        ],
        still coming out: 
        [
            {
                "title": "Боруто наркоман",
                "series": "100"
            }             
        ]
    ]       
}

"""


def run_api():
    app.run()
