from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Species, User

# Create a new SQLAlchemy Engine
engine = create_engine('sqlite:///plantnursery.db')

# Bind it to the metadata of the Base class in order to acesss our
# subclasses (Category, Species)
Base.metadata.bind = engine

# Create a new Session object, bind it to the engine, and initialize it for
# use communicating with the db
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create an existing user for testing that other users cannot modify entries
# they did not create
user1 = User(name="Joe Schmoe",
             email="joes@example.com",
             picture="")
session.add(user1)
session.commit()

# Seed the plantnursery db with some data
# Trees
category1 = Category(user_id=1, name="Trees")

session.add(category1)
session.commit()

species1 = Species(user_id=1,
                   name="Douglas-fir",
                   scientific_name="Pseudotsuga menziesii",
                   moisture_reqs="dry-moist",
                   exposure_reqs="sun - part shade",
                   description="The Douglas fir is host to many native species"
                   " of insect and bird.  Fast growing and predictable, it can"
                   " be grown in almost any native soil but will sometimes"
                   " blow down if planted in shallow soils over compacted clay"
                   " or glacial till.",
                   category=category1)

session.add(species1)
session.commit()

species2 = Species(user_id=1,
                   name="Western redcedar",
                   scientific_name="Thuja plicata",
                   moisture_reqs="moist - wet",
                   exposure_reqs="part shade - shade",
                   description="This is a grand and long lived tree, "
                   "achieving both height and breadth through 200-300 years."
                   " Ideal for lowland and dampish areas, it does better on"
                   " more level surfaces. ",
                   category=category1)

session.add(species2)
session.commit()

species3 = Species(user_id=1,
                   name="paper birch",
                   scientific_name="Betula papyrifera",
                   moisture_reqs="moist",
                   exposure_reqs="sun - part shade",
                   description="Paper birch is known for its white, peeling, "
                   "paper-like bark that is found in mature specimens. The "
                   "bark is dark in young trees. It has a smaller, more "
                   "delicate appearing leaf than alder and can look nice "
                   "planted in groves.",
                   category=category1)

session.add(species3)
session.commit()

species4 = Species(user_id=1,
                   name="vine maple",
                   scientific_name="Acer circinatum",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="One of the most desireable native plants, "
                   "this small tree is famous for fall color and its ability "
                   "to hold stream banks and eroding soil. Like the dogwood, "
                   "it grows best in the understory at the woodland edge but "
                   "will also grow more lankey in the forest interior and "
                   "smaller, denser in the open--where it can burn in the "
                   "afternoon sun.",
                   category=category1)

session.add(species4)
session.commit()

species5 = Species(user_id=1,
                   name="Pacific dogwood",
                   scientific_name="Cornus nuttallii",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade",
                   description="Beautiful spring bloomer with white blooms. "
                   "Red fruits provide lots of food for birds. Grows best "
                   "along forest edges with its roots protected from late "
                   "afternoon sun.",
                   category=category1)

session.add(species5)
session.commit()

# Shrubs
category2 = Category(user_id=1, name="Shrubs")

session.add(category2)
session.commit()

species1 = Species(user_id=1,
                   name="red-osier dogwood",
                   scientific_name="Cornus sericea",
                   moisture_reqs="moist - wet",
                   exposure_reqs="sun - shade",
                   description="This is an attractive plant almost year round."
                   " In the winter it is known for its flaming red bark and"
                   " in the spring and summer for it's light foliage that"
                   " flickers in the wind. Fall foliage is golden to reddish"
                   " on red stems. The small flowers are in large clusters"
                   " of frothy white. The berries are pale with a touch of"
                   " blue.",
                   category=category2)

session.add(species1)
session.commit()

species2 = Species(user_id=1,
                   name="low Oregon grape",
                   scientific_name="Mahonia nervosa",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="This is the short cousin to tall Oregon Grape"
                   " and is better used as a ground cover (generally 2 foot"
                   " in height) planted either singly or in masses. It looks"
                   " great combined with native snowberry above and through"
                   " the glossy green massed leaves. Tolerant of many"
                   " conditions, it will do its best in some shade and can"
                   " tolerate full shade. Clustered yellow flowers with"
                   " purple fruits.",
                   category=category2)

session.add(species2)
session.commit()

species3 = Species(user_id=1,
                   name="salal",
                   scientific_name="Gaultheria shallon",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="The single best ground cover for northwest"
                   " gardens, salal is a do it all plant. Long recognised as"
                   " one of the best foliage plants for flower arranging, it"
                   " is also one of the most adaptable in the native"
                   " repertoir. It can be grown short, if pruned back,"
                   " hedged into wave like drifts, allowed to grow rampant"
                   " and irregular to five feet or more. It will also grow"
                   " where almost nothing else will, in deep understory"
                   " forest groves, moist or dry soils, in full sun or"
                   " deep shade.",
                   category=category2)

session.add(species3)
session.commit()

species4 = Species(user_id=1,
                   name="nootka rose",
                   scientific_name="Rosa nutkana",
                   moisture_reqs="moist - wet",
                   exposure_reqs="sun - part shade",
                   description="Attractive pink blooms, and large red fruit"
                   " (hips) that persist in the winter. Covered with prickles,"
                   " aggressive spreader.",
                   category=category2)

session.add(species4)
session.commit()

species5 = Species(user_id=1,
                   name="Pacific rhododendron",
                   scientific_name="Rhododendron macrophyllum",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="It grows 15-20' on average. The leaves are 6 "
                   "inches long and are rather flat, evergreen and smooth on "
                   "the underside. The flowers can be rather large clusters "
                   "of rosy pink and rarely white. It can be used as a "
                   "thicket or wide, evergreen hedgerow. It blooms best on "
                   "forest edges but is known to bloom in dark forest as "
                   "well. Most garden rhododendron are species from Asia.",
                   category=category2)

session.add(species5)
session.commit()

species6 = Species(user_id=1,
                   name="spiraea",
                   scientific_name="Spiraea douglasii",
                   moisture_reqs="moist - wet",
                   exposure_reqs="sun - part shade",
                   description="Also known as 'hardhack'. Attractive, pink
                   "pyramid shaped flower "
                   "clusters. Can spread aggresively in moist environments, "
                   "but is better behaved in drier conditions.",
                   category=category2)

session.add(species6)
session.commit()

# Groundcover
category3 = Category(user_id=1, name="Groundcover")

session.add(category3)
session.commit()

species1 = Species(user_id=1,
                   name="Oregon iris",
                   scientific_name="Iris tenax",
                   moisture_reqs="moist - wet",
                   exposure_reqs="sun - part shade",
                   description="Attractive flowering blue to purple iris.",
                   category=category3)

session.add(species1)
session.commit()

species2 = Species(user_id=1,
                   name="wild strawberry",
                   scientific_name="Fragaria virginiana",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="Delightful woodland strawberry with white "
                   "flowers and red fruits. Spreads.",
                   category=category3)

session.add(species2)
session.commit()

species3 = Species(user_id=1,
                   name="Western columbine",
                   scientific_name="Aquilegia formosa",
                   moisture_reqs="moist",
                   exposure_reqs="sun - part shade",
                   description="Liking it a bit moist, this small columbine "
                   "will grow in open or shady sites and does best near the "
                   "coast. It can be grown in forest glades, rocky slopes, "
                   "meadows, clearings and meadows. Both butterflies and "
                   "hummingbirds like this delicate dangling plant.",
                   category=category3)

session.add(species3)
session.commit()

species4 = Species(user_id=1,
                   name="Western starflower",
                   scientific_name="Trientalis latifolia",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="Also known as 'Indian potato', this small "
                   "woodland wildflower is great for "
                   "adding some spring blooms in shady areas. Flower is white "
                   "to pink and appears to float above the whorl of leaves.",
                   category=category3)

session.add(species4)
session.commit()

species5 = Species(user_id=1,
                   name="oak fern",
                   scientific_name="Gymnocarpium dryopteris",
                   moisture_reqs="dry - moist",
                   exposure_reqs="part shade - shade",
                   description="The foliage of this delicate fern forms a "
                   "delightful spreading groundcover in a woodland setting. "
                   "Spreads by rhizomes, but not aggressive.",
                   category=category3)

session.add(species5)
session.commit()

species6 = Species(user_id=1,
                   name="camas, common",
                   scientific_name="Camassia quamash",
                   moisture_reqs="dry - moist",
                   exposure_reqs="sun - part shade",
                   description="Beautiful spikes of bluish purple flower "
                   "clusters. Spring blooming.",
                   category=category3)

session.add(species6)
session.commit()

species7 = Species(user_id=1,
                   name="wild ginger",
                   scientific_name="Asarum caudatum",
                   moisture_reqs="moist",
                   exposure_reqs="part shade - shade",
                   description="Attractive foliage, purplish flowers are "
                   "hidden beneath the foliage, but very beautiful when seen.",
                   category=category3)

session.add(species7)
session.commit()

# Grass-like
category4 = Category(user_id=1, name="Grass-like")

session.add(category4)
session.commit()

species1 = Species(user_id=1,
                   name="cattail",
                   scientific_name="Typha latifolia",
                   moisture_reqs="wet",
                   exposure_reqs="sun - part shade",
                   description="Cattail is quite common along lake shores and "
                   "wetlands and often is only limited in its spread by water "
                   "depth. It can outcompete other natives so plant it where "
                   "you don't mind it spreading. The unique cigar like "
                   "flowers provide interest, while the stand themselves "
                   "provide nesting sites.",
                   category=category4)

session.add(species1)
session.commit()

species2 = Species(user_id=1,
                   name="tufted hairgrass",
                   scientific_name="Deschampsia cespitosa",
                   moisture_reqs="dry - wet",
                   exposure_reqs="sun - part shade",
                   description="A narrow leaved bunch grass that is attractive"
                   " with the wind blowing through its tall seed plumes. Plant"
                   " in drifts of 5 or more for a meadow like effect. They"
                   " plants ususally do a nice job of reseeding themselves."
                   " Perfect for salt water shorelines.",
                   category=category4)

session.add(species2)
session.commit()

species3 = Species(user_id=1,
                   name="hardstem bulrush",
                   scientific_name="Scirpus acutus",
                   moisture_reqs="wet",
                   exposure_reqs="sun",
                   description="This very tall bulrush has tough, round stems"
                   " and works well along lakes and marshes. Needs saturated"
                   " soil conditons and sun. Spreads by rhizomes. Seeds are"
                   " important food for waterfowl.",
                   category=category4)

session.add(species3)
session.commit()

species4 = Species(user_id=1,
                   name="Lyngbye's sedge",
                   scientific_name="Carex lyngbyei",
                   moisture_reqs="wet",
                   exposure_reqs="sun - part shade",
                   description="This sedge forms widespread clumps in "
                   "estuaries. Excellent spreading sedge for salt water "
                   "shorelines.",
                   category=category4)

session.add(species4)
session.commit()

# Vines
category5 = Category(user_id=1, name="Vines")

session.add(category5)
session.commit()

species1 = Species(user_id=1,
                   name="blackberry, trailing",
                   scientific_name="Rubus ursinus",
                   moisture_reqs="dry - moist",
                   exposure_reqs="sun - shade",
                   description="This is not the big brambly invasive bully "
                   "lining area rivers and roadways. Although our native "
                   "blackberry likes to spread, it does not form self "
                   "supported brambles. Instead it rambles about the "
                   "landscape as a vine-like ground cover.",
                   category=category5)

session.add(species1)
session.commit()

species2 = Species(user_id=1,
                   name="tufted hairgrass",
                   scientific_name="Deschampsia cespitosa",
                   moisture_reqs="dry - wet",
                   exposure_reqs="sun - part shade",
                   description="A narrow leaved bunch grass that is attractive"
                   " with the wind blowing through its tall seed plumes. Plant"
                   " in drifts of 5 or more for a meadow like effect. They"
                   " plants ususally do a nice job of reseeding themselves."
                   " Perfect for salt water shorelines.",
                   category=category5)

session.add(species2)
session.commit()

species3 = Species(user_id=1,
                   name="hairy honeysuckle",
                   scientific_name="Lonicera hispidula",
                   moisture_reqs="dry - moist",
                   exposure_reqs="sun - part shade",
                   description="This native vine rambles along the ground "
                   "rather than climbing. Has very attractive pink flowers, "
                   "but can be a rather sparse bloomer. The leaves and stems "
                   "are fuzzy.",
                   category=category5)

session.add(species3)
session.commit()

print "Seeded the plantdb with existing entries."
