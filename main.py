import asyncio
from bs4 import BeautifulSoup
import itertools
import pandas
from aiohttp_client_cache import CachedSession, FileBackend

ROOT_URL = (
    "https://www.jamesbeard.org/awards/search?categories%5BRestaurant+%26+Chef%5D=1"
)


async def get_winners():
    async with CachedSession(cache=FileBackend()) as session:
        n_pages = await get_n_pages(session)
        tasks = [
            asyncio.create_task(get_page(session, i)) for i in range(1, 1 + n_pages)
        ]
        df = pandas.DataFrame.from_records(
            map(parse_winner, itertools.chain.from_iterable(await asyncio.gather(*tasks)))
        )
        df.to_csv("winners.csv", index=False)

def parse_winner(winner: list[str]):
    match winner:
        case [name, category, ranking, year_str]:
            location = None
            chef = None
        case [name, category, location, ranking, year_str]:
            chef = None
        case [name, category, location, _, ranking, year_str]:
            chef = None
        case [chef, category, name, location, _, ranking, year_str]:
            pass

    return {
        "name": name,
        "year": int(year_str),
        "place": name,
        "chef": chef,
        "category": category,
        "location": location,
        "ranking": ranking,
    }


async def get_n_pages(session: CachedSession) -> int:
    response = await session.get(ROOT_URL)
    response.raise_for_status()
    html = await response.text()
    soup = BeautifulSoup(html, "html.parser")
    # Return the text of the second to last pagination, the one before the next tag
    return int(soup.find(class_="pagination").find_all("li")[-2].text)


async def get_page(session: CachedSession, index: int):
    url = f"{ROOT_URL}&page={index}"
    response = await session.get(url)
    response.raise_for_status()
    html = await response.text()
    soup = BeautifulSoup(html, "html.parser")
    winners = soup.find_all(class_="c-award-recipient")
    return [
        get_fields(winner)
        for winner in winners
        if winner["data-award-template"] != "template not found"
    ]


def get_fields(winner):
    fields = [
        winner.find(class_="c-award-recipient__name"),
        *winner.find_all(class_="c-award-recipient__text"),
    ]
    return [field.text.strip() for field in fields]

asyncio.run(get_winners())
