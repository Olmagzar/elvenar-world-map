This is a python script to generate a map of some fellowships from elvenar.
To add a fellowship, create a file with the name of the fellowship inside the
fellowships directory and add a dictionnary named 'conf' with 'name' and
'members' as keys and the fellowship name string for the first value and an
array of dictionaries for each members (with name, x, y and scout score).
For instance:
conf = {
    "name": "My_Awesome_Fellowship", "members": [
        { "name": "Me_TheKing", "x": 18, "y": -27, "scout": 57298 },
        { "name": "MyBro_TheFool", "x": -89, "y": -54, "scout": 32817 },
        { "name": "MaxiTotor", "x": -12, "y": 52, "scout": 18415 }
    ]
}


Here, in this example, the locations might be wrong since cities are placed at
specific points, some coordinates might point to a regular province.
To get the location of a city, you'll have to open your web developper tools to
inspect 'POST' responses when visiting a city. The object you are looking for has
"visitPlayer" as requestMethod. Inside the 'other_player' field contained by
the responseData one, there is a 'location' field showing coordinates 'r' and
'q'. Set x with the 'r' value and y with the 'q' value. On the world map, 'r'
grows to the east (assuming east is on the right side and west on the left)
and 'q' grows to the south. The scout score can be found hovering the player
score either in the ranking list or in the player's city.
As for getting your own coordinates, one way is to look for the json object
from the 'POST' response when opening the world map with the requestMethod
'fetchInitialWorldMapData'. You'll find a field 'player_world_map_area_vo' in
the responseData containing an array of 'provinces' : 6 regular one and 3 cities
one of which is yours. Look for the name to verify, and get the 'r' and 'q'
values associated with.

After adding the fellowship file, import it in the config.py file and add it in
the array.
For instance:

from fellowships import My_Awesome_Fellowship, Another_Cool_Fellowship

guildes = [
    My_Awesome_Fellowship.conf,
    Another_Cool_Fellowship.conf
]

More than one fellowship in the array will result with:
 - a map with members estimated exploration area per fellowship (_aura.png) ;
 - a map with members linked by a minimal covering tree generated with Prim's
   algorithm, using tiles as distance unit (same as province exploration
   distances or fight troups moves) per fellowship (_named.png) ;
 - a map with the first fellowship in blue and any other fellowship in orange,
   named after the first fellowship and the second one (_overlap_ .png)

The last map (overlap) aims to see a bit of trading opportunities between
fellowships for non-sentient goods.
