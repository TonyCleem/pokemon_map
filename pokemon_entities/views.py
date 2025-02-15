import folium
import json


from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now_moscow = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now_moscow, disappeared_at__gte=now_moscow)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    now_moscow = localtime()
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entity.filter(appeared_at__lte=now_moscow, disappeared_at__gte=now_moscow)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url)
        )

    pokemon_page = {
        "title_ru": pokemon.title,
        "img_url": request.build_absolute_uri(pokemon.photo.url),
        "description": pokemon.description,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp
    }

    if pokemon.next_evolution.all():
        pokemon_page.update({
            "next_evolution": {
                "title_ru": pokemon.next_evolution.get(id=(pokemon.id + 1)),
                "pokemon_id": pokemon.next_evolution.get(id=(pokemon.id + 1)).id,
                "img_url": request.build_absolute_uri(pokemon.next_evolution.get(id=(pokemon.id + 1)).photo.url)
            }
        })

    if pokemon.previous_evolution:
        pokemon_page.update({
            "previous_evolution": {
                "title_ru": pokemon.previous_evolution.title,
                "pokemon_id": pokemon.previous_evolution.id,
                "img_url": request.build_absolute_uri(pokemon.previous_evolution.photo.url)
            }
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_page
    })