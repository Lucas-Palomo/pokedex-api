import json
import uuid
from abc import abstractmethod, ABC
from pypika import PostgreSQLQuery, Table
from pydantic import BaseModel


class JsonObject(ABC):
    @abstractmethod
    def marshall(self) -> str:
        pass

    @abstractmethod
    def unmarshall(self, data: dict):
        pass


class SQLStatements(ABC):

    @abstractmethod
    def get_insert_statement(self) -> str:
        pass


class PokemonAnimatedImage(BaseModel):
    front: str = ""
    back: str = ""

    # def to_dict(self):
    #     return {}


class PokemonImage(BaseModel):
    cover: str = ""
    animated: PokemonAnimatedImage = PokemonAnimatedImage()

    # def to_dict(self) -> dict:
    #     return {
    #         "cover": self.cover,
    #         "animated": self.animated.to_dict()
    #     }


class Pokemon(JsonObject, SQLStatements, BaseModel):
    id: uuid.UUID = ""

    external_id: int = 0

    name: str = ""
    weight: int = 0
    height: int = 0

    types: list[str] = []

    hp: int = 0
    speed: int = 0
    attack: int = 0
    defense: int = 0

    images: PokemonImage = PokemonImage()

    def __init__(self, data: dict | tuple | None = None):
        super().__init__()
        self.id = uuid.uuid4()

        if data is not None:
            if isinstance(data, dict):
                self.id = data.get("id")
                self.external_id = data.get("external_id")
                self.name = data.get("name")
                self.weight = data.get("weight")
                self.height = data.get("height")
                self.types = data.get("types")
                self.hp = data.get("hp")
                self.speed = data.get("speed")
                self.attack = data.get("attack")
                self.defense = data.get("defense")
                self.images.cover = data.get("images").get("cover")
                self.images.animated.front = data.get("images").get("animated").get("front")
                self.images.animated.back = data.get("images").get("animated").get("back")
            if isinstance(data, tuple):
                self.id = uuid.UUID(data[0])
                self.external_id = data[1]
                self.name = data[2]
                self.weight = data[3]
                self.height = data[4]
                self.types = data[5]
                self.hp = data[6]
                self.speed = data[7]
                self.attack = data[8]
                self.defense = data[9]
                self.images.cover = data[10][0]
                self.images.animated.front = data[10][1]
                self.images.animated.back = data[10][2]

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'external_id': self.external_id,
            'name': self.name,
            'weight': self.weight,
            'height': self.height,
            'types': self.types,
            'hp': self.hp,
            'speed': self.speed,
            'attack': self.attack,
            'defense': self.defense,
            'images': {
                "cover": self.images.cover,
                "animated": {
                    "front": self.images.animated.front,
                    "back": self.images.animated.back
                }
            }
        }

    def unmarshall(self, data: dict):
        self.external_id = data.get("id", 0)
        self.name = data.get('name', '')
        self.weight = data.get('weight', 0)
        self.height = data.get('height', 0)
        self.types = [entry.get('type', {}).get('name', '') for entry in data.get('types', [])]

        stats = data.get('stats', [])
        for entry in stats:
            value = entry.get('base_stat', 0)
            stat = entry.get('stat', {}).get('name', '')
            match stat:
                case 'hp':
                    self.hp = value
                case 'speed':
                    self.speed = value
                case 'defense':
                    self.defense = value
                case 'attack':
                    self.attack = value

        sprites = data.get('sprites', {})
        if len(sprites) > 0:
            other = sprites.get('other', {})
            if len(other) > 0:
                official_artwork = other.get('official-artwork', {})
                if len(official_artwork) > 0:
                    self.images.cover = official_artwork.get('front_default', '')

                showdown = other.get('showdown', {})
                if len(showdown) > 0:
                    self.images.animated.front = showdown.get('front_default', '')
                    self.images.animated.back = showdown.get('back_default', '')

    def marshall(self) -> str:
        return json.dumps(self.dict())

    def get_insert_statement(self) -> str:
        query = PostgreSQLQuery()

        table_columns = [
            "id",
            "external_id",
            "name",
            "weight",
            "height",
            "types",
            "hp",
            "speed",
            "attack",
            "defense",
            "images"
        ]

        values = [
            self.id,
            self.external_id,
            self.name,
            self.weight,
            self.height,
            self.types,
            self.hp,
            self.speed,
            self.attack,
            self.defense,
            [self.images.cover, self.images.animated.front, self.images.animated.back],
        ]

        query = query.into(Table("pokemon")).columns(table_columns).insert(values)

        return query.get_sql()
