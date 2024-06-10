from typing import List

import httpx
from furl import furl
from pathlib import Path

import domain
from domain import Pokemon


class Scrap:
    url = ""

    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> dict | None:
        res = httpx.get(self.url)
        if res.status_code == 200:
            return dict(res.json())
        return None

    def update(self, url: str):
        self.url = url
        return self

    def download(self, output_file: str):
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        res = httpx.get(self.url)
        if res.status_code == 200:
            with open(output_file, "wb") as file:
                file.write(res.content)


def get_all_pokemons_links(url: str, limit: int = 100) -> List[dict]:
    scrap = Scrap(url)
    content = scrap.fetch()
    total = content.get("count", 0)

    next_url = content.get('next', None)

    pokemons = content.get("results", [])
    print("\r\tFetching pokemon data ({} / {})".format(len(pokemons), total), end="")

    while next_url is not None:
        parsed_url = furl(next_url)
        parsed_url.query.set({"offset": parsed_url.args["offset"]})
        parsed_url.query.set({"limit": limit})

        content = scrap.update(parsed_url.url).fetch()
        next_url = content.get("next", None)
        pokemons += content.get("results", [])
        print("\r\tFetching pokemon data ({} / {})".format(len(pokemons), total), end="")

    return pokemons


def get_pokemon(name: str, url: str, static_folder: str) -> domain.Pokemon | None:
    scrap = Scrap(url)
    print("\n\tFetching pokemon {} from {}".format(name, url), end="")
    data = scrap.fetch()
    if data is not None:
        poke = Pokemon()
        poke.unmarshall(data)

        path = Path(static_folder + "/images/{}/".format(name))

        path.mkdir(parents=True, exist_ok=True)

        artwork = str(path) + "/artwork.png"
        back = str(path) + "/animated/back.gif"
        front = str(path) + "/animated/front.gif"

        scrap.update(poke.images.cover).download(artwork)
        poke.images.cover = "/" + artwork

        scrap.update(poke.images.animated.back).download(back)
        poke.images.animated.back = "/" + back

        scrap.update(poke.images.animated.front).download(front)
        poke.images.animated.front = "/" + front

        return poke
    return None
