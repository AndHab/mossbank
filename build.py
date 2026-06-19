#!/usr/bin/env python3
"""Static builder for Mossbank. No dependencies: `python3 build.py` writes the
finished HTML pages into the repo root, wrapping each page body in the shared
chrome (nav, footer, analytics). Content lives in the PAGES dict below."""

import html
from datetime import date

SITE = "Mossbank"
BASE = "https://mossbank.de"
YEAR = date.today().year
LAUNCH = "2026-06-03"
INDEXNOW_KEY = "d8673e1556bb458288ac3b759652d297"

# (filename, what it shows, author, licence). All from Wikimedia Commons, served
# from /assets, credited on credits.html. Add a row when adding an image.
IMAGE_CREDITS = [
    ("hero.jpg", "Forest moss, Gullmarsskogen ravine", "W. Carter", "CC0"),
    ("sphagnum.jpg", "Sphagnum capillifolium, bog moss", "Krzysztof Ziarnek, Kenraiz", "CC BY-SA 4.0"),
    ("hypnum.jpg", "Hypnum cupressiforme, plait moss", "Robert Flogaus-Faust", "CC BY 4.0"),
    ("dicranum.jpg", "Dicranum scoparium, broom fork-moss", "Rafael Medina", "CC BY 4.0"),
    ("thuidium.jpg", "Thuidium tamariscinum, tamarisk moss", "Michael Becker", "CC BY-SA 3.0"),
    ("marimo.jpg", "Aegagropila linnaei, a marimo, Hokkaido", "bryan, Taipei", "CC BY-SA 2.0"),
    ("reindeer.jpg", "Cladonia rangiferina, reindeer lichen", "Tomas P.", "CC0"),
    ("leucobryum.jpg", "Leucobryum glaucum, bun moss", "Krzysztof Ziarnek, Kenraiz", "CC BY-SA 4.0"),
    ("sundew-sphagnum.jpg", "Drosera rotundifolia among Sphagnum", "Geoff Gallice", "CC BY 2.0"),
    ("monstera-pole.jpg", "Monstera climbing a coir and moss pole", "Secretlondon", "CC BY-SA 4.0"),
    ("kokedama.jpg", "Kokedama of ornamental plants", "Wee Hong", "CC BY-SA 4.0"),
    ("paludarium.jpg", "Paludarium, Grand Aquarium Saint-Malo", "Kev22", "CC BY-SA 4.0"),
    ("kusamono.jpg", "Kusamono with fern and strawberry", "Sage Ross", "CC BY-SA 3.0"),
    ("polytrichum.jpg", "Polytrichum commune, common haircap moss", "Hans Hillewaert", "CC BY-SA 4.0"),
    ("wall-screw-moss.jpg", "Tortula muralis, wall screw-moss, in fruit", "Alexis (iNaturalist)", "CC BY 4.0"),
    ("silvery-thread-moss.jpg", "Bryum argenteum, silvery thread-moss", "Randal (iNaturalist)", "CC0"),
    ("fontinalis.jpg", "Fontinalis antipyretica, willow moss, Hohenlohe", "Bernd Haynold", "CC BY-SA 3.0"),
    ("rhytidiadelphus.jpg", "Rhytidiadelphus squarrosus, springy turf-moss", "Michael Becker", "CC BY-SA 3.0"),
    ("grimmia.jpg", "Grimmia pulvinata, common pincushion, on rock", "Christian Berg", "CC BY 4.0"),
]

# GoatCounter: cookieless, self-hosted. One line, every page.
ANALYTICS = (
    '<script data-goatcounter="https://stats.mossbank.de/count" '
    'async src="//stats.mossbank.de/count.js"></script>'
    # GA4 + Consent Mode v2: granted by default worldwide, denied only in the
    # EEA/UK/Switzerland until the visitor accepts (Google applies region by IP)
    '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
    "gtag('consent','default',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});"
    "gtag('consent','default',{region:['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'],ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});</script>"
    '<script async src="https://www.googletagmanager.com/gtag/js?id=G-FNWN0VY4KF"></script>'
    "<script>gtag('js',new Date());gtag('config','G-FNWN0VY4KF');</script>"
    # EEA/UK/CH consent is handled by Google's certified CMP (AdSense GDPR message),
    # which updates the Consent Mode signals; non-EEA defaults to granted above.
    # Google AdSense
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7059699192160095" crossorigin="anonymous"></script>'
)

NAV = [
    ("index", "Home"),
    ("biology", "What is moss"),
    ("species", "Species"),
    ("growing", "Growing"),
    ("will-it-grow", "Will it grow?"),
    ("projects", "Projects"),
    ("guides", "Guides"),
    ("uses", "Uses"),
    ("lawn", "Moss & lawns"),
    ("faq", "FAQ"),
]


def nav_html(active):
    items = []
    for slug, label in NAV:
        href = "index.html" if slug == "index" else f"{slug}.html"
        cls = ' class="active"' if slug == active else ""
        items.append(f'<li><a href="{href}"{cls}>{html.escape(label)}</a></li>')
    return "\n        ".join(items)


def page(slug, title, description, body, hero=None, active=None):
    import json as _json
    full_title = title if slug == "index" else f"{title} | {SITE}"
    active = active or slug
    url = BASE + ("/" if slug == "index" else f"/{slug}.html")
    img = f"{BASE}/assets/{hero or 'hero.jpg'}"
    ogtype = "website" if slug == "index" else "article"
    if slug == "index":
        ld = {"@context": "https://schema.org", "@type": "WebSite",
              "name": SITE, "url": BASE + "/", "description": description}
    else:
        ld = {"@context": "https://schema.org", "@type": "Article",
              "headline": title, "description": description, "image": img,
              "datePublished": LAUNCH, "dateModified": date.today().isoformat(),
              "inLanguage": "en-GB", "mainEntityOfPage": url,
              "author": {"@type": "Organization", "name": SITE},
              "publisher": {"@type": "Organization", "name": SITE}}
    ldjson = _json.dumps(ld, ensure_ascii=False).replace("<", "\\u003c")
    meta = f'''<link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta property="og:site_name" content="{SITE}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img}">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(full_title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{img}">
  <script type="application/ld+json">{ldjson}</script>'''
    if hero:
        hero_block = f'''
  <header class="hero hero--page" style="background-image:linear-gradient(rgba(20,32,18,.55),rgba(20,32,18,.7)),url('assets/{hero}')">
    <div class="wrap">
      <h1>{html.escape(title)}</h1>
    </div>
  </header>'''
    elif slug == "index":
        hero_block = ""  # index renders its own h1 in the hero-home section
    else:
        hero_block = f'''
  <header class="page-head">
    <div class="wrap"><h1>{html.escape(title)}</h1></div>
  </header>'''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  {meta}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"></noscript>
  {ANALYTICS}
</head>
<body>
  <nav class="nav nav--bar">
    <div class="wrap nav-inner">
      <a class="brand" href="index.html">Mossbank</a>
      <input type="checkbox" id="navtoggle" class="navtoggle">
      <label for="navtoggle" class="navburger" aria-label="Menu">≡</label>
      <ul>
        {nav_html(active)}
      </ul>
    </div>
  </nav>
{hero_block}
  <main>
{body}
  </main>
  <footer class="footer">
    <div class="wrap">
      <p class="foot-brand">Mossbank</p>
      <p>A small independent field guide to the bryophytes, for the curious, the gardener and the quietly obsessed.</p>
      <p class="foot-links">
        <a href="biology.html">What is moss</a> ·
        <a href="species.html">Species</a> ·
        <a href="growing.html">Growing</a> ·
        <a href="projects.html">Projects</a> ·
        <a href="uses.html">Uses</a> ·
        <a href="lawn.html">Moss &amp; lawns</a> ·
        <a href="faq.html">FAQ</a> ·
        <a href="privacy.html">Privacy</a> ·
        <a href="about.html">About</a>
      </p>
      <p class="credits">Photographs are from Wikimedia Commons, used under their respective licences and served from this site. Full <a href="credits.html">image credits</a>.</p>
      <p class="copy">&copy; <span>{YEAR}</span> Mossbank. Text licensed CC BY-NC-SA 4.0. Analytics are cookieless and self-hosted; see the <a href="privacy.html">privacy page</a>.</p>
    </div>
  </footer>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# Page content. British English; written to be genuinely useful.
# ---------------------------------------------------------------------------

PAGES = {}

PAGES["index"] = dict(
    title="The quiet green that carpets the world",
    description="Mossbank is an independent field guide to the mosses: what they are, the common species, how to grow them, the projects they suit and the many ways they have been used.",
    body='''
  <section class="hero hero--home">
    <div class="wrap hero-inner">
      <p class="eyebrow">A field guide to the bryophytes</p>
      <h1>The quiet green that carpets the world</h1>
      <p class="lede">Mosses are among the oldest land plants alive. They have no roots, no flowers and no real plumbing, yet they thrive on rock, bark, brick and bare soil where almost nothing else will. Mossbank is a small, independent guide to knowing them, growing them and putting them to use.</p>
      <p><a class="cta" href="biology.html">Start with the basics</a> <a class="cta cta--ghost" href="species.html">Meet the species</a></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="grid-cards">
        <a class="tile" href="biology.html"><h3>What is moss</h3><p>The biology, the strange life cycle, and why a plant with no roots can live on a roof tile.</p></a>
        <a class="tile" href="species.html"><h3>Common species</h3><p>The mosses you will actually meet in temperate gardens, woods and walls, with photographs.</p></a>
        <a class="tile" href="growing.html"><h3>Growing moss</h3><p>Shade, damp and patience. How to start a moss lawn, a wall or a pot, and keep it alive.</p></a>
        <a class="tile" href="projects.html"><h3>Projects</h3><p>Kokedama, terrariums, bonsai carpets, living walls and the slurry method.</p></a>
        <a class="tile" href="uses.html"><h3>Uses</h3><p>From peat bogs and carbon to wound dressings and pollution monitoring.</p></a>
        <a class="tile" href="lawn.html"><h3>Moss &amp; lawns</h3><p>Friend or weed? Why moss appears in turf, and how to either banish it or lean in.</p></a>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap two-col">
      <div>
        <h2>Why bother with moss</h2>
        <p>Moss asks for almost nothing. It needs no mowing, no feeding and no digging. It greens up in winter when everything else has gone over, holds water like a sponge, and softens hard edges of stone and concrete in a way no other plant manages.</p>
        <p>It is also a quiet ally in a warming, drying climate. A moss surface stays cooler than bare soil, slows run-off after heavy rain, and provides cover for the small invertebrates that the rest of the garden depends on. Once you start noticing moss you find it everywhere, and the noticing is half the pleasure.</p>
      </div>
      <aside class="facts">
        <h3>Moss, in brief</h3>
        <dl>
          <dt>Group</dt><dd>Bryophyta, the true mosses</dd>
          <dt>Species</dt><dd>around 12,000 worldwide</dd>
          <dt>Age</dt><dd>fossils back some 450 million years</dd>
          <dt>Roots</dt><dd>none; anchored by fine rhizoids</dd>
          <dt>Likes</dt><dd>shade, damp, still air, poor soil</dd>
        </dl>
      </aside>
    </div>
  </section>
''',
)

PAGES["biology"] = dict(
    title="What a moss actually is",
    description="The biology of mosses: non-vascular bryophytes, the gametophyte and sporophyte life cycle, rhizoids, and the drying-out trick called poikilohydry.",
    hero="hero.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Mosses belong to the bryophytes, a group of small, non-vascular land plants that also includes the liverworts and hornworts. Understanding a few basics about how they are built explains almost everything about where they grow and how to look after them.</p>

      <h2>No vessels, no roots</h2>
      <p>Unlike the familiar garden plants, a moss has no internal plumbing. There are no vessels to pump water and dissolved nutrients from a root system up to the leaves. Instead each leaf, often only a single cell thick, takes up moisture directly from rain, mist and dew across its whole surface. What looks like a root is a mass of fine threads called rhizoids, and their job is to anchor the plant, not to feed it.</p>
      <p>This is why moss is happiest on surfaces that a conventional plant would find impossible: the shaded face of a boulder, a north-facing wall, the mortar between paving stones, the bark of an old tree. It is not drawing anything from those surfaces. It only needs something to hold onto, plus shade and the occasional wetting.</p>

      <h2>The drying-out trick</h2>
      <p>The cleverest thing a moss does is survive drought by switching itself off. When the air dries, the plant dries with it, shrivelling to a crisp brown mat that looks dead. It is not. Within minutes of the next shower it rehydrates, greens up and resumes photosynthesis as though nothing happened. Botanists call this poikilohydry, the ability to let internal water content track the surroundings rather than defend a fixed level.</p>
      <p>For the gardener the lesson is simple. Brown moss is usually thirsty, not dead. A misting will tell you which.</p>

      <h2>Two plants in one life cycle</h2>
      <p>A moss lives in two stages that look quite different. The soft green cushion or carpet you recognise is the gametophyte, the long-lived stage. After fertilisation, which needs a film of water for the sperm to swim through, the gametophyte raises slender stalks tipped with capsules. These stalks and capsules are the sporophyte, the second stage, and they exist mainly to make and scatter spores.</p>
      <p>When a capsule ripens it dries, opens, and releases dust-fine spores to the wind. A spore that lands somewhere damp and shaded germinates into a fine green thread, the protonema, which in turn buds into a new cushion. The cycle begins again. Moss also spreads the lazy way, simply by fragments: a broken-off piece that lands somewhere suitable regrows into a whole new plant, which is the trick gardeners exploit when they propagate it.</p>

      <h2>The two growth forms</h2>
      <p>Look at a few mosses and they sort into two camps, a split worth knowing because it decides how a moss behaves. Some grow upright in tufts and tight cushions, staying compact and slow-spreading; these are the acrocarpous mosses, the bun-like domes on a wall top. Others creep and branch sideways into flat, spreading carpets and wefts; these are the pleurocarpous mosses, the feathery mats over logs and soil. Cushion-formers give shape and texture, carpet-formers give fast continuous cover, and knowing which you are looking at is about the most useful thing you can know about them. It has its own guide in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>Where mosses grow</h2>
      <p>Because a moss feeds from the air and only needs something to cling to, it grows where rooted plants cannot: bare rock, tree bark, brick and mortar, roof tiles, the compacted ground under trees, the splash zone by streams. What it cannot abide is the combination of strong sun and dry wind, which strips its moisture faster than it can take it up, so you find it on the cool, shaded, damp side of things. That same independence is why moss is one of the first life to colonise bare ground after disturbance, slowly building the conditions other plants then move into.</p>

      <h2>An ancient and successful design</h2>
      <p>Mosses are among the oldest land plants, with a lineage going back something like 450 million years, long before flowers, before dinosaurs, close to the time plants first left the water at all. That they are still here, in their thousands of species, on every continent including Antarctica, says how well the simple, rootless, dry-out-and-wait design works. A moss is not a primitive failure that never invented roots; it is a different and very durable answer to the problem of living on land.</p>

      <h2>How to tell a moss from a lookalike</h2>
      <p>Three plants are often mistaken for moss. Liverworts are flat and ribbon-like or have rounded lobes, and lie closer to the surface. Lichens are not plants at all but a partnership of fungus and alga, usually crusty, leafy or shrubby and often grey or yellow. Clubmosses and spikemosses look mossy but are larger, with tougher stems, and belong to an entirely different, vascular group. A true moss has the soft, leafy-stemmed, cushion-or-carpet form, and very often those fine stalked capsules standing above it.</p>

      <p class="next"><a href="species.html">Next: the species you are likely to meet &rarr;</a></p>
    </div>
  </section>
''',
)

PAGES["species"] = dict(
    title="Species you are likely to meet",
    description="A photographic guide to common temperate mosses: Sphagnum, Hypnum cupressiforme, Dicranum scoparium, Thuidium tamariscinum and more, with how to recognise each.",
    body='''
  <section class="section">
    <div class="wrap">
      <p class="lede">There are thousands of moss species, but a small handful turn up again and again in temperate gardens, woods and walls. Learn these first; they train your eye for the rest.</p>
      <div class="cards cards--species">
        <article class="card">
          <img src="assets/sphagnum.jpg" alt="A dense red-green cushion of Sphagnum capillifolium bog moss">
          <div class="card-body">
            <h3>Bog moss <span>Sphagnum capillifolium</span></h3>
            <p>The peat-builders. Sphagnum holds many times its own weight in water and slowly lays down the peat of moors and mires. Acid-loving, spongy, and often flushed red. If you keep carnivorous plants you already know it.</p>
          </div>
        </article>
        <article class="card">
          <img src="assets/hypnum.jpg" alt="Feathery mat of Hypnum cupressiforme">
          <div class="card-body">
            <h3>Cypress-leaved plait moss <span>Hypnum cupressiforme</span></h3>
            <p>Possibly the most common moss in the temperate world. A flat, glossy, trailing mat on tree trunks, fence posts, roofs and rocks. Tolerant of almost anything, which is why it is everywhere.</p>
          </div>
        </article>
        <article class="card">
          <img src="assets/dicranum.jpg" alt="Swept tufts of Dicranum scoparium">
          <div class="card-body">
            <h3>Broom fork-moss <span>Dicranum scoparium</span></h3>
            <p>Its leaves all sweep to one side as if combed by the wind, forming deep, springy cushions on woodland floors and acid banks. A favourite for terrariums because the look is so distinctive.</p>
          </div>
        </article>
        <article class="card">
          <img src="assets/thuidium.jpg" alt="Fern-like fronds of Thuidium tamariscinum">
          <div class="card-body">
            <h3>Tamarisk moss <span>Thuidium tamariscinum</span></h3>
            <p>Three-times-branched fronds give it the look of a tiny fern. A handsome, sprawling moss of damp, shaded woodland and stream banks, and a fine choice for a shaded patch of ground.</p>
          </div>
        </article>
      </div>

      <div class="prose">
        <h2>A few more worth knowing</h2>
        <ul class="loose">
          <li><strong>Wall screw-moss (<em>Tortula muralis</em>)</strong>: the little grey-green cushions on top of nearly every garden wall, with fine hair-points that give a hoary look when dry.</li>
          <li><strong>Silvery thread-moss (<em>Bryum argenteum</em>)</strong>: the silver-green moss that grows in pavement cracks and at the foot of walls, tolerant of pollution and trampling.</li>
          <li><strong>Common haircap (<em>Polytrichum commune</em>)</strong>: one of the tallest mosses, almost like a forest of tiny conifers, on damp acid ground and heath.</li>
          <li><strong>Springy turf-moss (<em>Rhytidiadelphus squarrosus</em>)</strong>: the coarse, star-shooted moss most people are trying to remove when they complain of moss in the lawn.</li>
          <li><strong>Common feather-moss (<em>Kindbergia praelonga</em>)</strong>: fine, much-branched carpets over soil, logs and the base of walls in shade.</li>
        </ul>
        <p>Identifying mosses to species often needs a hand lens and patience with leaf shape and capsule detail. Do not let that put you off. Knowing a moss as "a plait moss" or "a haircap" is plenty to start gardening with, and the names come with familiarity.</p>

        <h2>What surface tells you what to expect</h2>
        <p>Once your eye is in, the surface a moss is growing on is a strong clue to which it is. The tops of walls and the mortar between bricks tend to host tight grey-green cushions like wall screw-moss, hardy things that cope with sun and drying. Tree bark and fence posts carry the flat, trailing mats of plait moss and its relatives. Shaded woodland soil and acid banks grow the deep cushions of broom fork-moss and the fern-like fronds of tamarisk moss. Pavement cracks and trampled ground in towns belong to the tough silvery thread-moss. Knowing the typical residents of each surface means you are half way to a name before you have even reached for the lens.</p>

        <h2>Cushions or carpets</h2>
        <p>Beyond individual names, every moss here falls into one of two groups that decide how it behaves. The cushion-formers, the acrocarpous mosses such as the screw-mosses and haircaps, grow as upright domes and stay compact. The carpet-formers, the pleurocarpous mosses such as the plait and feather mosses, creep and branch into spreading mats. It is the most useful single distinction in the whole subject, because it tells you at a glance whether a moss will sit as a neat cushion or knit into continuous cover. It has its own guide in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

        <h2>A note on the names</h2>
        <p>Mosses carry both Latin names and, increasingly, English ones, and the English names are often charmingly descriptive once you know the plant: plait moss for the braided look of its shoots, fork-moss for its divided leaf tips, feather-moss for its frond-like branching. You do not need the Latin to garden with moss, but it is worth noting because the same English name is sometimes used loosely for several species, so when buying or recording it the Latin name is what pins down exactly which moss you mean.</p>

        <p class="next"><a href="growing.html">Next: growing moss on purpose &rarr;</a></p>
      </div>
    </div>
  </section>
''',
)

PAGES["growing"] = dict(
    title="Growing moss on purpose",
    description="A practical guide to growing moss: choosing a shaded damp site, reducing competition, transplanting, the buttermilk slurry method, watering and troubleshooting.",
    hero="hero.jpg",
    body='''
  <section class="section">
    <div class="wrap two-col">
      <div class="prose">
        <p class="lede">Moss asks for the opposite of most gardening: poor soil, shade, damp and patience. Give it those and it will largely look after itself. Here is how to start.</p>

        <h2>1. Pick the right spot</h2>
        <p>Shade and moisture are everything. North-facing walls and beds, the foot of trees, shaded paving and damp stone all suit moss. Strong sun and dry wind are the enemies; a spot that bakes by midday will defeat you whatever you do. If the surface stays cool and a little damp for most of the day, you are in business.</p>

        <h2>2. Lower the competition</h2>
        <p>Moss is a poor competitor against grass and weeds, so it wins where they struggle. Clear off existing growth, then firm the surface and, on most soils, nudge it towards acid. Bare, compacted, slightly acidic ground suits moss far better than the rich, fluffy loam we lavish on everything else. Do not add compost or feed.</p>

        <h2>3. Transplant, or make a slurry</h2>
        <p>The direct way is to lift fresh patches of moss and press them firmly onto the prepared surface, peat side down, with good contact all over. Keep pieces small and butt them together; they knit in time.</p>
        <p>The other way is the slurry, or "moss milkshake". Blend a couple of handfuls of clean moss with enough buttermilk, natural yoghurt or plain water to make a thin paint, then brush or pour it onto stone, brick, pots or shaded soil. The moss fragments regenerate where they land. It looks unpromising for a few weeks, then greens up.</p>

        <h2>4. Keep it moist while it takes</h2>
        <p>For the first three or four weeks, mist daily, ideally in the morning or evening rather than the heat of the day. This is the make-or-break stage while the rhizoids grip. After that, in a properly shaded spot, rainfall and shade usually carry it.</p>

        <h2>5. Then leave it alone</h2>
        <p>No feeding, no digging, no mowing. In autumn, sweep or gently blow off heavy leaf litter so the moss is not smothered over winter. That is the whole maintenance regime. The cushion thickens year on year.</p>
      </div>
      <aside class="facts">
        <h3>Troubleshooting</h3>
        <dl>
          <dt>Turning brown</dt><dd>too dry or too sunny; add shade and water and wait</dd>
          <dt>Not spreading</dt><dd>soil too rich or too alkaline, or poor contact; firm it down</dd>
          <dt>Lifting at the edges</dt><dd>rhizoids have not gripped; press down and keep misting</dd>
          <dt>Slimy or algal</dt><dd>too wet with too little air; improve drainage and airflow</dd>
          <dt>Birds pulling it up</dt><dd>common in spring; pin patches with a little wire mesh until rooted</dd>
        </dl>
        <h3 class="mt">Water sense</h3>
        <p>Rainwater is kinder than hard tap water, which is alkaline and leaves limescale that moss dislikes. If you can water from a butt, do.</p>
      </aside>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap prose">
      <h2>Choosing the right moss to start with</h2>
      <p>Match the moss to the job. For fast, continuous cover over ground or a wall, use the creeping carpet-formers, the pleurocarpous mosses such as the plait and feather mosses, which knit together quickly and fragment readily for slurry. For cushiony texture in a terrarium or a moss garden, use the upright acrocarpous mosses such as bun moss and the fork-mosses, which hold a domed shape but spread slowly. The easiest moss to start with is whatever already grows happily in your own garden, because it is proven to suit your conditions; lift a little and propagate from that rather than importing something that may sulk. See <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a> for the distinction.</p>

      <h2>Growing on different surfaces</h2>
      <p>The method shifts a little with the surface. On <strong>soil</strong>, clear competition, firm it hard and press moss into good contact. On <strong>stone, brick and concrete</strong>, the slurry method works best, painting blended moss onto the porous surface in shade. In <strong>pots and on bonsai</strong>, a thin pressed layer keeps the surface cool and finished; see <a href="bonsai-moss.html">moss for bonsai</a>. On a <strong>wall or vertical panel</strong>, you need a moisture-holding backing and patience, as in <a href="moss-walls.html">living moss walls</a>. The constants across all of them are shade, damp and firm contact; the rest is detail.</p>

      <h2>The slurry method in more detail</h2>
      <p>The slurry, or "moss milkshake", is the workhorse for covering an area or an awkward shape. Blend two or three handfuls of clean moss with enough liquid to make a thin, brushable paint. The classic binder is buttermilk or natural yoghurt, which helps it cling and feeds the moss a little, though plain rainwater works and avoids the faint smell while it establishes. Brush or pour it where you want growth, keep the fragments coarse rather than pureed so more of them survive, and mist daily. It looks unpromising for a few weeks, then greens up as the fragments regenerate. For a whole wall, the same mix can be sprayed, as in <a href="spraying-moss.html">spraying moss slurry at scale</a>.</p>

      <h2>The common mistakes</h2>
      <p>Three errors account for most failures. The first is choosing too sunny or dry a spot, which no amount of care overcomes; shade and moisture are not optional. The second is enriching the ground, since compost and feed help the competition, not the moss, which wants poor, firm, slightly acidic ground. The third is giving up too soon: moss is slow, and a patch that browns in a dry spell is almost always dormant rather than dead, so water it and wait rather than digging it out. Get the spot right and resist fussing, and moss is one of the most self-sufficient things you can grow.</p>
    </div>
  </section>
''',
)

PAGES["projects"] = dict(
    title="Things to make with moss",
    description="Moss projects for the garden and home: kokedama moss balls, terrariums, bonsai carpets, living moss walls, Japanese moss gardens and the moss graffiti slurry.",
    body='''
  <section class="section">
    <div class="wrap">
      <p class="lede">Once you can keep moss alive, it becomes a material. Six things people make with it, each with its own guide.</p>
      <div class="grid-cards">
        <a class="tile" href="kokedama.html">
          <h3>Kokedama</h3>
          <p>The Japanese "moss ball": a plant whose roots are wrapped in soil, bound with moss and string, and hung or set on a dish. A forgiving first project.</p>
        </a>
        <a class="tile" href="terrariums.html">
          <h3>Terrariums</h3>
          <p>A closed glass jar is a near-perfect moss home: high humidity, soft light, no drying wind. Cushion mosses keep their shape under glass for years.</p>
        </a>
        <a class="tile" href="bonsai-moss.html">
          <h3>Bonsai carpets</h3>
          <p>A skin of moss over a bonsai's soil keeps roots cool and damp, stops the surface washing out, and finishes the tree with a settled, aged look.</p>
        </a>
        <a class="tile" href="moss-walls.html">
          <h3>Living walls</h3>
          <p>Moss panels green a shaded wall with almost no weight and no irrigation once established, soaking up rain and cooling the surface.</p>
        </a>
        <a class="tile" href="japanese-moss-gardens.html">
          <h3>Japanese moss gardens</h3>
          <p>The moss gardens of Kyoto treat the carpet itself as the planting, with stone, water and a few trees for structure. Quiet, and deep.</p>
        </a>
        <a class="tile" href="moss-graffiti.html">
          <h3>Moss graffiti</h3>
          <p>Paint a moss slurry onto a shaded wall in a shape or letters, keep it misted, and it grows into a living design.</p>
        </a>
      </div>
      <div class="prose">
        <p class="next"><a href="growing.html">You will need the basics first: the growing guide &rarr;</a></p>
      </div>
    </div>
  </section>
''',
)

PAGES["uses"] = dict(
    title="What moss is good for",
    description="The uses of moss: peat and carbon storage, water and flood regulation, insulation and packing, wartime wound dressings, pollution monitoring and green roofs.",
    hero="hero.jpg",
    body='''
  <section class="section">
    <div class="wrap">
      <p class="lede">Moss is easy to overlook and has been quietly useful for a very long time. A tour of what it does, in the wild and in our hands.</p>
      <div class="uses-grid">
        <div class="use">
          <h3>Peat and carbon</h3>
          <p>Sphagnum mosses build peat, and peatlands store more carbon per hectare than forest. Healthy bogs are one of the most effective carbon stores on land, which is why draining and digging them is so costly, and restoring them so valuable.</p>
        </div>
        <div class="use">
          <h3>Water and floods</h3>
          <p>A moss layer holds huge amounts of water and releases it slowly. On hillsides and in bogs this slows run-off, steadies streams and reduces the spikes that cause flooding downstream.</p>
        </div>
        <div class="use">
          <h3>Insulation and packing</h3>
          <p>Dried moss has chinked log cabins, stuffed mattresses and packed shipped plants and bulbs for centuries. It is light, springy, holds moisture and is mildly antiseptic.</p>
        </div>
        <div class="use">
          <h3>Wound dressings</h3>
          <p>Sphagnum is absorbent and slightly acidic, which discourages bacteria. It was gathered by the sackful to dress wounds in the First World War when cotton ran short, and it genuinely saved lives.</p>
        </div>
        <div class="use">
          <h3>Pollution monitoring</h3>
          <p>Because mosses feed straight from air and rain, they accumulate whatever is in them. Scientists use moss samples to map heavy metals, nitrogen and other airborne pollutants cheaply and over wide areas.</p>
        </div>
        <div class="use">
          <h3>Green roofs and walls</h3>
          <p>Light, drought-hardy once established and needing none of the upkeep of sedum or grass, moss carpets cool buildings, hold rainwater and add habitat, all for very little structural load.</p>
        </div>
        <div class="use">
          <h3>Gardens and bonsai</h3>
          <p>As a living mulch, moss keeps roots cool and damp, suppresses weeds and finishes a planting. It is the quiet groundwork under a great deal of fine container growing.</p>
        </div>
        <div class="use">
          <h3>Habitat</h3>
          <p>A moss carpet is a small world: a humid refuge for springtails, mites, tardigrades and the creatures that eat them, and nesting material for birds. Lose the moss and you lose that layer of life.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap prose">
      <h2>The long view: peat and climate</h2>
      <p>The grandest thing moss does happens over thousands of years and out of sight. In waterlogged bogs, sphagnum grows at the surface while its older growth beneath fails to rot in the airless, acidic conditions, and that half-preserved material piles up as peat. The result is one of the planet's great carbon stores, holding more per hectare than woodland, alongside an enormous capacity to soak up and slowly release water. Drain a bog or cut it for fuel and that carbon escapes to the air; keep it wet and it goes on quietly banking the stuff. Much of the modern argument for peat-free compost rests on this, and there is a fuller account in <a href="peat-and-peat-free.html">sphagnum, peat and why peat-free matters</a>.</p>

      <h2>A history of practical use</h2>
      <p>People worked out the useful properties of moss long before they understood the biology. Its springiness and water-holding made it a packing material for everything from shipped bulbs to crockery, and a stuffing for mattresses and pillows. Dried and rammed between logs, it sealed cabins against the weather. The most striking use was medical: sphagnum's acidity and absorbency make it hostile to bacteria, and when surgical cotton ran short in the First World War, volunteers gathered bog moss by the cartload to dress wounds. There is more of this story in <a href="moss-in-history.html">moss through history</a>.</p>

      <h2>Moss in modern hands</h2>
      <p>Today the interest runs in two directions. Scientists read moss as an instrument: because it takes everything from the air and rain, a moss sample records the heavy metals and nitrogen drifting over a place, which makes for cheap, wide-area pollution mapping. Designers, meanwhile, treat it as lightweight green infrastructure, carpeting roofs and walls that could never carry a conventional planting, cooling buildings and catching rainwater for almost no structural load. And in the ordinary garden it remains what it has always been, a living mulch that keeps roots cool, smothers weeds and quietly finishes a planting.</p>
    </div>
  </section>
''',
)

PAGES["lawn"] = dict(
    title="Moss in the lawn: friend or weed?",
    description="Why moss takes over a lawn, what it tells you about shade, drainage and soil, how to remove it if you must, and the case for letting a moss lawn take over.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">More people meet moss as a lawn complaint than in any other way. Before reaching for the iron sulphate, it pays to read what its arrival is telling you about the ground.</p>

      <h2>Why the moss is there</h2>
      <p>Moss colonises turf wherever grass is already losing its grip. Shade, compacted soil, poor drainage, scalping the lawn with a low mower and thin, acidic, hungry ground all weaken grass and happen to be the conditions moss prefers. So the green carpet creeping through the lawn is really a reading of the site. Clear it off and leave those conditions untouched, and it will be back inside a season.</p>

      <h2>Reading the signs</h2>
      <p>Each cause leaves a clue. Worst under trees or along a fence line, and shade is your answer. Worst where the lawn squelches underfoot or sits on heavy clay, and the trouble is drainage and compaction. A thin general invasion across an old, hungry, close-mown lawn points instead to low fertility and cutting too hard. Working out which one you have matters, because some of these yield to effort and others, deep shade above all, simply will not.</p>

      <h2>Getting the grass back</h2>
      <p>Where the cause can be addressed, go for the cause rather than the moss itself. Thin overhead growth to let in light, spike or hollow-tine to relieve compaction, sort out drainage, raise the cutting height, and feed so the grass can muscle back in. Scarifying drags out the loose moss and opens room for grass to thicken, and on a truly acidic lawn a measured dose of lime shifts the balance. Iron-based mosskillers blacken it within days, which feels like progress but lasts only until the same conditions grow it back.</p>

      <h2>Living with a moss lawn</h2>
      <p>The alternative is to stop fighting. In a shaded, damp garden a moss lawn is a real pleasure underfoot, green right through winter and drought, and free of mowing, feeding and watering once it has settled in. Clearing the leaves in autumn is about all it asks. Where grass has never properly taken, this tends to be both the better-looking surface and far the less demanding, and plenty of gardeners now choose it on purpose rather than inheriting it by defeat. There is a full how-to in <a href="moss-lawn.html">how to make a moss lawn</a>.</p>

      <h2>Which moss makes a lawn</h2>
      <p>If you are encouraging it rather than evicting it, lean towards the creeping, carpet-forming kinds over tight cushions, because they spread into continuous, walkable cover. The springy turf-moss already colonising many lawns is one of them; the feather mosses are another. Cushion-formers look marvellous in a moss garden but spread too slowly and lumpily to make a lawn.</p>
    </div>
  </section>
''',
)

PAGES["faq"] = dict(
    title="Frequently asked questions",
    description="Common questions about moss: is it killing my lawn or roof, does it harm trees, is it bad for paving, how to grow it, and whether moss is a weed.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <h2>Is moss killing my lawn?</h2>
      <p>No. Moss colonises ground where grass is already failing, usually through shade, compaction or poor drainage. It is the result, not the cause. See <a href="lawn.html">moss and lawns</a>.</p>

      <h2>Does moss harm my roof?</h2>
      <p>Moss itself does not eat into sound tiles or slates, but thick growth can hold moisture against them and block gutters and valleys, so it is worth clearing from roofs and keeping out of gutters. Brush rather than blast: high-pressure washing damages the surface and shortens a roof's life more than the moss does.</p>

      <h2>Is moss bad for trees?</h2>
      <p>No. Moss on bark is just using the trunk as a surface. It takes nothing from the tree and is a sign of clean, damp air, not of ill health.</p>

      <h2>Is moss damaging my paving and walls?</h2>
      <p>On sound surfaces moss is cosmetic and, on steps, a slip hazard worth managing. It can work into already-failing mortar, so it is a prompt to repoint rather than a cause of the damage. On a stable wall it is simply part of the character.</p>

      <h2>How do I get rid of moss?</h2>
      <p>Decide where first. On paths and roofs, brush it off and improve drainage and light. On lawns, fix the shade, compaction and drainage or it returns. Chemical mosskillers based on iron sulphate blacken and kill it quickly but change nothing underlying.</p>

      <h2>How do I grow moss on purpose?</h2>
      <p>Shade, damp, poor firm soil, and patience, plus either transplanted patches or a blended slurry. The full method is on the <a href="growing.html">growing page</a>.</p>

      <h2>Is moss a weed?</h2>
      <p>Only where you do not want it. The same plant is a nuisance in a bowling green and the entire point of a Kyoto moss garden. It is all a matter of place.</p>

      <h2>Will moss grow indoors?</h2>
      <p>In a closed terrarium, very happily, because the humidity stays high. Out in a dry, centrally heated room it will not last; it needs that damp, still air. The full picture is in <a href="moss-indoors.html">can you keep moss as a houseplant</a>.</p>

      <h2>Is moss a plant?</h2>
      <p>Yes. Moss is a true plant, one of the bryophytes, a group of non-vascular plants that also includes liverworts and hornworts. What makes it unusual is what it lacks: no roots, no flowers, no seeds and no internal plumbing. It is a plant stripped back to fundamentals, which is exactly why it can live where other plants cannot. See <a href="biology.html">what a moss actually is</a>.</p>

      <h2>Does moss flower or have seeds?</h2>
      <p>No to both. Moss reproduces by spores, not seeds, and it has nothing like a flower. Instead it raises slender stalks tipped with capsules that release dust-fine spores to the wind, and it also spreads from broken fragments. The little stalked capsules standing above a moss cushion are the nearest thing it has to "going to seed".</p>

      <h2>How long does moss live?</h2>
      <p>Individual cushions can persist and slowly expand for many years, and a moss colony on an undisturbed bank or wall may be effectively decades old, thickening season on season. Moss also survives drying out by going dormant, so a patch can sit lifeless-looking through a drought and revive years' worth of growth intact when the rain returns.</p>

      <h2>Is moss poisonous, or safe around pets and children?</h2>
      <p>Garden and woodland mosses are not poisonous and are not a meaningful hazard to pets or children, who in any case rarely show interest in eating it. The sensible cautions are the ordinary ones: anything growing outdoors may carry whatever has landed on it, and a wet moss surface on steps or stone is slippery. Preserved decorative moss is treated with glycerine and dye and is for looking at, not handling food with, but it is not toxic to have in the house.</p>

      <h2>Why has my moss gone brown?</h2>
      <p>Almost always because it has dried out. Brown moss is usually dormant rather than dead, and a good soaking will tell you which within a day or two as it greens back up. Persistent browning means the spot is too dry or too sunny for it; add shade and moisture, and water with rainwater rather than hard tap water, which it dislikes. See <a href="watering-moss.html">water for moss</a>.</p>

      <h2>Can I walk on a moss lawn?</h2>
      <p>Gently, yes, once it is well established. Moss does not take the heavy, repeated traffic a grass sports lawn does, but a settled moss lawn handles normal garden use and stepping stones perfectly well, and is soft underfoot. Keep off it while it is young and still gripping. See <a href="moss-lawn.html">how to make a moss lawn</a>.</p>
    </div>
  </section>
''',
)

PAGES["about"] = dict(
    title="About Mossbank",
    description="About Mossbank, a small independent field guide to mosses and the other bryophytes.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Mossbank is a small, independent field guide to the bryophytes, written for anyone who has ever crouched down to look closely at the green stuff on a wall.</p>
      <p>It started, as these things do, with noticing. Once you see one moss properly you start seeing all of them, and it turns out the soft green carpet you walked past for years is a whole quiet kingdom: older than the dinosaurs, living without roots, surviving drought by switching itself off, and holding more of the world together than its size suggests.</p>
      <p>The aim here is plain and practical. What is moss, which ones will you meet, how do you grow it, what is it good for. No jargon for its own sake, and British names alongside the Latin so you can actually use them.</p>
      <p>The photographs are from Wikimedia Commons under their respective licences, credited in the footer. The words are licensed CC BY-NC-SA 4.0, free to share and adapt non-commercially with credit. Corrections and additions are welcome.</p>
      <p class="next"><a href="index.html">&larr; Back to the start</a></p>
    </div>
  </section>
''',
)

PAGES["privacy"] = dict(
    title="Privacy",
    description="Mossbank's privacy approach: cookieless, self-hosted analytics, no tracking cookies, no personal data sold, and a note on future advertising.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">The short version: Mossbank sets no tracking cookies, sells no data, and counts visits with privacy-respecting, self-hosted analytics.</p>

      <h2>Analytics</h2>
      <p>To understand which pages are read, Mossbank uses GoatCounter, a privacy-friendly analytics tool that we host ourselves rather than handing your visit to a third party. It sets no cookies and does not track you across other sites. It records a page view with non-identifying details such as the page address, the referring site, a broad country derived from your network, and the type of browser and screen. It does not store your full IP address. Because nothing identifies you personally and no cookie is set, no consent banner is required.</p>

      <h2>What we do not do</h2>
      <p>We do not set advertising or tracking cookies, build profiles of individuals, or sell or share personal data. There are no third-party social or tracking widgets embedded in these pages.</p>

      <h2>Fonts</h2>
      <p>Pages load a typeface from Google Fonts, which means your browser contacts Google's servers to fetch the font files. If you would rather avoid that, a content blocker will stop it without breaking the site.</p>

      <h2>Advertising</h2>
      <p>Mossbank may in future carry advertising to cover its running costs. If and when it does, this page will be updated to describe exactly what that involves, including any cookies an advertising provider would set and how to opt out, before any such advertising appears.</p>

      <h2>Your rights and contact</h2>
      <p>Since we do not hold information that identifies you, there is nothing personal to access, correct or delete. If anything here changes, this page will say so. Questions about privacy can be raised through the contact details on the <a href="about.html">about page</a>.</p>
    </div>
  </section>
''',
)


PAGES["kokedama"] = dict(
    title="Kokedama: the moss ball",
    description="How to make and care for kokedama, the Japanese moss ball: choosing a plant, mixing the soil, binding with moss and string, watering by soaking, and keeping it alive.",
    active="projects",
    hero="kokedama.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Kokedama, literally "moss ball", is a plant grown with its roots in a ball of soil that is wrapped in living moss and bound with string. No pot, just a green sphere you hang or rest on a dish. It is the friendliest way into growing with moss.</p>

      <h2>What you need</h2>
      <ul class="loose">
        <li>A small shade-tolerant plant: ferns, ivy, peace lily, asparagus fern and many houseplants all take to it.</li>
        <li>A soil mix that holds together: the classic is roughly seven parts akadama (a Japanese clay soil) to three parts peat-free compost, but any heavy, slightly clayey mix that binds when damp will do.</li>
        <li>Sheet moss to wrap the outside.</li>
        <li>Cotton or jute twine, and a bucket of water.</li>
      </ul>

      <h2>Making it</h2>
      <p>Ease the plant from its pot and tease most of the loose compost off the roots. Dampen your soil mix until it holds a shape like modelling clay, and press it around the root ball into a firm sphere. Wrap the moss around the outside, green side out, covering the ball completely, then wind twine around it in every direction until the moss is held snug. Tie off and tidy the loose ends.</p>

      <h2>Watering and care</h2>
      <p>You water a kokedama by soaking, not pouring. When the ball feels light, sit it in a bowl of water (rainwater for preference) for ten to twenty minutes until it stops bubbling and feels heavy again, then let it drain. How often depends on your room, but once or twice a week is typical. Keep it out of direct sun and away from radiators, mist the moss between soakings if your air is dry, and feed the plant occasionally in summer by adding a weak feed to the soak water.</p>

      <h2>Choosing the plant</h2>
      <p>The plant matters more than the wrapping. Pick something that tolerates shade and likes its roots evenly moist, since that is the life a kokedama offers. Ferns are the natural fit, and ivy, pothos, peace lily, asparagus fern, spider plant and many small foliage houseplants all settle in happily. Avoid succulents and cacti, which want to dry right out and will rot in a damp ball, and skip anything that grows into a heavy specimen the wrapping cannot support. A small, slow plant is easier to keep looking right than a vigorous one straining at the moss.</p>

      <h2>When it goes wrong, and how long it lasts</h2>
      <p>Two faults account for most trouble. A ball left to dry hard sheds its moss and stresses the plant, so weigh it in your hand and soak before it gets light. A ball kept sodden, sitting in a saucer of water, rots the roots from the inside; let it drain fully after each soak and never leave it standing. The moss itself wants the humidity and indirect light described above, and will brown on a hot dry windowsill. Looked after, a kokedama lasts a year or two before the plant outgrows the ball, at which point you simply unwrap it, pot it on or split it, and start again with a fresh sphere.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)

PAGES["terrariums"] = dict(
    title="Moss terrariums",
    description="Building a moss terrarium: choosing a closed or open vessel, drainage and substrate layers, which cushion mosses suit glass, planting, and the light and watering they need.",
    active="projects",
    hero="dicranum.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A glass vessel gives moss exactly what it likes and we struggle to provide indoors: high humidity, soft even light and still air. A closed terrarium can keep a moss landscape fresh for years with almost no attention.</p>

      <h2>Open or closed</h2>
      <p>A closed jar or bottle traps moisture and recycles it, so it suits mosses and other damp-lovers and needs watering only rarely. An open bowl dries faster, wants more frequent misting, and suits plants that dislike constant wet. For moss, closed is the easier and more reliable choice.</p>

      <h2>The layers</h2>
      <p>Build from the bottom up: a layer of gravel or clay pebbles for drainage, a thin layer of activated charcoal to keep the water sweet, a mesh or fibre divider if you like, then a few centimetres of substrate. A free-draining, low-nutrient mix is best; rich compost encourages mould under glass.</p>

      <h2>Which mosses</h2>
      <p>Cushion species hold their shape beautifully behind glass. Bun moss and the broom fork-moss keep their domed, combed look for a long time. Carpet-forming feather mosses spread to fill gaps and soften the floor. Avoid bog mosses unless you are running things very wet.</p>

      <h2>Planting and care</h2>
      <p>Press each piece of moss firmly onto the substrate so it makes full contact, then mist lightly. Stand the terrarium in bright, indirect light, never direct sun, which cooks the inside in minutes. A closed jar should show a light mist on the glass; clear it for a while if it streams with water, and add a spray if it dries out. That is more or less the entire job.</p>

      <h2>Hardscape and arrangement</h2>
      <p>A jar of flat moss is pleasant; a little landscaping makes it absorbing. A couple of stones, a knot of driftwood or a piece of cork bark give the eye somewhere to rest and the moss something to climb. Set the taller cushions towards the back and let a carpet run forward to the glass, so there is a sense of depth rather than a flat lawn. Odd numbers of features tend to look more natural than even, and a single bold stone usually beats a scatter of small ones. Tweezers and a long spoon help you place things in a narrow-necked vessel.</p>

      <h2>The long game</h2>
      <p>A sealed moss terrarium is one of the few planted things that genuinely thrives on neglect, since the water cycles round inside it and the moss asks for almost nothing. Months can pass between sprays. The usual reasons one fails are a sunny windowsill, which overheats it, and too much rich soil or buried leaf litter, which feeds mould in the still air. Keep it bright but shaded, keep the substrate lean, pull out anything that starts to fur over, and a good terrarium will hold its looks for years. For diagnosing the wobbles, there is a dedicated <a href="moss-terrarium-troubleshooting.html">troubleshooting guide</a>.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)

PAGES["bonsai-moss"] = dict(
    title="Moss for bonsai",
    description="Using moss on bonsai: why a moss surface helps, choosing a fine flat-growing species, applying it as patches or a slurry, and avoiding the moss harming the tree.",
    active="projects",
    hero="hypnum.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A skin of moss over the soil of a bonsai does real work as well as looking right. It keeps the root zone cool and evenly damp, stops the surface washing out when you water, and gives the planting that settled, long-established look that takes years to fake otherwise.</p>

      <h2>Choose the right moss</h2>
      <p>You want a fine, flat, tight-growing species that hugs the soil, not a tall or shaggy one that competes for the eye with the tree. Low feather mosses and the flat plait mosses are ideal. Collect small amounts from paths, walls and pots rather than stripping a single patch.</p>

      <h2>Applying it</h2>
      <p>The simplest method is to press small pieces of fresh moss firmly onto the dampened soil surface, butting them together with no gaps, then water gently. The slurry method also works well on bonsai: blend moss with a little water or buttermilk and paint it over the soil, where it regenerates over a few weeks.</p>

      <h2>Do not let it work against you</h2>
      <p>Moss holds water, which is the point, but on a tree that likes to dry between waterings it can keep the surface too wet and hide what the soil is doing. Keep an eye on watering, lift a corner now and then to check the soil beneath, and trim the moss back if it starts creeping up the trunk. On the show bench, a neat moss surface is the finishing touch; off-season, give the tree normal airflow.</p>

      <h2>Matching the moss to the tree</h2>
      <p>The moss should sit beneath the tree in scale and in feeling, never compete with it. On a small shohin bonsai a coarse, shaggy moss looks absurd, like long grass round a model; choose the finest, tightest carpet you can find. On a larger, rugged tree a slightly bolder moss reads well. Aim for variation too: a single flawless green sheet can look artificial, whereas a mix of tones and a hint of bare, mossy soil at the edges looks like ground that has simply aged. Many growers keep a tray of spare moss going so there is always a patch to lift from before a show.</p>

      <h2>Through the year</h2>
      <p>Moss on bonsai is best treated as a seasonal dressing rather than a permanent fixture. It looks its part in the cool, damp growing season and for display, but a tree sealed under moss through a wet winter can stay soggy at the worst time. Many keepers lift or thin the moss off-season to let the soil breathe and to watch the surface, then re-dress before the tree goes on show. That rhythm also lets you correct watering habits the moss would otherwise mask.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)

PAGES["moss-walls"] = dict(
    title="Living moss walls",
    description="Making a living moss wall: why moss suits vertical greening, framed panels versus direct growing, the shade and humidity it needs, and the difference from preserved moss.",
    active="projects",
    hero="thuidium.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss is close to the perfect material for greening a wall. It is light, needs no soil to speak of, asks for no feeding, and once established lives on shade, humidity and the occasional misting rather than a pumped irrigation system.</p>

      <h2>Living, not preserved</h2>
      <p>Be clear which you want. Much of what is sold as a "moss wall" is preserved moss: real moss treated so it stays soft and green but is no longer alive, used purely as decoration indoors. A living moss wall is a different thing, a genuine growing surface that needs the right conditions. This guide is about the living kind.</p>

      <h2>What it needs</h2>
      <p>Shade and humidity are everything. A living moss wall wants a spot out of direct sun, ideally north-facing or well shaded, with still, damp air. A bright bathroom, a shaded courtyard or a north wall all suit it; a sunny living room does not. Without enough humidity it browns and you are back to misting daily.</p>

      <h2>Building one</h2>
      <p>The usual approach is a shallow framed panel backed with a moisture-holding medium such as a felt mat or a fine substrate, onto which moss is pressed or grown in. Keep the panel evenly damp while the moss grips, using rainwater if you can. The slurry method works for covering an awkward shape: paint blended moss onto the backing and keep it misted until it knits. Once it has taken, the wall largely looks after itself in the right spot.</p>

      <h2>Indoors, and the humidity question</h2>
      <p>A living wall indoors lives or dies on humidity. Ordinary heated rooms sit too dry for moss to stay green, so an indoor living wall realistically needs either a naturally humid spot, a bright bathroom being the classic, or some help: regular misting, a nearby humidifier, or a sealed glass-fronted frame that holds moisture like a vertical terrarium. A room hovering around the upper half of the humidity range gives moss a fighting chance; a dry lounge does not. If you simply want green on the wall and not a maintenance habit, preserved moss is the practical answer, covered in <a href="preserved-moss-wall.html">preserved moss walls</a>.</p>

      <h2>Watering without a flood</h2>
      <p>The trick with any vertical planting is wetting it evenly without water sheeting straight to the floor. Mist by hand for a small panel, or for a larger one fit a simple drip line along the top and let gravity carry moisture down through the backing. Whatever the method, the backing wants to stay damp like a wrung-out cloth, never running, and a waterproof tray or channel at the base catches the surplus. Rainwater keeps the moss greener and spares the wall the limescale that hard tap water leaves.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)

PAGES["japanese-moss-gardens"] = dict(
    title="Japanese moss gardens",
    description="The Japanese moss garden tradition: the famous Kyoto gardens, why moss became central, the conditions that make a moss garden work, and how to bring the idea home.",
    active="projects",
    hero="hero.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">In the Japanese moss garden the carpet itself is the planting. Where a Western garden fills beds with flowers, these gardens use moss as the ground, with stone, water and a few carefully placed trees for structure. The effect is quiet, even and deep.</p>

      <h2>Kyoto and the moss tradition</h2>
      <p>Kyoto is the home of the form, and Saiho-ji, the temple known simply as Koke-dera or "the moss temple", is its most famous example, its grounds carpeted in well over a hundred kinds of moss. The look was not entirely planned: in a damp, shaded climate, moss spread of its own accord over older gardens, and gardeners came to value rather than fight it. The restraint we admire grew partly out of letting the moss have its way.</p>

      <h2>Why it works there</h2>
      <p>Kyoto's humid summers and shaded temple grounds are close to ideal for moss. That is the real lesson for anyone wanting the effect elsewhere: a moss garden is not a style you impose but a response to a place. Give moss the shade and damp it needs and it thrives; deny them and no amount of design will hold it.</p>

      <h2>Bringing the idea home</h2>
      <p>You do not need a temple. A shaded, damp corner, a few good stones, a simple path and patience will carry the feeling. Prepare the ground as in the <a href="growing.html">growing guide</a>, keep grass and weeds out, clear fallen leaves in autumn, and let the moss thicken year on year. The discipline is mostly in what you leave out.</p>

      <h2>The idea behind it</h2>
      <p>These gardens are not merely lawns of moss; the restraint carries meaning. The even green surface is meant to calm the eye and suggest age, stillness and the slow passage of time, qualities tied to the Zen Buddhist temples where many of the famous examples grew. Moss reads as something that has always been there, that arrived on its own and was allowed to stay, and that quietness is the whole point. Understanding that helps when you plan your own: the aim is not to fill the space but to compose a few elements and let the moss hold them together.</p>

      <h2>Stone, water and the planting around it</h2>
      <p>In the traditional palette the moss is the ground and a handful of other elements sit within it: weathered rocks placed as if they grew there, a stone lantern or basin, raked gravel or a small pool, and a few trees, often maples and pines, for shade and seasonal change. A maple over moss is a particularly happy pairing, the autumn colour set against the steady green. Keep the planting sparse and the maintenance gentle, sweeping debris and trimming back anything that threatens to shade the moss into decline, and the composition deepens rather than fades as the years pass.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)

PAGES["moss-graffiti"] = dict(
    title="Moss graffiti",
    description="How to make moss graffiti: blending a moss slurry, painting a design onto a shaded wall, keeping it misted until it takes, and the etiquette of where to do it.",
    active="projects",
    hero="hypnum.jpg",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss graffiti is a living design: a shape, word or pattern painted onto a wall as a moss slurry, which then grows into the real thing. Done in the right spot it is one of the most satisfying things you can do with moss.</p>

      <h2>The slurry</h2>
      <p>Blend a couple of handfuls of clean moss with enough liquid to make a thick paint. The traditional binder is buttermilk or natural yoghurt, which helps it cling and feeds the moss a little; plain water works too. Some people add a spoonful of sugar or a little water-retaining gel. You want a mix you can apply with a brush without it running off.</p>

      <h2>Applying it</h2>
      <p>Pick a shaded, damp, porous surface: rough brick, stone or bare concrete in shade takes moss far better than a smooth, sunny, painted wall. Paint your design on with a brush, keep the edges crisp, and then comes the only hard part, which is keeping it damp. Mist it daily for the first few weeks while the moss establishes. In a genuinely shaded, humid spot it greens up and fills in; in sun it simply dries and fails.</p>

      <h2>Where, and whose wall</h2>
      <p>This is lovely on your own damp north wall, a shaded fence or a back yard. On anyone else's property it is criminal damage however green and gentle it looks, so ask first, and do not do it on listed or historic stonework where even moss can be unwelcome. Your wall, your rules; someone else's wall, their permission.</p>

      <h2>Designing the lettering</h2>
      <p>Moss spreads and softens as it grows, so fine detail blurs. Keep shapes bold and strokes thick, the way a stencil or a chunky display typeface reads, rather than attempting thin script that will smudge into an illegible green smear within weeks. A simple word, a number or a clean graphic holds up far better than anything fiddly. It helps to chalk the outline on the wall first, or cut a card stencil and paint the slurry through it, which keeps edges crisp while the moss is establishing.</p>

      <h2>Why it often fails, and how to improve the odds</h2>
      <p>Most disappointments come down to the wall and the watering. A sunny, smooth or painted surface will not hold moss however good the slurry, whereas rough, porous masonry in steady shade gives it a real chance. The other half is moisture: the design needs to stay damp for weeks while the fragments root, and a spell of neglect in dry weather undoes the lot. People who get good results either pick a wall that stays naturally damp or rig a way to keep it misted, and they accept that the design takes a month or two to come through rather than appearing overnight.</p>

      <p class="next"><a href="projects.html">&larr; Back to projects</a></p>
    </div>
  </section>
''',
)


PAGES["preserved-moss-wall"] = dict(
    title="Preserved moss walls",
    description="Preserved moss walls explained: what preserved moss is, why it suits offices with no light or watering, the ideal humidity, how to build one, and how it differs from a living wall.",
    active="guides",
    blurb="The no-watering, no-light green wall most offices actually have. What preserved moss is, and how to build one.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Most of the lush green moss walls you see in offices and reception areas are not alive. They are made from preserved moss: real moss whose sap has been replaced with a glycerine solution so it stays soft, green and supple indefinitely, without light, soil or water. For an indoor wall this is usually the right answer.</p>

      <h2>Why preserved suits an office</h2>
      <p>A preserved wall needs no light, no irrigation, no misting and no feeding. It does not grow, so it never outgrows its frame or drops debris. The only things it dislikes are direct sun, which fades it, the dry blast of an air-conditioning vent, and standing damp. Humidity in the region of 40 to 60 per cent keeps it at its best: below about 40 it can turn brittle, and much above 60 to 70 it may slowly reabsorb moisture and spoil. An office sitting at 55 to 60 per cent is squarely in the happy range.</p>

      <h2>The kinds of preserved moss</h2>
      <ul class="loose">
        <li><strong>Reindeer moss</strong> (actually a lichen): the springy, bobbly texture used for most flat panels.</li>
        <li><strong>Flat or sheet moss</strong>: a smooth, carpet-like green for clean modern panels.</li>
        <li><strong>Bun or ball moss</strong>: rounded cushions that give a rolling, hummocky surface.</li>
        <li><strong>Mood moss</strong>: larger clumps for a wilder, more three-dimensional look.</li>
      </ul>
      <p>Most walls mix two or three for depth.</p>

      <h2>Building one</h2>
      <p>Preserved moss is simply glued to a backing board. Cut a board to size, lay out your moss to plan the texture and colour, then fix each piece down with a hot-melt glue gun or a strong craft adhesive, packing the pieces tight so no backing shows at the edges. Mount the finished panel like a picture. There is no blending, no slurry and no yoghurt; those are living-moss techniques and have no place here.</p>

      <h2>If you want it living instead</h2>
      <p>At 55 to 60 per cent humidity a living wall is borderline rather than impossible. It would need a genuinely shaded position out of direct sun, a small grow light, regular misting, and hardy cushion or sheet mosses rather than bog moss. That is a real ongoing project. If you want green on the wall and your time back, preserved is the sane choice; the <a href="moss-walls.html">living moss walls</a> guide covers the other path.</p>

      <h2>How long it lasts</h2>
      <p>A preserved wall holds its look for years rather than months, often quoted at five to ten years indoors before the colour dulls and it wants refreshing. What shortens that is mistreatment rather than age: direct sunlight bleaches the green, dry air near a vent or radiator makes it brittle and shed, and damp lets it spoil. Keep it out of those three and it ages gracefully. There is no watering, no feeding and no pruning in between; an occasional gentle dusting with a soft brush or a puff of air is the entire maintenance routine.</p>

      <h2>Cost, and making your own</h2>
      <p>Bought ready-made, preserved panels are priced as decor and add up quickly for a large area. Making your own is far cheaper and not difficult: preserved moss is sold loose by weight, and you simply glue it to a board as described above, which also lets you mix textures and shapes to taste. Buying the moss loose and building the panel yourself typically costs a fraction of a finished commission, and a weekend of gluing covers a sizeable wall. It is a satisfying job, and forgiving, since gaps are easily filled and the eye reads the overall texture rather than any single piece.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["removing-moss"] = dict(
    title="How to get rid of moss",
    description="Removing moss from lawns, roofs, patios, paths and decking: why it appears, how to clear it without damage, and how to stop it coming straight back.",
    active="guides",
    blurb="Lawns, roofs, patios, paths and decking: how to clear moss without wrecking the surface, and stop it returning.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss appears where conditions favour it over whatever you would rather have: shade, damp, poor drainage and compaction. You can scrape it off, but unless you change those conditions it returns. Here is how to clear each surface and, more importantly, keep it gone.</p>

      <h2>Lawns</h2>
      <p>Rake or scarify out the dead and living moss, then treat the cause: relieve compaction by spiking or aerating, improve drainage, cut less hard, reduce shade where you can, and feed the grass so it competes. A lawn sand or iron-sulphate treatment blackens moss quickly but changes nothing underlying. The full picture is on the <a href="lawn.html">moss and lawns</a> page.</p>

      <h2>Roofs and gutters</h2>
      <p>Brush moss off dry, working downwards so you do not lift tiles, and clear it out of gutters and valleys where it traps water. Do not pressure-wash: the force strips the protective surface off tiles and slates and shortens the roof's life far more than the moss would. Improving light and airflow, and fitting zinc or copper strips near the ridge, slows regrowth.</p>

      <h2>Patios, paths and decking</h2>
      <p>For paving and stone, a stiff brush and a bucket of hot water shift most of it; a patio cleaner or a weak solution does the rest. On decking, scrub along the grain and rinse. Keep these surfaces clear afterwards by improving drainage and cutting back overhanging growth so they dry out between downpours. On steps, treat moss as a slip hazard and stay on top of it.</p>

      <h2>Chemical mosskillers, and when to skip them</h2>
      <p>The common chemical treatments are based on ferrous sulphate (iron), the active part of most lawn sands and path mosskillers. They work fast, blackening moss within a day or two, and on a lawn they have the side benefit of greening the grass. The catch is that they kill the existing moss without touching the reasons it grew, so on a shaded, damp surface you are signing up to repeat the dose every season. They also stain paving and concrete with rust marks, so on a patio or path a brush and hot water are usually the better tool. Bleach and harsh cleaners shift moss too but harm surrounding plants and soil life, and are best avoided outdoors.</p>

      <h2>Prevention that actually holds</h2>
      <p>Clearing moss is the easy half; keeping it gone is the half that lasts. Everything that helps comes down to letting the surface dry and see daylight: cut back overhanging branches and shrubs, clear leaf litter and debris that hold damp, improve drainage so water does not sit, and on roofs fit zinc or copper strips whose run-off discourages regrowth. None of this is dramatic, but a surface that dries out between downpours grows far less moss than one that stays perpetually shaded and wet.</p>

      <h2>The honest caveat</h2>
      <p>If a surface is permanently shaded and damp, moss will keep coming whatever you do. At that point the real choice is between clearing it on a schedule and simply accepting a little green. Away from steps and other places where a slippery film is a hazard, living with it is far less work and arguably better looking than a constant chemical battle.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-lawn"] = dict(
    title="How to make a moss lawn",
    description="Making a moss lawn: when it is the right choice, preparing the ground, planting by transplant or slurry, watering it in, and keeping a moss lawn over the years.",
    active="guides",
    hero="hero.jpg",
    blurb="A green, no-mow, drought-proof carpet for shade. When to choose it, and how to establish and keep one.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">In a shaded, damp garden a moss lawn is soft underfoot, green through winter and drought, and free of mowing, feeding and watering once established. Where grass struggles, it is often the better surface, not the consolation prize.</p>

      <h2>Is your site right?</h2>
      <p>Moss lawns want shade or part shade, reliable moisture, and acidic, firm, low-nutrient ground. A spot that bakes in afternoon sun is the wrong place; a cool, damp, north-facing or tree-shaded area is ideal. If grass already sulks there and moss is creeping in on its own, the site is telling you what it wants.</p>

      <h2>Prepare the ground</h2>
      <p>Strip off the existing grass and weeds, level the surface, then firm it down; moss likes contact with compacted ground, not fluffy tilth. Do not add compost or feed. On limey soils a light dressing of something acidic helps tip the balance in moss's favour.</p>

      <h2>Plant it</h2>
      <p>Either press fresh patches of moss firmly onto the prepared surface, butted tight together, or blend moss into a slurry with water or buttermilk and spread it over the area. Carpet-forming species such as the springy turf-mosses and feather mosses knit into a lawn faster than cushion types.</p>

      <h2>Establish and keep it</h2>
      <p>Mist daily for the first three or four weeks, ideally with rainwater, while the moss grips. After that, rainfall and shade do most of the work. The only routine job is clearing fallen leaves in autumn so the moss is not smothered. Walk on it lightly while young; once thick it takes gentle use. It improves every year.</p>

      <h2>What to expect, year by year</h2>
      <p>Temper your expectations on timing and a moss lawn is a delight; expect an instant carpet and you will be disappointed. In the first few months the patches or slurry green up and begin to spread, looking patchy and unconvincing while they do. Across the first full year they knit together into more or less continuous cover. By the second and third years the lawn has thickened into the deep, even, springy surface people picture, and from then on it simply improves, deepening and filling as the seasons pass. The slow start is the price of a surface that then needs almost nothing.</p>

      <h2>Honest comparison with grass</h2>
      <p>A moss lawn is not a like-for-like swap for turf, and it helps to know the trade in advance. Against grass it wins on shade tolerance, winter colour, drought resilience and upkeep, no mowing, no feeding, little watering. It loses on hard wear: it will not take football, a running dog or daily heavy footfall the way a sports lawn does, though it copes with normal garden use and stepping stones. So the honest summary is that moss suits a shaded, gently used garden beautifully and a sunny, child-and-ball-battered one poorly. Choose it for the right spot and it outperforms grass; force it into the wrong one and it struggles.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-pole"] = dict(
    title="Moss poles for climbing houseplants",
    description="Moss poles explained: why climbing aroids like monstera and pothos benefit, sphagnum versus coir poles, how to make and mount one, and keeping it damp so aerial roots grip.",
    active="guides",
    hero="monstera-pole.jpg",
    blurb="Why monstera and other climbers love them, how to make one, and how to keep it damp so aerial roots grip.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A moss pole gives a climbing houseplant something to do what it does in the wild: grip a damp vertical surface with its aerial roots and haul itself upward. For aroids such as monstera, pothos and philodendron it often means bigger leaves and a stronger plant.</p>

      <h2>Why it helps</h2>
      <p>These plants are climbers. Given a damp, textured support, their aerial roots attach and feed, and the plant frequently responds by producing larger, more mature foliage than it would scrambling along the ground or flopping out of a pot. The pole also keeps a big plant upright and tidy.</p>

      <h2>Sphagnum or coir</h2>
      <p>This is the one moss-wall context where sphagnum is exactly right. A pole stuffed with damp sphagnum holds water and stays moist, which is what the roots want, and being upright and regularly watered it does not suffer the way sphagnum would on a dry vertical wall. Coir poles are tidier and longer-lasting but hold less water; sphagnum is messier but the roots love it.</p>

      <h2>Making and using one</h2>
      <p>Form a tube of plastic mesh, pack it firmly with pre-soaked sphagnum, and stand it in the pot behind the plant, anchored into the soil. Tie the stems in loosely to start, guiding the nodes against the moss. Then keep the pole damp: mist it daily or pour water down the top, and the aerial roots will grow into it and grip on their own. Extend the pole as the plant climbs.</p>

      <h2>Keeping it damp without the bother</h2>
      <p>The whole benefit rests on the pole staying moist, and a dry pole is the usual reason aerial roots refuse to attach. Daily misting works but is easily forgotten; growers with several plants tend to rig something steadier. A length of capillary wick run from a small reservoir at the top, a self-watering pole with a hollow core you simply top up, or a weekly thorough soak of the whole pole in the shower all keep the sphagnum damp with less fuss than hand-misting. Warm, humid air helps too, which is why these plants and their poles do well in a steamy bathroom.</p>

      <h2>Extending and the usual mistakes</h2>
      <p>Add to the pole before the plant overtops it rather than after, since a stem that has grown past its support flops and is awkward to retrain. Most problems come from two habits: letting the pole dry out, so roots never grip, and tying stems so tightly that they are throttled or snapped. Tie loosely, guide rather than force, and let the plant do the climbing itself. A pole that stays damp and is extended in good time turns a sprawling, leggy aroid into an upright specimen with markedly larger leaves.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["aquarium-moss"] = dict(
    title="Aquarium mosses",
    description="Aquatic mosses for the planted tank: Java moss, Christmas moss, flame moss and Weeping moss, how to attach them to wood and rock, and the light and trimming they need.",
    active="guides",
    blurb="Java moss and friends: attaching them to wood and rock, the light they want, and keeping them tidy underwater.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Mosses are not only land plants. A handful of true mosses grow happily underwater, and they are among the most useful plants in the aquarium: undemanding, slow to outgrow, and the natural cover for fry and shrimp.</p>

      <h2>The usual suspects</h2>
      <ul class="loose">
        <li><strong>Java moss</strong> (<em>Taxiphyllum barbieri</em>): the classic, nearly indestructible, grows in almost any light.</li>
        <li><strong>Christmas moss</strong> (<em>Vesicularia montagnei</em>): tidier, with a fir-branch shape, a little more demanding.</li>
        <li><strong>Flame moss</strong> (<em>Taxiphyllum</em> "Flame"): grows upward in twisting flame-like columns.</li>
        <li><strong>Weeping moss</strong> (<em>Vesicularia ferriei</em>): trails downward, lovely draped over wood.</li>
      </ul>

      <h2>Attaching it</h2>
      <p>Aquatic moss does not root into substrate; it clings to hard surfaces by rhizoids, exactly as land moss does. Tie or wrap a thin layer over wood or rock with cotton thread or fine fishing line, or use a dab of cyanoacrylate gel. Spread it thin; a thick wad rots underneath because water cannot reach the inner strands. In a few weeks it grips on its own and the thread can be removed or will simply rot away.</p>

      <h2>Light, flow and trimming</h2>
      <p>Most aquarium mosses are content in low to moderate light and do not need added carbon dioxide, though brighter light and CO2 give denser, neater growth. Gentle flow keeps debris from settling in the strands, which otherwise traps muck and starves the moss. Trim with scissors to keep the shape; the clippings will start new patches wherever they settle.</p>

      <h2>What moss does for the tank</h2>
      <p>Beyond looking good, moss pulls real weight in a planted tank. Its dense tangle grows the biofilm that shrimp and young fish graze, and it gives fry and shrimplets both food and cover at the moment they are most vulnerable, which is why breeders treat it as close to essential. It also offers a surface for beneficial bacteria, mops up a little excess nutrient, and shelters the small invertebrates that round out a tank's ecology. For dwarf shrimp in particular there is a dedicated piece on <a href="moss-for-shrimp.html">how moss benefits Caridina and Neocaridina</a>.</p>

      <h2>Aquascaping with moss</h2>
      <p>Aquascapers prize moss because it does what almost nothing else underwater will: clothe hardscape. Tied thin over branching wood it reads as foliage on a miniature tree; bound to a flat stone it makes a mossy boulder; grown on a mesh panel it becomes a wall or a lawn. The look depends on trimming, since an untrimmed clump turns shapeless and shades out its own base, so regular light scissoring keeps it crisp and healthy. Growing the carpet in emersed first, by the dry start method, gives the densest, most even result; both that and bulk-growing are covered in <a href="propagating-aquarium-moss.html">how to propagate aquarium moss</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["telling-moss-apart"] = dict(
    title="Moss, lichen, liverwort or algae?",
    description="How to tell moss from the things mistaken for it: liverworts, lichens, algae and clubmosses, with the simple features that separate each.",
    active="guides",
    blurb="The green stuff on the wall is not always moss. The simple features that separate moss from its lookalikes.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">"Moss" gets blamed for a lot of green that is not moss at all. Telling them apart takes only a close look, and it matters because they want different things and respond differently to treatment.</p>

      <h2>True moss</h2>
      <p>A soft, leafy plant with tiny leaves arranged around a stem, forming cushions or carpets, very often with fine stalks carrying capsules held above the green. If you can see little leafy shoots and stalked capsules, it is a moss.</p>

      <h2>Liverwort</h2>
      <p>Either flat and ribbon-like, pressed close to the surface in branching green lobes (the thallose kind), or leafy and very low-growing. No upright leafy stems like a moss, and the spore capsules, when present, are quite different. Liverworts favour really wet, often disturbed ground, such as the surface of pot compost.</p>

      <h2>Lichen</h2>
      <p>Not a plant at all, but a partnership of a fungus and an alga living as one. Lichens are usually crusty, leafy or shrubby in texture and often grey, white, yellow or orange rather than fresh green. They feel dry and tough, not soft, and grow very slowly on bark, stone and roofs. Reindeer "moss" is in fact a lichen.</p>

      <h2>Algae</h2>
      <p>A formless green film or slime with no leaves, stems or structure at all, on damp paving, timber, glass and pots. If you can smear it and there is nothing leafy to it, it is algae.</p>

      <h2>Clubmosses</h2>
      <p>These look mossy but are larger, with tougher, scaly stems, and belong to an ancient vascular group quite separate from the true mosses. Mostly you meet them on heath and hill rather than in the garden.</p>

      <h2>A quick field test</h2>
      <p>Faced with a patch of green and unsure what it is, a few seconds of looking usually settles it. Is it soft and leafy, made of tiny shoots you could tease apart, often with fine stalks standing above it? That is moss. Is it flat, lobed and pressed to the surface with no upright shoots? Liverwort. Is it crusty, leathery or shrubby, dry to the touch and a colour other than fresh green? Lichen. Is it a structureless film or slime you can wipe away in one smear? Algae. A hand lens turns these hunches into certainties, and once you have checked a dozen patches the answer comes at a glance.</p>

      <h2>Why the distinction is worth making</h2>
      <p>It is not mere pedantry. The four groups want different conditions and respond differently to whatever you do about them, so misidentifying the green is the first step to mistreating it. Algae signals a surface that is simply too wet and shaded and will wipe off; lichen is slow-growing and harmless and generally best left; liverwort on pot compost points to overwatering; and moss, depending on where it is, may be a welcome carpet or a slip hazard to manage. Knowing which you have tells you whether to leave it, encourage it or clear it.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["life-in-moss"] = dict(
    title="The hidden world in a moss cushion",
    description="The miniature ecosystem inside a moss cushion: tardigrades, springtails, mites, rotifers and nematodes, and why moss is such a rich habitat in miniature.",
    active="guides",
    blurb="Tardigrades, springtails and a whole micro-ecosystem live in a single moss cushion. A look at the tiny world inside.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Pull up a cushion of moss and you are holding a small, crowded world. The damp, sheltered spaces between the leaves are home to a community of tiny animals, and one of them is among the toughest creatures known.</p>

      <h2>The water bears</h2>
      <p>Tardigrades, the "water bears", are eight-legged animals under a millimetre long that live in the film of water around moss leaves. When the moss dries, they dry too, curling into a desiccated tun and shutting their metabolism almost entirely off. In that state they have survived being frozen, boiled, irradiated and even the vacuum of space, springing back when wetted. Moss is the easiest place to find them: soak a dry cushion, squeeze the water into a dish, and look under a cheap microscope.</p>

      <h2>The rest of the crowd</h2>
      <p>They share the cushion with springtails, which flick themselves into the air with a sprung tail; mites; rotifers, the "wheel animalcules" that whirl food into their mouths; nematode worms; and the protozoa and bacteria they all feed on. A handful of moss can hold thousands of individuals across dozens of species.</p>

      <h2>Why moss is such good habitat</h2>
      <p>Moss does for these animals what it does for itself: it holds water, buffers the swings of temperature and humidity, and provides endless sheltered surface in a small space. Lose the moss from a wall or a wood and you lose this whole layer of life, and the larger creatures that feed on it. It is a reminder that the quiet green is doing more than it appears.</p>

      <h2>Look for yourself</h2>
      <p>Finding this world takes almost nothing. Collect a dry cushion of moss, drop it into a jar of water and leave it to soak for an hour or two, then squeeze the water out into a shallow dish or onto a glass slide. Under a basic microscope, even a cheap one or a clip-on phone lens at decent magnification, the drop comes alive: tumbling rotifers, scuttling mites, the unmistakable plodding gait of a tardigrade. Children find it spellbinding, and it costs the price of a jam jar. A drop from different mosses, or from a wall versus a wood, turns up noticeably different casts of characters.</p>

      <h2>A measure of a healthy place</h2>
      <p>The richness of that hidden community is also a quiet indicator. A moss cushion teeming with varied life sits in clean, undisturbed surroundings; a thin, sparse one often reflects pollution or disturbance nearby. Researchers lean on this, sampling the animals in moss as one read on the health of a habitat. For the gardener the lesson is gentler: a mossy, undisturbed corner is not a sign of neglect but a small reservoir of biodiversity, and leaving it be supports far more than the moss itself.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["growing-moss-from-spores"] = dict(
    title="Growing moss from spores",
    description="Growing moss from spores and fragments: how moss spreads naturally, the realistic fragment and slurry methods, and why spore-from-scratch is slow and unpredictable.",
    active="guides",
    blurb="Can you grow moss from spores like seed? Sort of. What works, what does not, and the faster fragment route.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">People often ask whether moss can be grown from spores the way you sow seed. It can, in principle, but it is slow and unpredictable, and there is almost always a faster route to the same place.</p>

      <h2>How moss spreads naturally</h2>
      <p>A ripe capsule releases dust-fine spores to the wind. A spore that lands somewhere damp and shaded germinates into a fine green thread called a protonema, which spreads and then buds into recognisable leafy shoots. The whole sequence is gradual and depends entirely on conditions staying damp throughout.</p>

      <h2>The realistic methods</h2>
      <p>In practice, gardeners propagate moss from fragments rather than spores, because moss regenerates so readily from broken pieces. The two reliable approaches are pressing fresh patches onto prepared ground, and the slurry method, blending moss with water or buttermilk and spreading it. Both are described in the <a href="growing.html">growing guide</a>, and both are far quicker than starting from spores.</p>

      <h2>If you really want to start from spores</h2>
      <p>Scatter the contents of ripe capsules, or lay whole capsules, onto a firm, damp, low-nutrient surface in shade, and keep it constantly moist and undisturbed for weeks to months. Results are erratic; whatever moss spores happen to be in your air may colonise the patch before your chosen species does. Treat it as an experiment rather than a reliable way to cover ground.</p>

      <h2>The protonema, and why patience is everything</h2>
      <p>It helps to know what is going on during the long wait. A germinating spore does not turn straight into a recognisable moss; first it grows a sprawling mat of fine green threads called the protonema, which can look like little more than a green algal film for weeks before the upright leafy shoots, the part you would call moss, finally bud from it. Many people give up at the film stage, assuming nothing is happening or that algae have taken over. The threads are fragile and depend utterly on the surface never drying, so the slightest neglect sets the whole thing back. This is the real reason spores are a poor way to cover ground: the vulnerable phase is long.</p>

      <h2>Where growing from spores does make sense</h2>
      <p>For covering an area, fragments win every time. But sowing spores has its place. It is how laboratories and serious enthusiasts raise particular species that are hard to source as living material, and it is a genuinely rewarding thing to watch under controlled, sterile-ish conditions on agar or a sterilised substrate, where competing spores from the air are excluded. Approached as a patient experiment rather than a quick way to green a path, it is a window into a part of the plant's life most people never see.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["spraying-moss"] = dict(
    title="Spraying moss slurry at scale",
    description="Applying moss slurry with a sprayer to cover a whole wall: why an airless sprayer is the wrong tool, which low-pressure hopper and hydroseeding kit works, slurry consistency, and keeping the fragments alive.",
    active="guides",
    hero="thuidium.jpg",
    blurb="Cover a whole wall in an afternoon. Why airless sprayers fail, which gear works, and how to keep the moss alive.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">The slurry method works beautifully painted on by hand, but for a whole wall you will want to spray it. The trick is choosing a tool that suits a lumpy, fibrous, living mix, which rules out the obvious one.</p>

      <h2>Why not an airless sprayer</h2>
      <p>An airless rig atomises at very high pressure, often 1,500 to 3,000 psi, through a tiny tip around 0.013 to 0.021 inch. Two things go wrong. The tip clogs almost at once on the fibres and fragments in a moss mix, so you spend the job unblocking it. Worse, the only way to pass that tip is to blend the moss to a fine puree, and the shredding plus the pressure destroy most of the living cells. Moss regrows from viable fragments, so a fine, high-shear spray paints the wall green with material that will not grow.</p>

      <h2>The tools that do work</h2>
      <p>Think low pressure and a big orifice instead:</p>
      <ul class="loose">
        <li><strong>Texture or hopper gun</strong> (the drywall and render type, fed by a compressor), set to its largest nozzle. Cheap, and built for lumpy mixes.</li>
        <li><strong>Render or tyrolean sprayer</strong> for masonry coatings.</li>
        <li><strong>Hydroseeding kit</strong>, the industrial analogue, which sprays a seed-and-mulch slurry through wide nozzles at low pressure. A moss slurry is the same principle.</li>
        <li><strong>A coarse pump or garden sprayer with the tip removed</strong>, for a small wall, giving a usable splatter.</li>
      </ul>

      <h2>Mixing for the gun</h2>
      <p>Blend in short pulses to a coarse, just-pourable consistency, not a smoothie; you want the largest fragments the nozzle will pass, because bigger pieces hold more living tissue. Thin with rainwater rather than loading it with thick buttermilk, which clogs and adds unwanted nutrients. A spoonful of water-retaining gel helps it cling to a vertical surface. Strain out only the coarsest woody bits that would jam the nozzle, and no more.</p>

      <h2>Keep the pressure and the losses down</h2>
      <p>Run the lowest pressure that will throw the mix. Every increase in pressure and every reduction in fragment size costs you viability, so the gentle, coarse, low-pressure end of the range gives the best take even though it feels less like "spraying paint". Expect to lose some of the moss to the process and apply a little more thickly to compensate.</p>

      <h2>After spraying</h2>
      <p>Nothing about the gun changes what moss needs. The wall must be shaded, damp and porous, and you must keep the sprayed area misted daily for the first few weeks while the fragments establish. Done on the right wall, you can green a large area in an afternoon that would take days by brush. See <a href="moss-graffiti.html">moss graffiti</a> for the hand method and <a href="moss-walls.html">living moss walls</a> for the conditions.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["aquarium-moss-real-or-not"] = dict(
    title="Which aquarium “mosses” are really moss",
    description="Java moss is a true moss, and so are most named aquarium mosses. But marimo balls are algae, Riccia and Pellia are liverworts, and Süsswassertang is a fern. A guide to the real and the impostors.",
    active="guides",
    blurb="Java moss is the real thing. Marimo balls, Riccia and Süsswassertang are not. Sorting the true mosses from the impostors.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">It is a fair thing to wonder, because the aquarium trade calls a lot of unrelated plants "moss". The surprise is which way it falls: Java moss really is a moss, while several of the other "mosses" in the hobby are nothing of the sort.</p>

      <h2>The real mosses</h2>
      <p>Java moss is a genuine true moss, <em>Taxiphyllum barbieri</em> (long sold under the old name <em>Vesicularia dubyana</em>, which caused years of confusion in the trade). It is a bryophyte, the same broad group as the moss on a wall, simply one that grows submerged. So are most of the other named aquarium mosses:</p>
      <ul class="loose">
        <li>Christmas moss (<em>Vesicularia montagnei</em>)</li>
        <li>Flame moss (<em>Taxiphyllum</em> "Flame")</li>
        <li>Weeping moss (<em>Vesicularia ferriei</em>)</li>
        <li>Taiwan moss (<em>Taxiphyllum alternans</em>)</li>
        <li>Phoenix moss (<em>Fissidens fontanus</em>)</li>
        <li>Willow moss (<em>Fontinalis antipyretica</em>)</li>
      </ul>
      <p>All true mosses. If the label says one of these, you are growing the real thing.</p>

      <h2>The impostors</h2>
      <p>These are sold and used like mosses but belong to entirely different groups:</p>
      <ul class="loose">
        <li><strong>Marimo "moss balls"</strong> (<em>Aegagropila linnaei</em>) are not moss and not even a plant in the usual sense. They are a green <strong>alga</strong> that happens to grow into a velvety sphere.</li>
        <li><strong>Riccia or crystalwort</strong> (<em>Riccia fluitans</em>) is a <strong>liverwort</strong>, a bryophyte cousin of moss but a separate lineage.</li>
        <li><strong>Monosolenium</strong>, often sold as "Pellia", is also a <strong>liverwort</strong>.</li>
        <li><strong>Süsswassertang</strong>, sometimes called round pellia, is stranger still: it is the gametophyte stage of a <strong>fern</strong>, with no true leaves or stems at all.</li>
      </ul>

      <h2>Does it matter?</h2>
      <p>For day-to-day growing, not hugely; most behave like low-light, undemanding plants you attach to wood or rock. But it is worth knowing, because care differs at the edges, an alga and a fern are not going to respond to advice written for moss, and it saves you the embarrassment of insisting a marimo ball is a moss. For attaching and trimming the genuine aquarium mosses, see the <a href="aquarium-moss.html">aquarium mosses</a> guide; for telling the land groups apart, see <a href="telling-moss-apart.html">moss, lichen, liverwort or algae</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-on-roofs"] = dict(
    title="Moss on roofs: is it a problem?",
    description="Whether moss damages a roof, why you should never pressure-wash it off, how to remove it safely, how to stop it returning, and moss as a lightweight green roof where a heavy sedum or substrate roof would be too much load.",
    active="guides",
    hero="hypnum.jpg",
    blurb="Does it harm the roof? Why not to pressure-wash, safe removal, prevention, and moss as a lightweight green-roof option.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss on a roof looks alarming and is usually less serious than it appears, but it is worth managing for two real reasons. Here is what it does, what not to do about it, and how to keep it down.</p>

      <h2>Does it harm the roof?</h2>
      <p>Moss does not eat into sound tiles or slates. The genuine problems are indirect: thick growth holds moisture against the surface, which matters in a hard frost when trapped water freezes and flakes the face of a tile, and clumps break off and block gutters and valleys, backing water up under the edges. On a sound roof it is mostly cosmetic; on an old or north-facing one it is worth staying on top of.</p>

      <h2>Why not to pressure-wash</h2>
      <p>This is the big one. A pressure washer blasts the protective surface off tiles and slates, drives water under them, and takes years off the roof's life. It does far more damage than the moss ever would. Whatever you read, do not jet-wash a roof to clean moss.</p>

      <h2>Removing it safely</h2>
      <p>Brush it off dry with a stiff brush, working downward so you do not lift the tiles, and clear the gutters and valleys while you are there. Do this from a safe platform or leave it to someone who works at height; a wet mossy roof is treacherous. There is no rush, so wait for dry weather and good access.</p>

      <h2>Keeping it down</h2>
      <p>Moss returns wherever the roof stays damp and shaded, so reduce that: cut back overhanging branches to let in light and air. Fitting a strip of zinc or copper along the ridge works well, since rain washes a trace of metal down the slope that moss dislikes, slowing regrowth for years. For the general principles, see <a href="removing-moss.html">how to get rid of moss</a>.</p>

      <h2>Moss as a deliberate green roof, and the weight question</h2>
      <p>So far this has been about unwanted moss. Moss can also be the point: a living green roof, deliberately grown on a shed, garage, extension or low-pitch deck. Here moss has one big advantage, which is weight.</p>
      <p>A conventional green roof is heavy. An extensive sedum or substrate system typically adds somewhere around 60 to 150 kg per square metre once it is fully saturated, and an intensive roof garden a great deal more again. That is real structural load, and many roofs, especially older ones and lightweight timber structures, cannot take it without strengthening and an engineer's sign-off. The weight is the single most common reason a green roof is ruled out.</p>
      <p>Moss is one of the lightest living coverings there is. A moss mat over a thin layer of growing medium weighs far less than a sedum-and-substrate build, which sometimes makes a living roof possible on a structure that could never carry the conventional kind. Two cautions, though. First, moss holds a lot of water, so always reckon on the <em>saturated</em> weight plus any snow load, not the dry weight, when you or an engineer check the roof. Second, a light mat catches the wind, so it needs securing and good edge detailing against uplift.</p>
      <p>It is not a free pass: you still need sound waterproofing beneath it, a shaded or north-facing aspect and a low pitch suit moss best, and anything you deliberately install should have its loading checked rather than assumed. But where a traditional green roof is simply too heavy, a moss roof is often the version that can actually go ahead.</p>

      <h2>What it does to rainwater collection</h2>
      <p>If you harvest rainwater into a butt or tank, a moss or green roof works against you, on both quantity and quality. It is the same water-holding that makes moss useful elsewhere, turned into a drawback here.</p>
      <p><strong>Quantity.</strong> Moss is a sponge. A moss roof soaks up a large share of the rain that lands on it and evaporates much of it straight back to the air, so light showers can produce almost no run-off until the moss is saturated. Over a year an extensive green roof commonly retains something like half the rainfall, which means your tank sees far less than the same area of plain tile or metal would deliver.</p>
      <p><strong>Quality.</strong> The water that does run off a living roof carries organic matter, tannins that stain it brown, nutrients, and fine particles from the moss and any growing medium. That is fine for watering the garden, but it discolours stored water, feeds algae in the butt, and clogs fine filters faster, so it is poorly suited to clean or drinking use without good filtration and a first-flush diverter.</p>
      <p><strong>The flip side.</strong> That same retention is a real benefit for stormwater: it slows and reduces run-off and eases the load on drains in a downpour. So it is a genuine trade-off. If your aim is to fill a tank with as much clean water as possible, keep moss off the collecting roof and run a hard tile or metal surface to the gutter. If slowing run-off and cooling the building matter more to you, the green roof wins, but expect less water in the butt and browner water at that.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["best-moss-for-terrariums"] = dict(
    title="The best mosses for a terrarium",
    description="Choosing moss for a terrarium: cushion versus carpet species, reliable choices like bun moss, broom fork-moss, mood moss and sheet moss, where to source them, and what to avoid.",
    active="guides",
    hero="dicranum.jpg",
    blurb="Cushion or carpet? The species that thrive under glass, where to get them, and which to avoid.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Almost any moss survives in a closed terrarium, but some look far better and behave far better than others. A quick guide to choosing.</p>

      <h2>Cushion or carpet</h2>
      <p>Cushion mosses grow in domed mounds and hold their shape beautifully behind glass, giving a terrarium structure and little hills. Carpet or feather mosses spread flat to cover ground and soften the floor between features. Most good terrariums use one or two cushions for height and a carpet to knit it together.</p>

      <h2>Reliable choices</h2>
      <ul class="loose">
        <li><strong>Bun moss</strong> (<em>Leucobryum</em>): the classic pale-green dome, holds its shape for years.</li>
        <li><strong>Broom fork-moss</strong> (<em>Dicranum scoparium</em>): springy combed cushions, very photogenic.</li>
        <li><strong>Mood moss</strong> (<em>Dicranum</em> types sold under this name): larger clumps for a wilder look.</li>
        <li><strong>Sheet or carpet moss</strong> (<em>Hypnum</em> and relatives): the flat green floor.</li>
        <li><strong>Fern moss</strong> (<em>Thuidium</em>): fine, frond-like, lovely as an accent.</li>
      </ul>

      <h2>Where to get it</h2>
      <p>You can collect small amounts from your own garden, walls and paths, which is free and local; take a little from several places rather than stripping one patch, and rinse off soil and creatures. Specialist terrarium suppliers sell named, clean cushions if you want a particular look or to avoid introducing pests.</p>

      <h2>What to avoid</h2>
      <p>Skip bog moss (sphagnum) unless you are deliberately running a wet, boggy setup, as it wants saturation. Be wary of moss lifted with a lot of soil and leaf litter, which brings in mould spores, slugs and springtails; a closed jar will happily incubate all of them. A quick rinse and a look-over saves trouble later. See the <a href="terrariums.html">terrarium guide</a> for building and care.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-indoors"] = dict(
    title="Can you keep moss as a houseplant?",
    description="Keeping moss alive indoors: why moss browns in a normal room, why a closed terrarium is the reliable answer, caring for open dishes and bonsai, and the light moss needs inside.",
    active="guides",
    blurb="Why moss browns on a windowsill, why a closed jar is the answer, and how to keep it green indoors.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">People bring moss indoors expecting a low-effort green and watch it turn brown in a fortnight. It is not that moss is fussy; it is that a normal room is the wrong climate. Here is how to keep it alive inside.</p>

      <h2>Why it browns on the windowsill</h2>
      <p>A heated room is dry, and dry air is moss's main enemy indoors. Out in the open it loses water faster than it can take it up, dries out and goes dormant, and if it stays dry it eventually dies rather than just resting. Direct sun through glass finishes it off fast. Open moss in a normal living room is fighting a losing battle.</p>

      <h2>The reliable answer: a closed terrarium</h2>
      <p>A lidded glass jar or bowl traps humidity and recycles it, which is exactly what moss wants, and turns it into a near-zero-maintenance feature. This is the honest answer to "moss as a houseplant": grow it behind glass and it thrives for years. See the <a href="terrariums.html">terrarium guide</a> and the <a href="best-moss-for-terrariums.html">species roundup</a>.</p>

      <h2>Open dishes and bonsai</h2>
      <p>If you want moss in the open, on a bonsai or in a shallow dish, you are signing up to mist it daily and keep it out of direct sun and away from radiators. It can be done in a humid room such as a bright bathroom, but it is hands-on. A room sitting at higher humidity, well above half, makes it far easier.</p>

      <h2>Light</h2>
      <p>Moss does not want strong light, but it does need some. Bright, indirect light is ideal; deep gloom leaves it weak and prone to algae. A spot near a north window, or a low-output grow light for a closed setup, keeps it healthy without cooking it.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["peat-and-peat-free"] = dict(
    title="Sphagnum, peat, and why peat-free matters",
    description="How sphagnum moss builds peat, why peat bogs matter for carbon and water, the cost of digging peat for compost, and the peat-free alternatives available to growers.",
    active="guides",
    hero="sphagnum.jpg",
    blurb="How bog moss makes peat over millennia, why digging it up is so costly, and what to use instead.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Of all the things moss does, building peat is the one with the biggest consequences. It is worth understanding, because it is why "peat-free" is written on compost bags now.</p>

      <h2>How sphagnum makes peat</h2>
      <p>Sphagnum, the bog mosses, grow in waterlogged, acidic, oxygen-poor ground. The old growth beneath the living surface does not fully rot, because there is too little oxygen and the conditions are too acidic for the usual decomposers. Instead it accumulates, layer on layer, over thousands of years, as peat. A deep peat bog is, in effect, millennia of moss stacked up and half-preserved.</p>

      <h2>Why bogs matter</h2>
      <p>Because the carbon in all that moss never finished decomposing, peatlands lock away enormous amounts of it, more per hectare than forest. They also hold and slowly release vast quantities of water, steadying rivers and reducing floods, and they are home to specialised plants and animals found nowhere else. Intact, they are quietly doing several important jobs at once.</p>

      <h2>The cost of digging it</h2>
      <p>Cutting peat for fuel or compost drains the bog, exposes the stored carbon to the air, and releases it. A resource that took thousands of years to form is gone in one season's growing, and the carbon it held goes into the atmosphere. That is the case against peat compost in a sentence.</p>

      <h2>Peat-free for growers</h2>
      <p>Modern peat-free composts use coir, wood fibre, bark, green compost and similar materials. They behave a little differently, tending to dry on top while staying wet below, so they reward checking the moisture lower down rather than watering on a fixed schedule. For most growing they now work well, and they leave the bogs where they are.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-myths"] = dict(
    title="Moss myths, busted",
    description="Common myths about moss put straight: whether it kills lawns, harms trees, only grows on the north side, whether marimo balls and Java moss are really moss, and more.",
    active="guides",
    blurb="It kills lawns, harms trees, only grows on the north side? The common moss myths put straight.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss attracts more folklore than most plants. A few of the common claims, and what is actually true.</p>

      <h2>"Moss is killing my lawn"</h2>
      <p>It is the other way round. Moss moves in where grass has already weakened through shade, compaction or poor drainage, taking the space the grass has vacated rather than driving it out. Clear the moss and leave those conditions unchanged and it simply returns, which is why the <a href="lawn.html">moss and lawns</a> guide spends its time on the conditions rather than the moss.</p>

      <h2>"Moss damages trees"</h2>
      <p>It does not. Moss on bark uses the trunk only as a perch and draws nothing from it. If anything its presence speaks well of the air, since moss favours clean, damp conditions. A mossy old tree is a healthy sight, not a warning.</p>

      <h2>"Moss only grows on the north side"</h2>
      <p>A half-truth worth understanding. Moss prefers the cooler, damper, shadier face of a tree or wall, and in the northern hemisphere that is most often the north side, so the old navigation lore holds up loosely. What the moss is actually tracking is shade and moisture, though, not a compass bearing. In a damp wood it grows merrily on every side, so treat it as a hint rather than a reliable direction-finder.</p>

      <h2>"You have to pressure-wash it off"</h2>
      <p>Please do not, least of all on a roof, where the jet strips the weatherproof surface from tiles and slates and costs you far more than the moss ever would. A dry brush does the job without the harm. The <a href="moss-on-roofs.html">roof guide</a> goes into why.</p>

      <h2>"Marimo balls are moss"</h2>
      <p>A common one in the aquarium hobby, and wrong: the marimo "moss ball" is a green alga that happens to grow into a velvety sphere. Confusingly, Java moss really is a moss, so the trade gets it both ways round. The full sorting is in <a href="aquarium-moss-real-or-not.html">which aquarium mosses are really moss</a>.</p>

      <h2>"It has no roots, so it must feed off what it grows on"</h2>
      <p>No. The fine threads underneath are rhizoids, and their only job is to hold the plant in place. A moss feeds itself from rain, mist and airborne dust through its leaves, which is exactly why it can sit on bare rock, glass or a roof tile and take nothing from any of them.</p>

      <h2>"Moss is a fungus"</h2>
      <p>It is a plant, green and photosynthesising like any other, just an unusually simple one without roots, flowers or internal plumbing. The confusion may come from moss often keeping company with fungi and lichens in damp, shady places, but biologically they are far apart.</p>

      <h2>"Moss means a damp problem in the house"</h2>
      <p>Moss growing on an outside wall reflects shade and moisture on that wall, nothing more, and does not by itself indicate damp indoors. It does not bore into sound masonry or "spread" through a wall to the inside. Persistent damp inside has its own causes worth investigating, but a green north wall is not the diagnosis.</p>

      <h2>"You cannot grow moss on purpose"</h2>
      <p>You very much can, and people have for centuries; it just asks for the opposite of normal gardening. Give it shade, damp, poor firm ground and time, and it spreads readily from transplanted patches or a blended slurry. The whole of the <a href="growing.html">growing guide</a> is about doing it deliberately.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["how-to-identify-moss"] = dict(
    title="How to identify moss",
    description="A beginner's approach to identifying mosses to species: using a hand lens, the features that matter (leaf shape, midrib, capsule), acrocarps versus pleurocarps, and recording your finds.",
    active="guides",
    blurb="Get past 'it's a moss'. A hand lens, the features that matter, and how to start naming what you find.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Telling a moss from a lichen or liverwort is one thing; naming the actual species is another, and it is where a lot of people stall. You do not need a laboratory, but you do need a hand lens and a few habits.</p>

      <h2>Get a hand lens</h2>
      <p>A simple folding lens at ten or twenty times magnification is far and away the most useful tool, and it changes everything. Mosses are small and the features that separate species, the shape of a leaf, whether it has a midrib, the form of the little capsule, are simply invisible to the naked eye. Hold the lens close to your eye and bring the moss up to it, in good light.</p>

      <h2>The features that matter</h2>
      <ul class="loose">
        <li><strong>Growth form</strong>: does it grow in upright tufts and cushions (acrocarps) or trailing, branching mats (pleurocarps)? This first split narrows things enormously.</li>
        <li><strong>Leaf shape and arrangement</strong>: long and narrow, oval, pointed, blunt, swept to one side, spirally arranged or in ranks.</li>
        <li><strong>The midrib (nerve)</strong>: a single vein running up the leaf, present or absent, single or double, reaching the tip or stopping short.</li>
        <li><strong>The capsule</strong>: upright or nodding, round or cylindrical, on a long or short stalk, with what kind of lid. When present, capsules are full of clues.</li>
      </ul>

      <h2>Use a key and record it</h2>
      <p>With those observations you can work through a moss field guide or key, which leads you by yes-or-no questions to a name. Photograph your finds, note where and on what they grew, and consider logging them with a recording scheme or a naturalist app; verified records are genuinely useful to science, and the feedback sharpens your eye. Start with the common species on the <a href="species.html">species page</a> and build from there.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["collecting-moss"] = dict(
    title="Collecting moss responsibly",
    description="How to collect moss without harm: taking small amounts from many places, where you may and may not collect, protected sites and landowner permission, and why never to strip wild ground.",
    active="guides",
    blurb="Where you may gather moss, how much is fair, and the sites and rules to respect so you do no harm.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Most moss projects start with collecting a little, and done thoughtfully that is fine. Done carelessly it scars a place that took years to grow. A few simple principles keep you on the right side.</p>

      <h2>Little and often, from many places</h2>
      <p>Take small pieces from several spots rather than lifting one patch whole. Moss regrows from fragments and from the edges of what is left, so a light, scattered take recovers quickly, whereas a bare scrape can stay bare for years. Your own garden, walls, paths and pots are the easiest and most guilt-free source, and they usually have more than you think.</p>

      <h2>Where you may, and may not</h2>
      <p>On your own land, collect freely. On other land you need the owner's permission, and in many places removing plants from the wild without it is not allowed. Nature reserves, protected sites and designated areas are off limits; some rare mosses and their habitats are specifically protected by law, and a casual handful can be a serious matter on the wrong ground. Pavements, old walls and waste ground in towns are far less sensitive than ancient woodland or bog.</p>

      <h2>Do no lasting harm</h2>
      <p>Avoid stripping banks, boulders and tree bases that hold a place together and shelter other life; that moss is habitat as well as scenery. Take what you will actually use, clean off soil and creatures before bringing it home, and leave the spot looking as though you were never there. Treated that way, collecting moss is a gentle thing. The wild does not owe you a moss lawn; grow most of it on from a modest start, as in the <a href="growing.html">growing guide</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-and-wildlife"] = dict(
    title="Moss and wildlife",
    description="Why moss matters for wildlife: nesting material for birds, shelter and hunting ground for invertebrates, a humid refuge in dry spells, and how a mossy patch supports the wider garden.",
    active="guides",
    hero="thuidium.jpg",
    blurb="Nesting material, invertebrate shelter, a damp refuge: how a mossy patch quietly feeds the rest of the garden.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A patch of moss is doing more for the life around it than it looks. It is food, shelter, building material and a damp refuge all at once, and the garden is poorer without it.</p>

      <h2>Birds build with it</h2>
      <p>Many birds line their nests with moss, prized for being soft, insulating and water-holding. Wrens, robins, chaffinches, long-tailed tits and others gather it every spring. A garden with moss to hand makes nest-building easier, which is one good reason not to scour every last scrap off the lawn in March.</p>

      <h2>A world for invertebrates</h2>
      <p>The damp, sheltered spaces in a moss cushion hold springtails, mites, beetles, spiders and a host of smaller creatures, and the things that eat them come looking. Moss is hunting ground as much as habitat. For the truly tiny end of that community, including the famous water bears, see <a href="life-in-moss.html">the hidden world in a moss cushion</a>.</p>

      <h2>A refuge when it is dry</h2>
      <p>Because moss buffers humidity and temperature, it gives small animals somewhere to ride out a dry, hot spell that would see them off on bare ground. In a warming climate that buffering matters more, not less. A mossy log, wall base or shady corner is a little reservoir of cool and damp the rest of the garden can draw on.</p>

      <h2>Leaning into it</h2>
      <p>You do not have to do much: leave some moss rather than removing all of it, keep a shady damp corner, and resist the urge for a sterile, scrubbed surface everywhere. A garden that tolerates moss supports more life, with no extra work. See <a href="uses.html">what moss is good for</a> for the wider picture.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-in-history"] = dict(
    title="Moss through history",
    description="Historical uses of moss: chinking log cabins, stuffing and packing, Ötzi the Iceman, and sphagnum wound dressings in the First World War. How a humble plant has served for millennia.",
    active="guides",
    hero="hero.jpg",
    blurb="Cabin chinking, packing, the Iceman, and wartime wound dressings: how moss has served people for millennia.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss is so ordinary that it is easy to forget how long and how usefully people have relied on it. A short tour of the humble plant's working past.</p>

      <h2>Building and packing</h2>
      <p>For centuries moss chinked the gaps between the logs of cabins and the planks of boats, sealing out draughts and damp because it packs tight, holds a little moisture and resists rot. Dried moss stuffed mattresses, pillows and cushions, and padded all manner of goods in transit, including plants and bulbs sent long distances. Light, springy and free, it was the obvious material to hand.</p>

      <h2>The Iceman's moss</h2>
      <p>When the 5,000-year-old body known as Ötzi was found in the Alps, mosses were among the plant remains with him, including pieces that had no business growing where he died. They had been carried, used for packing or wrapping, and they help researchers trace where he had been. Even a Copper Age traveller had moss about his person.</p>

      <h2>Sphagnum and the wars</h2>
      <p>The best-known chapter is medical. Sphagnum, the bog moss, is highly absorbent and slightly acidic, which discourages bacteria, and it had been used on wounds for a very long time. When the First World War outran the supply of cotton dressings, sphagnum was gathered from bogs by the sackful, cleaned and sewn into dressings, and it genuinely saved lives. It is a striking thing to remember while looking at a patch of moss on a wall.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["watering-moss"] = dict(
    title="Water for moss: rainwater or tap?",
    description="The best water for moss: why rainwater suits it and hard tap water does not, the problem with lime and chlorine, and practical watering for moss lawns, walls and terrariums.",
    active="guides",
    blurb="Why rainwater beats hard tap water for moss, what lime and chlorine do, and how to water without overdoing it.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss takes its water in across its whole surface, so what is in that water matters more than it would for a rooted plant. The short version: rainwater is kinder than the tap, especially where the tap is hard.</p>

      <h2>Why rainwater suits it</h2>
      <p>Rainwater is soft, slightly acidic and free of additives, which is close to what most mosses meet in nature. Hard tap water is alkaline and full of dissolved lime, and over time that lime raises the surface pH and leaves a chalky scale that many mosses dislike, slowly turning a healthy patch tired and grey. Chlorine and chloramine, added to tap water to keep it safe, do moss no favours either.</p>

      <h2>When the tap is fine</h2>
      <p>If your water is naturally soft, the tap is perfectly usable. Where it is hard, save rainwater for the moss if you can; a water butt is more than enough for a lawn, a wall or a clutch of terrariums. Letting tap water stand overnight lets some chlorine off but does nothing about hardness.</p>

      <h2>How to water</h2>
      <p>Little and often beats an occasional soaking. Misting keeps the surface damp without waterlogging, which is what moss wants; standing wet with no air encourages algae and rot instead. Early morning or evening is best, so it is not drying in the midday sun. For establishing new moss, mist daily for the first few weeks, as in the <a href="growing.html">growing guide</a>; after that, in a shaded spot, the weather does much of the job.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["sphagnum-moss"] = dict(
    title="Sphagnum moss and its many uses",
    description="Sphagnum, the bog moss: what it is, why it holds so much water, and its uses for orchids and carnivorous plants, kokedama, moss poles, propagation, and historically wound dressing.",
    active="guides",
    hero="sphagnum.jpg",
    blurb="The bog moss that holds many times its weight in water. Its uses for orchids, carnivorous plants, kokedama and more.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Sphagnum is the one moss most growers handle by name, usually dried in a bag. It is the bog moss, the peat-builder, and its trick of holding many times its own weight in water makes it useful in ways no other moss is.</p>

      <h2>What it is</h2>
      <p>Sphagnum is a group of mosses adapted to waterlogged, acidic, nutrient-poor bogs. Its leaves are built with large dead cells that act as reservoirs, which is why it soaks up so much water and why, over millennia, its undecayed remains build peat. See <a href="peat-and-peat-free.html">sphagnum, peat and why peat-free matters</a> for that side of the story.</p>

      <h2>In horticulture</h2>
      <ul class="loose">
        <li><strong>Orchids</strong>: long-fibre sphagnum is a classic potting medium, holding moisture around roots that still want air.</li>
        <li><strong>Carnivorous plants</strong>: its acidity and low nutrients suit sundews, pitchers and Venus flytraps, which hate rich compost.</li>
        <li><strong>Kokedama</strong>: it binds and holds water around the root ball; see the <a href="kokedama.html">kokedama guide</a>.</li>
        <li><strong>Moss poles</strong>: damp sphagnum packed into a pole gives climbing aroids the wet, grippy surface their aerial roots want; see <a href="moss-pole.html">moss poles</a>.</li>
        <li><strong>Propagation</strong>: damp sphagnum is excellent for air-layering and rooting cuttings.</li>
      </ul>

      <h2>Live, dried and milled</h2>
      <p>Live sphagnum can be grown on the surface of carnivorous plant pots and in bog gardens. Most sold is dried long-fibre moss, which rehydrates for the uses above. Milled sphagnum, ground fine, is used as a seed-sowing medium because its mild acidity discourages the fungus that causes damping-off.</p>

      <h2>Source it with care</h2>
      <p>Sphagnum and the peat it forms come from bogs that are slow to form and important to leave intact, so look for sustainably harvested or cultivated sources rather than moss stripped from sensitive ground. Its long history as an absorbent, antiseptic wound dressing, most famously in the First World War, is covered in <a href="moss-in-history.html">moss through history</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-in-paving"] = dict(
    title="Moss in paving, patios and gravel",
    description="Moss between paving slabs, on patios and in gravel: why it grows there, when to clear it as a slip hazard, and how to encourage it for the soft stepping-stone look.",
    active="guides",
    hero="hypnum.jpg",
    blurb="Moss in the joints: when to clear it as a slip risk, and when to encourage it for that soft stepping-stone look.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss in paving divides people sharply. To some it is a slippery nuisance; to others it is the soft green seam that makes old stone look settled and right. Both are correct, in the right place.</p>

      <h2>Why it grows there</h2>
      <p>Paving joints and gravel collect grit, organic dust and moisture, and in shade they stay damp long enough for moss to take hold, especially where drainage is poor and the surface rarely dries. The mortar between slabs is often slightly alkaline at first, but as it weathers and grime builds up, moss moves in.</p>

      <h2>When to clear it</h2>
      <p>On steps and well-used paths, moss is a genuine slip hazard when wet and worth keeping down. A stiff brush and hot water shift most of it; a patio cleaner does the rest. The lasting fix is to dry the surface out: improve drainage and cut back overhanging growth so it gets light and air between downpours. Avoid pressure-washing soft or old stone, which it pits and erodes.</p>

      <h2>When to encourage it</h2>
      <p>On a quiet, shaded path, a terrace edge or between stepping stones, moss in the joints is a feature people work hard to fake. To encourage it, leave the joints alone, keep the area shaded and damp, and brush a little moss slurry into the gaps as in the <a href="spraying-moss.html">slurry method</a>. The Japanese stepping-stone look, stone set into a soft moss field, is exactly this, deliberately.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-terrarium-troubleshooting"] = dict(
    title="Why is my terrarium moss dying?",
    description="Troubleshooting a moss terrarium: browning, white fuzzy mould, streaming condensation, leggy pale growth and fungus gnats, with the cause and fix for each.",
    active="guides",
    hero="dicranum.jpg",
    blurb="Browning, white mould, fogged-up glass, leggy growth: the common terrarium problems, each with a cause and fix.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A moss terrarium should be near-effortless, so when it goes wrong it is usually one of a handful of causes. Match the symptom and fix the cause.</p>

      <h2>Browning or crisping</h2>
      <p>Almost always too dry, too hot, or too much direct sun. A closed jar in a sunny window cooks in minutes. Move it to bright, indirect light, mist with rainwater (hard tap water also browns moss over time), and make sure a closed lid is actually holding humidity.</p>

      <h2>White fuzzy mould</h2>
      <p>Too wet, too still, and usually too much decaying organic matter. Remove the affected pieces, take the lid off for a few days to dry and air it out, cut back on watering, and remove dead leaves and debris that feed the mould. A little airflow now and then prevents it.</p>

      <h2>Glass streaming with water</h2>
      <p>A light mist on the glass is healthy; water running down it means it is too wet. Leave the lid off until the inside is merely damp, then close it again. Persistent heavy condensation breeds mould.</p>

      <h2>Pale, leggy, stretched growth</h2>
      <p>Too little light. Moss does not want strong light, but in deep gloom it weakens and stretches and algae take over. Move it somewhere brighter but out of direct sun, or add a low grow light.</p>

      <h2>Fungus gnats</h2>
      <p>Little black flies usually mean the substrate is too wet and rich. Let it dry back, improve drainage, and they generally fade. Bought-in moss laden with soil is a common way to import them; a rinse first helps. See the <a href="terrariums.html">terrarium guide</a> for getting the setup right from the start.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["how-fast-does-moss-grow"] = dict(
    title="How fast does moss grow?",
    description="How quickly moss grows and spreads: realistic timescales for a slurry to green up, a lawn or wall to establish and a deep cushion to mature, what speeds it up, and why it sometimes seems to stop.",
    active="guides",
    blurb="Slower than you hope, faster than you fear. Realistic timelines, what speeds it up, and why it seems to stall.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss is not a fast plant, and that is worth knowing before you start, so you neither give up too early nor expect a carpet by next month. Here is what to actually expect.</p>

      <h2>Realistic timescales</h2>
      <p>Kept constantly damp and shaded, a slurry or fresh transplant usually starts to green up and grip within a few weeks. A patch knits into continuous cover over a few months. A convincing moss lawn or wall takes a full season or two to look established, and the deep, springy cushions of an old moss garden are the work of years. None of it is quick, but most of it is steady.</p>

      <h2>What speeds it up</h2>
      <p>Three things, mostly: constant moisture, deep shade, and firm contact with the surface. Mild temperatures help, which is why moss does much of its visible growing in the cool, damp shoulders of the year, spring and autumn, rather than high summer. Soft rainwater, a humid spot and protection from drying wind all push it along.</p>

      <h2>Why it seems to stop</h2>
      <p>Moss switches off when it dries out, shrivelling and going dormant until the next wetting, so a patch that looks dead or static in a dry spell is usually just waiting. It has not failed; it is paused. Resume the moisture and it resumes growing. The single biggest mistake is deciding it has died and giving up during a dry fortnight. Patience is most of the technique; see the <a href="growing.html">growing guide</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-and-air-quality"] = dict(
    title="Moss and air quality",
    description="Moss and air pollution: how mosses work as bioindicators of air quality, the claims about moss walls cleaning city air, and an honest look at what moss can and cannot do.",
    active="guides",
    blurb="Moss as a pollution monitor, and the truth about those 'moss walls clean city air' claims.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss and air pollution come up together a lot, partly for good reasons and partly for hype. Here is what moss genuinely does, and where the claims run ahead of the evidence.</p>

      <h2>Moss as a pollution monitor</h2>
      <p>This part is solid. Because moss has no roots and feeds straight from the air and rain, it accumulates whatever is in them, including heavy metals and nitrogen compounds. Scientists exploit this directly, sampling moss across a region to map airborne pollution cheaply and over wide areas, a technique called biomonitoring. As a sensor of air quality, moss is genuinely useful.</p>

      <h2>The moss wall claims</h2>
      <p>You will have seen installations marketed as moss walls that "clean the air of a city" or do the work of many trees. Treat these carefully. Moss does take up some particulates and gases, and a large damp moss surface has a real if modest effect on its immediate surroundings. But the headline figures are often generous, the units do not always survive scrutiny, and the walls usually need careful watering and upkeep to stay alive and effective at all. The honest position is that moss helps a little, locally, and is not a substitute for cutting pollution at source.</p>

      <h2>What moss can really offer in a city</h2>
      <p>Set aside the strongest claims and there is still a genuine case: moss surfaces cool their surroundings, hold rainwater, add habitat, and yes, monitor and modestly absorb pollution, all with very little weight or upkeep compared with planting. As one tool among many for greener, cooler streets, moss earns its place. As a magic air filter, it does not. See <a href="uses.html">what moss is good for</a> for the wider picture.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["propagating-aquarium-moss"] = dict(
    title="How to propagate aquarium moss",
    description="Propagating aquarium moss at home: multiplying Java moss and others from fragments, spreading thin on mesh or hardscape, the emersed and dry-start methods for fast bulk, and keeping it clean.",
    active="guides",
    blurb="Never buy it twice. Multiply Java moss and friends from fragments, on mesh or hardscape, submerged or emersed.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Aquarium moss is the plant you buy once. Like its land cousins it regrows readily from fragments, so a golf-ball-sized portion becomes as much as you want with a little time. Here is how to multiply it on purpose.</p>

      <h2>The basic principle</h2>
      <p>Every trim is propagation. Cut a clump of Java moss, Christmas moss or the like and each fragment can grow into a new plant, so the clippings are not waste, they are your next batch. The two things that decide success are spreading it thin and keeping it clean.</p>

      <h2>Spread it thin</h2>
      <p>The commonest mistake is piling moss on in a thick wad. The inside of a thick clump gets no light or water flow, browns and rots, while only the surface grows. Tease your moss into a thin layer over wood, rock or mesh, tie or glue it down lightly (cotton thread or a dab of cyanoacrylate gel), and it spreads outward into a clean carpet far faster than a heap ever would. See <a href="aquarium-moss.html">aquarium mosses</a> for attaching.</p>

      <h2>The mesh mat method</h2>
      <p>For a moss carpet or wall, sandwich a thin scatter of fragments between two pieces of plastic mesh, or tie it to a single flat mesh panel, and lay it where you want cover. The moss grows through the mesh and knits into an even mat you can lift, trim or split. Trimmings from the mat start the next one.</p>

      <h2>Emersed and dry-start growing</h2>
      <p>Moss often bulks up faster grown emersed, that is out of the water but in saturated, humid air, than fully submerged. Lay fragments on a damp surface in a covered, humid container with bright indirect light, much like a <a href="terrariums.html">terrarium</a>, and let it carpet up before transferring it to the tank. Aquascapers use the same idea as a dry start: plant the moss on damp hardscape in a sealed, misted tank, grow it in emersed for a few weeks, then flood. It is the quickest way to a dense carpet.</p>

      <h2>Keep it clean and lit</h2>
      <p>Moss grows faster with decent light and gentle flow, and CO2 helps if you run it, but the bigger issue is cleanliness: detritus and algae settling in the strands choke it. Gentle flow keeps it clear, and a shrimp or two will happily pick it over. Trim to shape whenever it gets shaggy, and pass the clippings to another fishkeeper; moss is the friendly currency of the hobby. For why it is slow at first, see <a href="how-fast-does-moss-grow.html">how fast does moss grow</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-propagation-machine"] = dict(
    title="Build an aquarium moss propagation box",
    description="A detailed DIY guide to building an emersed moss propagation box for aquarium moss: parts list, the reservoir and platform, lighting and humidity, an automated version, running it and harvesting.",
    active="guides",
    hero="dicranum.jpg",
    blurb="A step-by-step DIY emersed grow-box that turns a scrap of Java moss into trays of it. Parts, build, automation, harvest.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">If you want a lot of aquarium moss rather than a little, the fastest route is to grow it emersed, out of the water but in saturated, humid air, in a dedicated box. Moss bulks up faster and denser this way than submerged, and a simple sealed chamber turns a scrap of Java moss into trays of it. Here is how to build one, from a five-minute version to an automated one.</p>

      <h2>How it works</h2>
      <p>The box is just a humid chamber: a shallow reservoir of clean water, a platform that holds the moss saturated but not drowned, bright soft light, and enough air exchange to keep mould away. Get those four things right and the moss does the rest. Everything below is in service of them.</p>

      <h2>Parts list</h2>
      <ul class="loose">
        <li>A clear plastic storage box with a lid (a 10 to 30 litre tote is ideal), or any tank you can cover.</li>
        <li>A platform to lift the moss above the water: plastic egg-crate (light-diffuser grid), a section of plastic mesh on feet, or capillary matting that wicks from the reservoir.</li>
        <li>Rainwater, RO or dechlorinated water. Hard tap water leaves scale and is the main avoidable killer.</li>
        <li>A small LED grow light, or a bright cool-white LED, plus a mains timer plug.</li>
        <li>A spray bottle.</li>
        <li>Optional: a cheap thermo-hygrometer, a small 5V USB fan, and an ultrasonic mist maker (fogger).</li>
        <li>Your starter moss: Java, Christmas, flame, weeping, chopped into fragments.</li>
      </ul>

      <h2>Build it (the simple version)</h2>
      <ol>
        <li>Put 1 to 2 cm of clean water in the bottom of the box as a reservoir.</li>
        <li>Set the platform in so its top sits just above the waterline. If you are using capillary matting, drape it so one end dips in the water and wicks it up; the moss goes on the damp matting. With egg-crate or mesh, the moss sits on top and you keep it misted.</li>
        <li>Spread the moss fragments in a thin, even layer over the platform. Thin is the whole secret: a thick wad rots in the middle. You can also tie fragments to flat mesh tiles for liftable mats.</li>
        <li>Mist everything, put the lid on, and stand it somewhere warm-ish and out of direct sun.</li>
        <li>Crack the lid for a few minutes once a day for fresh air, and mist if the surface looks less than glistening.</li>
      </ol>

      <h2>Light and conditions</h2>
      <p>Give it bright, indirect light, not blazing sun, on a timer for ten to twelve hours a day. Keep the temperature moderate, roughly 18 to 24 degrees; warm speeds growth but too warm with high humidity invites mould. Aim for humidity above 80 per cent, which a closed box with a little standing water holds easily. A hygrometer takes the guesswork out.</p>

      <h2>The automated version</h2>
      <p>To make it genuinely a machine rather than a box you tend, automate the three variables:</p>
      <ul class="loose">
        <li><strong>Light</strong> on the mains timer plug, ten to twelve hours.</li>
        <li><strong>Humidity</strong> from an ultrasonic fogger sitting in the reservoir, run in short bursts on a cheap cycle timer (a couple of minutes per hour is plenty); it also tops the air up as water evaporates.</li>
        <li><strong>Air exchange</strong> from a small USB fan on its own timer, run briefly a few times a day to clear stale, mould-friendly air. A couple of small vent holes let it breathe.</li>
      </ul>
      <p>That is as far as most people need to go. If you like a project, the fogger and fan are easy to drive from a microcontroller with a temperature and humidity sensor, but honest truth, two timer plugs and a fan do the same job for less fuss.</p>

      <h2>Running it and harvesting</h2>
      <p>The enemies are mould and scale, and both have easy answers: keep the air moving a little, and use rainwater or RO, not hard tap. Pull out any fuzzy patch the moment you see it and air the box for a day. Top up the reservoir as it drops. In a few weeks the moss carpets the platform; lift the mats, trim what you want for the tank, and leave a portion behind to reseed the box. Run like that, it is a perpetual moss supply, and far more than one tank needs, which makes it the friendliest thing to trade with other fishkeepers. See <a href="propagating-aquarium-moss.html">how to propagate aquarium moss</a> for the underlying method and <a href="aquarium-moss.html">aquarium mosses</a> for the species.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-for-shrimp"] = dict(
    title="How moss benefits Caridina and Neocaridina shrimp",
    description="Why moss is the best plant for a dwarf shrimp tank: biofilm grazing, cover and moulting safety, shrimplet survival, and what it offers Neocaridina and Caridina, plus shrimp-safe cautions.",
    active="guides",
    hero="dicranum.jpg",
    blurb="Biofilm, cover, and far higher baby survival: why moss is the one plant a cherry or crystal shrimp tank should have.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Ask experienced shrimp keepers for the one plant to put in a tank and most will say moss. For both Neocaridina, the cherry shrimp and their colour forms, and the fussier Caridina such as crystal reds and Taiwan bees, a clump of moss does more good than almost anything else you can add.</p>

      <h2>It grows their food</h2>
      <p>Dwarf shrimp graze biofilm, the living film of bacteria, algae and microbes that coats every surface, more or less constantly. Moss has an enormous surface area for its size, all of it fine, sheltered and slow-flowing, which makes it a biofilm factory. A shrimp tank with plenty of moss is a tank where the shrimp are never short of something to pick at, and you will see them working through it all day.</p>

      <h2>Cover, and safe moulting</h2>
      <p>Shrimp are prey animals and feel it. Dense moss gives them somewhere to retreat, which lowers stress and brings them out into the open more, not less, once they trust the tank. It matters most just after a moult, when a shrimp is soft and defenceless for a few hours; moss to hide in during that window reduces losses, whether the threat is a tankmate or just a nervous shrimp.</p>

      <h2>It is what saves the babies</h2>
      <p>This is the big one for breeding. Newly hatched shrimplets are tiny, weak grazers that cannot travel far for food or escape open water. A thick moss tangle gives them both: endless biofilm and microfauna to eat right where they sit, and dense cover from anything that might pick them off. The single biggest jump most keepers see in shrimplet survival comes from adding moss. If you want a colony to take off, moss is not optional.</p>

      <h2>Neocaridina and Caridina</h2>
      <p>Both benefit equally from the food, cover and breeding support; the difference is the water around the moss, not the moss itself. Neocaridina are hardy and tolerate a wide, harder, more neutral-to-alkaline range, which is why they are the beginner's shrimp. Caridina want soft, acidic water, usually over an active buffering substrate, and are less forgiving. Moss is happy across that whole span, so it suits either; set the water for your shrimp and the moss will cope.</p>

      <h2>Which moss</h2>
      <p>Java moss is the usual first choice: hardy, dense, biofilm-rich and nearly impossible to kill. Christmas, weeping and flame moss work just as well and look tidier. Whichever you pick, let it grow into a generous tangle rather than a neat sprig; for the shrimp, more moss is simply more food and more safety. See <a href="aquarium-moss.html">aquarium mosses</a> and <a href="propagating-aquarium-moss.html">how to propagate it</a>.</p>

      <h2>Shrimp-safe cautions</h2>
      <p>Shrimp, and Caridina especially, are extremely sensitive to <strong>copper</strong>, so never add moss that has been treated with anything, and be wary of plant fertilisers and snail treatments that contain it. Bought moss can also carry pesticide residue that is lethal to inverts, or hitchhikers like planaria, hydra and dragonfly larvae, so quarantine and rinse new moss, or buy from a shrimp keeper, before it goes in with a colony. Given that, moss is as close to a free win as a shrimp tank has.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-in-vivariums"] = dict(
    title="Moss in a bioactive vivarium",
    description="Using live moss in a bioactive vivarium for dart frogs, geckos and invertebrates: the drainage and substrate layers, the cleanup crew of springtails and isopods, which mosses actually survive, the lighting and humidity they need, and why so many attempts fail.",
    active="guides",
    hero="dicranum.jpg",
    blurb="Live moss in a dart-frog or gecko vivarium: the layers, the cleanup crew, which mosses survive, and why many fail.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A bioactive vivarium, a planted, self-cleaning enclosure for dart frogs, geckos, mantids or other small humid-loving animals, is one of the few indoor settings where moss can genuinely thrive, because it provides the warmth, light and constant humidity moss wants. Get the conditions right and a moss carpet becomes the living floor of a little rainforest; get them wrong and it browns like any houseplant. Here is how to give it a real chance.</p>

      <h2>What "bioactive" means</h2>
      <p>A bioactive setup is built to run as a tiny ecosystem rather than a box you scrub out. A population of small invertebrates lives in the substrate and eats animal waste, mould and dead plant matter, breaking it down on the spot so the enclosure cleans itself. Live plants, including moss, take up the resulting nutrients and keep the air and surfaces healthy. Done well, it is low-maintenance and far better for the animals than a sterile tank.</p>

      <h2>The layers</h2>
      <p>A vivarium is built up in layers, and moss sits on top of all of them:</p>
      <ul class="loose">
        <li><strong>Drainage layer</strong>: clay pebbles or a purpose-made false bottom at the base, so excess water collects below the roots rather than waterlogging everything.</li>
        <li><strong>Barrier</strong>: a mesh or fabric layer to keep the substrate from washing down into the drainage.</li>
        <li><strong>Substrate</strong>: a moisture-holding, free-draining mix, typically coir, orchid bark, sphagnum and leaf compost, deep enough for plant roots and the cleanup crew.</li>
        <li><strong>Leaf litter</strong>: a scatter of dried leaves on top, which feeds the invertebrates and shelters them, and sets off the moss nicely.</li>
      </ul>

      <h2>The cleanup crew</h2>
      <p>The engine of the whole thing is the cleanup crew: springtails and isopods (woodlice), seeded into the substrate where they multiply and quietly consume waste and mould. They are harmless to the animals and to the moss, and a healthy population is what keeps mould off a humid, warm enclosure. Add them early and let them establish before the main animal goes in.</p>

      <h2>Which mosses survive, and the honest failure rate</h2>
      <p>This is where people are caught out: a lot of moss put into vivariums slowly dies, because even a humid tank is not the cool, shaded wild. The species that cope best are the resilient cushion and carpet mosses, and several so-called vivarium mosses are sold specifically because they tolerate the warmth. Java moss, normally an aquarium plant, also does well grown emersed in a humid viv. Be ready to lose some, reseed from what thrives, and favour fragments grown on in place over big transplanted sheets, which tend to brown from the middle. See <a href="best-moss-for-terrariums.html">the best mosses for a terrarium</a> for the cushion-versus-carpet split, which applies here too.</p>

      <h2>Light, humidity and airflow</h2>
      <p>Moss wants bright but indirect light, so the plant lighting that suits most vivarium foliage suits it, kept off a harsh direct beam. Humidity should be high and steady, which a planted, misted enclosure with a glass top holds easily, but it must be paired with a little airflow: a stagnant, soaking box grows mould faster than the cleanup crew can eat it. Most keepers run gentle ventilation and mist on a schedule, by hand or with an automatic mister, to keep the surface damp without drowning it.</p>

      <h2>Establishing it</h2>
      <p>Press moss fragments firmly onto the substrate and hardscape so they make contact, mist daily, and give it weeks rather than days. A dry-start approach works beautifully here: grow the moss in under glass with the cleanup crew before introducing the animal, so the floor is established and the system is already cycling. Patience at this stage pays off in a carpet that then looks after itself for years.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["dry-start-method"] = dict(
    title="The dry start method for moss and carpets",
    description="The aquascaping dry start method explained in full: growing moss and carpeting plants emersed in a sealed, misted tank before flooding it, why it works, how to set it up, the week-by-week timeline, when and how to flood, and the trade-offs against planting straight into water.",
    active="guides",
    hero="dicranum.jpg",
    blurb="Grow a dense moss carpet emersed before you flood the tank. The full aquascaping method, timeline and trade-offs.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">The dry start method, or DSM, is an aquascaping technique for establishing a thick, even carpet of moss or foreground plants before the tank ever holds water. You plant into damp hardscape, seal the tank to trap humidity, grow everything emersed for a few weeks, and only then flood it. It takes patience up front and repays it with a dense, algae-free carpet that would be much harder to grow underwater from the start.</p>

      <h2>Why it works</h2>
      <p>Many carpeting plants and mosses actually grow faster out of the water than in it, given saturated air, because carbon dioxide is freely available from the atmosphere rather than limited as it is when dissolved. Just as importantly, while the tank is drained there is no water column for algae to bloom in, so the young plants get a clear run to establish without competition. By the time you flood, the carpet is rooted, dense and able to hold its own.</p>

      <h2>Setting it up</h2>
      <p>Lay your substrate and hardscape and shape the scape as you want it. Plant moss as a thin scatter of fragments pressed firmly onto the wood, rock or soil, and tuck carpeting plants in small, well-spaced clumps. Mist everything thoroughly with dechlorinated or RO water until the surface glistens and a shallow film sits in the low points, but do not flood. Then seal the top with cling film or glass to hold near-total humidity, and light the tank on a normal photoperiod, around eight to ten hours.</p>

      <h2>The waiting weeks</h2>
      <p>For the next few weeks the work is light: keep the surface damp by misting if it dries, lift the cover briefly every day or two for fresh air to stave off mould, and watch for growth. You will see fine new shoots and spreading first, then thickening. Pull out any fuzzy mould promptly and air the tank more if it appears. Most scapes need around four to six weeks emersed, sometimes longer for a really dense carpet; rushing it is the usual mistake.</p>

      <h2>When and how to flood</h2>
      <p>Flood once the carpet has knitted together and is gripping the surface, not before. Add water slowly and gently, ideally pouring onto a plate or bag laid on the substrate so you do not blast the new growth loose. Expect a short adjustment as the plants switch from emersed to submerged growth, during which a little melt-back is normal, and run good flow and your normal maintenance from day one to keep early algae down.</p>

      <h2>The trade-offs</h2>
      <p>The DSM gives a denser, more even, more securely attached carpet with far less early algae than planting straight into water, and it is gentle on the wallet because nothing is lost to a tank that has not cycled. Against that, it is slow, it ties the tank up for weeks before any fish go in, and not every plant takes the transition to submerged life equally well. For moss specifically it works very well, and it pairs naturally with the bulk-growing ideas in <a href="propagating-aquarium-moss.html">how to propagate aquarium moss</a> and the rig in <a href="moss-propagation-machine.html">the propagation box</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["acrocarpous-vs-pleurocarpous"] = dict(
    title="Acrocarpous and pleurocarpous mosses",
    description="The two main growth forms of moss explained: acrocarpous, upright and cushion-forming, versus pleurocarpous, creeping, branching and carpet-forming, how to tell them apart by their capsules and branching, and why the difference matters for lawns, walls, terrariums and bonsai.",
    active="guides",
    hero="hypnum.jpg",
    blurb="Cushion-forming or carpet-forming? The two growth forms of moss, how to tell them apart, and why it matters.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Once you start looking at mosses closely, they sort into two broad camps, and learning the difference is one of the most useful things a beginner can do. It explains why some mosses make tight domes and others spread in flat carpets, and it quietly decides which moss is right for a lawn, a wall, a terrarium or a bonsai.</p>

      <h2>The two forms</h2>
      <p>The two camps are the acrocarpous mosses and the pleurocarpous mosses. Acrocarps grow upright in tufts and cushions, with stems that mostly stand on end and grow from the tip. Pleurocarps creep and trail, with much-branched stems that spread sideways into mats and wefts. The cushiony bun moss on top of a wall is a classic acrocarp; the flat, feathery plait moss trailing over a log is a classic pleurocarp.</p>

      <h2>How to tell them apart</h2>
      <p>The names come from where the spore capsules grow, and that is the surest test. In acrocarpous mosses the capsule forms at the very tip of the main stem, which also tends to stop that stem growing upward, so they stay compact and upright. In pleurocarpous mosses the capsules grow on short side branches along the stem, not at the tip, leaving the main stem free to keep creeping and branching. Even without capsules you can usually tell by habit: upright and tufted, or sprawling and feathery. A hand lens makes it obvious, as covered in <a href="how-to-identify-moss.html">how to identify moss</a>.</p>

      <h2>Acrocarps in practice</h2>
      <p>Because they grow as discrete upright cushions, acrocarps hold a domed shape beautifully and are slow, tidy and sculptural. They are the stars of a terrarium, where their little hills give structure, and of Japanese moss gardens, where the rolling cushion texture is the whole point. The trade-off is that they spread slowly and knit into a continuous surface reluctantly, so they are less good where you want fast, seamless cover.</p>

      <h2>Pleurocarps in practice</h2>
      <p>Pleurocarps are the carpet-makers. Their creeping, branching habit lets them knit quickly into a continuous mat, which makes them the right choice for a moss lawn, a green wall or covering ground fast. They are generally more tolerant of being walked on and handled, and they fragment and regrow readily, which is why most slurry and propagation work uses them. The trade-off is that they look like a carpet rather than a collection of jewel-like cushions.</p>

      <h2>Why it matters for your project</h2>
      <p>Match the form to the job. For a lawn, a wall or any fast continuous cover, reach for pleurocarpous carpet mosses. For a terrarium, a moss garden or anywhere you want shape and texture, choose acrocarpous cushions, or mix the two, cushions for the hills and a pleurocarp to knit the floor between them. Knowing which is which turns "buy some moss" into choosing the right tool, and it is the most practical scrap of botany the whole subject offers. See the <a href="species.html">species page</a> for common examples of each.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-ground-cover"] = dict(
    title="Moss as ground cover in a shade garden",
    description="Using moss as ground cover in shade: under trees where grass fails, on banks and slopes to hold soil, between stepping stones, and among ferns and hostas. Why it beats grass in deep shade, how to establish a large area, and how to keep it.",
    active="guides",
    hero="thuidium.jpg",
    blurb="The answer to that bare, shady patch where grass won't grow. Moss under trees, on banks, and among shade plants.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Every garden has the spot where grass gives up: the dry shade under a tree, the damp north-facing bank, the corner that never sees sun. Fighting to grow a lawn there is a losing battle. Moss is the plant that actually wants those conditions, and used as ground cover it turns the garden's problem corners into its quietest, greenest ones.</p>

      <h2>Where moss earns its place</h2>
      <p>Moss comes into its own exactly where conventional ground cover struggles: deep or dappled shade, consistent moisture, poor or compacted soil, and acidic ground. In those conditions it gives you a soft, even, evergreen surface that needs no mowing, no feeding and almost no water once established, and stays green through winter and drought when grass has gone brown and patchy. It is lower input and lower effort, not a compromise.</p>

      <h2>Under trees</h2>
      <p>The dry, root-filled, shaded ground beneath a tree is the textbook place grass fails and moss flourishes. Moss has no roots to compete with the tree, takes nothing from the soil, and copes with the shade, so it carpets the ground where nothing else will hold. Clear the failing grass and weeds, firm the surface, and establish moss as below; the result frames the tree far better than thin, struggling turf.</p>

      <h2>Banks and slopes</h2>
      <p>On a shaded bank, moss does a practical job as well as a decorative one: a knitted moss carpet holds the surface together, slows run-off and reduces the erosion that bare or sparsely grassed slopes suffer in heavy rain. Choose creeping, carpet-forming pleurocarpous mosses for this, since they knit fastest into a continuous, soil-binding mat, as explained in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>Among ferns, hostas and stone</h2>
      <p>Moss is the perfect understorey for the classic shade-garden plants. It sets off the bold leaves of hostas, the fronds of ferns and the foliage of woodland perennials, filling the ground between them with calm green instead of bare soil or bark mulch. Run it up to and between stepping stones and around the base of rocks and it ties a shady planting together into something that looks settled and whole. The Japanese tradition leans on exactly this; see <a href="japanese-moss-gardens.html">Japanese moss gardens</a>.</p>

      <h2>Establishing a large area</h2>
      <p>For anything bigger than a patch, the slurry method is the practical way in: blend moss with rainwater or buttermilk and spread or paint it over the prepared ground, or for the largest areas spray it, as in <a href="spraying-moss.html">spraying moss slurry at scale</a>. Prepare the ground first by clearing competition and firming the surface, keep it misted daily for the first few weeks while it grips, and accept that full, seamless cover takes a season or two to develop.</p>

      <h2>Keeping it</h2>
      <p>Upkeep is mostly a matter of leaves. The one thing that smothers a moss carpet is a thick layer of autumn leaf fall left to sit and rot, so sweep or gently blow leaves off through autumn. Beyond that, keep foot traffic light on young moss, top up moisture in long dry spells until it is well established, and otherwise leave it alone to thicken year on year. See the <a href="growing.html">growing guide</a> for the establishing detail.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-through-the-seasons"] = dict(
    title="Moss care through the seasons",
    description="A seasonal calendar for moss: encouraging growth in the cool damp of spring, helping it survive summer heat and drought, clearing leaves and establishing new moss in autumn, and understanding what moss does in winter.",
    active="guides",
    hero="hero.jpg",
    blurb="What moss needs in spring, summer, autumn and winter, and why the cool damp shoulders of the year do the heavy lifting.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss does not follow the garden's usual calendar. It does most of its growing when the showy plants are dormant and rests when they are at their peak, so caring for it well is mostly a matter of working with that rhythm rather than against it. Here is the year, season by season.</p>

      <h2>Spring</h2>
      <p>Spring is prime moss season. Cool, damp air and steadily lengthening days are exactly what it likes, and growth is at its fastest, so this is the best time to start new moss, whether by transplanting patches or laying down a slurry. Established moss greens up and thickens with little help. The one spring job worth noting is that birds gather moss for nests now, so expect a little pilfering from lawns and walls, and pin down freshly laid moss if they are lifting it before it has gripped.</p>

      <h2>Summer</h2>
      <p>Summer is the hard season, because heat and dry air are moss's main enemies. Established moss in deep shade usually rides it out, drying and going dormant in spells without rain and greening up again when the weather breaks, so brown summer moss is almost always just resting rather than dead. New or recently laid moss is far more vulnerable and may need watering through dry weeks, ideally with rainwater in the early morning or evening rather than the midday heat. Resist the urge to dig up a brown patch and give up on it; wait for rain.</p>

      <h2>Autumn</h2>
      <p>Autumn brings back the cool, damp conditions of spring, and with them a second flush of growth, which makes it the other good window for establishing new moss. It also brings the single most important maintenance job of the moss year: clearing fallen leaves. A thick blanket of wet leaves left over a moss carpet smothers and kills it over winter, so sweep or gently blow leaves off through the season. Do that one thing and the moss comes through fine.</p>

      <h2>Winter</h2>
      <p>Winter is moss's quiet advantage. While the rest of the garden is bare and brown, moss stays green and even keeps growing slowly in mild, damp spells, which is much of why a shaded moss surface looks good when nothing else does. It tolerates frost without harm, simply pausing and resuming. There is little to do beyond keeping heavy leaf litter and debris off it, and enjoying the fact that the greenest thing in the garden in January asked nothing of you.</p>

      <h2>The rhythm of it</h2>
      <p>The pattern underneath all this is simple: moss does its real work in the cool, damp shoulders of the year, spring and autumn, rests through summer drought, and quietly carries the green through winter. Plan your planting for the shoulders, your watering for summer, and your leaf-clearing for autumn, and the rest looks after itself. See the <a href="growing.html">growing guide</a> for the establishing basics that all of this builds on.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-as-living-mulch"] = dict(
    title="Moss as living mulch",
    description="Using moss as a living mulch in shade: how it retains moisture, suppresses weeds, cools roots and protects soil, how it differs from bark and gravel, where it works, and the catch with seedlings.",
    active="guides",
    hero="thuidium.jpg",
    blurb="It does mulch's job and never needs topping up. How moss retains moisture, smothers weeds and protects soil.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">It is a fair way to think of it. A skin of moss over the ground does much of what a layer of bark or gravel does, except that it is alive, renews itself, and looks like a small green landscape rather than a dressing. In a shady bed, moss is mulch that gardens itself.</p>

      <h2>What mulch does, and how moss matches it</h2>
      <p>Mulch earns its keep in a few plain ways, and moss covers most of them. It keeps moisture in, since a moss layer slows evaporation from the soil beneath and holds water like a sponge after rain. It suppresses weeds, because a dense carpet leaves bare ground little chance to seed. It buffers temperature, keeping roots cooler in heat and a touch more sheltered in cold. And it shields the surface from the battering of heavy rain, which on bare soil drives compaction and run-off. A bark or gravel mulch does these things passively as it sits there; moss does them while quietly growing.</p>

      <h2>Where it shines, and where it does not</h2>
      <p>The catch is the same one that governs moss everywhere: it wants shade and damp. As mulch it comes into its own in shaded borders, around the feet of ferns, hostas and woodland perennials, beneath trees and shrubs, and over the soil of containers and bonsai, where it keeps the root zone cool and finished. It is no use as mulch on a hot, sunny vegetable bed, where bark, straw or compost serve far better. So it suits the shady, ornamental parts of a garden and leaves the productive sunny ones to conventional materials.</p>

      <h2>How it differs from bark and gravel</h2>
      <p>Two differences are worth weighing. The first is feeding: a bark or compost mulch rots down over time and improves the soil, whereas moss adds very little nutrient and does not break down into the ground, so it protects the soil without enriching it. The second cuts in moss's favour: a conventional mulch needs topping up every year or two as it rots or scatters, while an established moss carpet renews itself and, if anything, thickens with age. Moss also takes nothing from the soil, having no roots to compete with the plants it surrounds.</p>

      <h2>The catch with seedlings</h2>
      <p>One genuine drawback follows from moss being such good ground cover: it is as happy to smother your seeds as the weeds you wanted gone. A dense moss layer makes a poor seedbed, and it can also hold damp against the soft stems of low plants in a wet spell. So use moss as mulch around established plants, and keep it off ground where you intend to sow or where you are raising seedlings. Treated that way, around the things already growing, it is one of the lowest-effort, longest-lasting mulches there is.</p>

      <h2>Putting it down</h2>
      <p>You establish mulch moss exactly as you would any moss: clear and firm the ground, press in transplanted patches or paint on a slurry, and keep it damp while it grips. The creeping carpet-forming kinds knit fastest into continuous cover, and the <a href="moss-ground-cover.html">ground cover guide</a> and the <a href="growing.html">growing guide</a> both cover the method in full. Once down, it asks for nothing but the autumn leaf-clearing every moss surface wants.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["marimo-moss-balls"] = dict(
    title="Marimo balls: care, and the truth about them",
    description="Marimo moss ball care and what they really are: not a moss but a rare ball-forming green alga, how to keep one healthy for decades, keeping its shape and colour, and using them with shrimp.",
    active="guides",
    hero="marimo.jpg",
    blurb="Not a moss at all, but a charming green alga. How to keep one alive for decades, and keep it round and green.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">The marimo is the friendliest oddity in the aquarium trade: a soft green velvet ball that asks almost nothing and can outlive the keeper. The first thing to know is that it is not a moss, despite the name stuck on it everywhere.</p>

      <h2>What a marimo actually is</h2>
      <p>A marimo is a green alga, <em>Aegagropila linnaei</em>, that in a few cold, clean lakes in Japan, Iceland and northern Europe grows into dense spheres rolled smooth by gentle currents. The ball is not a single organism wrapped round a core but a colony of filaments growing radially, green all the way through. Wild marimo are slow-growing and rare enough to be legally protected in their native lakes, so the ones sold are cultivated or hand-rolled from loose filaments rather than taken from the wild.</p>

      <h2>How to keep one</h2>
      <p>Marimo want the conditions of the cold lakes they come from: cool water, gentle or no flow, and modest light. They are happiest below about 22 degrees and dislike a hot, brightly lit tank, which is one of the few ways to actually harm them. Keep them in clean, cool water, give them an occasional swill in old tank water or dechlorinated water to rinse out trapped debris, and that is more or less the whole regime. Looked after, they live for decades; some kept specimens are over a century old.</p>

      <h2>Keeping it round and green</h2>
      <p>Two simple habits keep a marimo looking right. Roll it gently in your hand now and again, or rely on a little water movement to turn it, so every side gets light and it stays spherical rather than flattening where it rests. And keep it out of strong light and warmth, which bleach it pale or let it brown and fur with other algae. If a ball goes patchy, a rinse, a gentle squeeze and a spell somewhere cool and dim usually brings it back; a badly misshapen one can be rolled back into form by hand.</p>

      <h2>In the tank, and with shrimp</h2>
      <p>Marimo sit happily in a community tank and are a particular favourite in shrimp tanks, where the residents graze the biofilm off the surface and pick through the filaments for scraps. They are soft, harmless and trap no sharp edges. Because they are an alga rather than a rooted plant, you simply set them on the substrate or wedge them where you like. For the wider untangling of which aquarium "mosses" are the real thing, see <a href="aquarium-moss-real-or-not.html">which aquarium mosses are really moss</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["reindeer-moss"] = dict(
    title="Reindeer moss: the lichen everyone calls moss",
    description="Reindeer moss explained: it is a lichen, not a moss; its role in the tundra and as caribou food, the preserved dyed form used in decor and model-making, and whether it can be grown.",
    active="guides",
    hero="reindeer.jpg",
    blurb="The springy stuff in moss walls and model railways is a lichen, not a moss. What it is, and how it is used.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">The pale, springy, branching stuff sold by the bag for moss walls, floristry and model scenery goes by the name reindeer moss, and like the marimo it is misnamed. It is a lichen.</p>

      <h2>Not a moss</h2>
      <p>Reindeer moss is <em>Cladonia rangiferina</em> and its relatives, lichens rather than plants: each is a partnership between a fungus and an alga living as a single organism. That is why it feels dry, brittle and cartilaginous rather than soft and leafy, and why it is grey-white or pale green rather than the fresh green of a true moss. For how to tell the groups apart in general, see <a href="telling-moss-apart.html">moss, lichen, liverwort or algae</a>.</p>

      <h2>In the wild</h2>
      <p>In the tundra and on northern heaths it forms vast pale carpets, and it is a winter mainstay for reindeer and caribou, which dig it out from under the snow. It grows extraordinarily slowly, often only a few millimetres a year, so those carpets represent decades of growth and recover painfully slowly once grazed or stripped. That slowness matters when it is harvested commercially.</p>

      <h2>The preserved decorative form</h2>
      <p>Almost all the reindeer moss you can buy has been preserved, its structure stabilised with glycerine and usually dyed a vivid green, so it stays soft and pliable indefinitely without water or light. In that state it is the workhorse of preserved moss walls, wreaths, terrarium dressing and model railway scenery, valued for its fine springy texture. It is no longer alive and needs no care beyond keeping it out of direct sun and damp; there is more on this use in <a href="preserved-moss-wall.html">preserved moss walls</a>.</p>

      <h2>Can you grow it?</h2>
      <p>Not really, in any practical sense. Lichens this slow do not lend themselves to cultivation, and there is no quick way to raise a crop, which is exactly why the harvested wild supply raises sustainability questions. If you forage a little for a project, take sparingly and from abundant ground, knowing that what you pick took many years to grow and will take many more to return.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["bun-moss"] = dict(
    title="Bun moss (Leucobryum): the cushion moss",
    description="Bun moss or pincushion moss (Leucobryum glaucum): the pale domed cushion moss, where it grows, why it is a favourite for terrariums and moss gardens, and how to keep it.",
    active="guides",
    hero="leucobryum.jpg",
    blurb="The pale, domed cushion moss beloved of terrariums. What Leucobryum is, where it grows, and how to keep it.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">If you picture a moss as a neat green dome, you are picturing bun moss. Its rounded, pale grey-green cushions are among the most recognisable and best-loved of all mosses, and the most useful where you want shape rather than a flat carpet.</p>

      <h2>What it is</h2>
      <p>Bun moss, also called pincushion moss, is <em>Leucobryum glaucum</em> and its close relatives. The greyish, almost glaucous colour that sets it apart comes from its unusually thick leaves, built with layers of empty cells that store water and scatter light. It is a classic acrocarpous moss, growing upward in tight tufts that mound into firm, springy hemispheres rather than spreading sideways, which is covered more fully in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>Where it grows</h2>
      <p>Look for it on acid ground in shaded woodland and on heaths, where it forms discrete cushions on the floor, on rotting logs and over rocks. The cushions can grow surprisingly large and dense, and a single one detached and set down elsewhere will often carry on quite happily, which is part of its appeal to growers.</p>

      <h2>Why terrarium makers love it</h2>
      <p>Behind glass, bun moss is a star. It holds its domed shape for years where a carpet moss would simply spread flat, so it gives a terrarium hills, structure and a sense of miniature landscape. It tolerates the high humidity of a closed jar beautifully. A couple of bun cushions set as low hills with a feather moss running between them is the backbone of many a good terrarium; the species roundup is in <a href="best-moss-for-terrariums.html">the best mosses for a terrarium</a>.</p>

      <h2>Keeping it</h2>
      <p>Give bun moss what it has in the wild: shade, steady damp and acidic, low-nutrient conditions, watered with rainwater rather than hard tap. It resents lime and bright sun. It is slower to spread than the carpet mosses, so treat it as a specimen to place rather than a quick cover, and if you collect it from the wild take single small cushions from where it is plentiful rather than clearing a patch, as set out in <a href="collecting-moss.html">collecting moss responsibly</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-for-carnivorous-plants"] = dict(
    title="Moss for carnivorous plants",
    description="Using sphagnum moss for carnivorous plants: why bog moss suits sundews, pitcher plants, Venus flytraps and butterworts, live versus dried sphagnum, the strict no-minerals water rule, and potting.",
    active="guides",
    hero="sundew-sphagnum.jpg",
    blurb="Why sphagnum is the growing medium for sundews, flytraps and pitchers, and the strict water rule that goes with it.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Carnivorous plants and sphagnum moss come from the same place, the nutrient-starved acid bog, and they belong together in cultivation. If you grow sundews, pitcher plants, Venus flytraps or butterworts, sphagnum is very likely your main growing medium.</p>

      <h2>Why sphagnum suits them</h2>
      <p>Carnivorous plants catch insects precisely because their native bogs offer almost no nutrients in the soil. Pot them in ordinary rich compost and the dissolved minerals scorch their roots and kill them. Sphagnum recreates the bog instead: acidic, extremely low in nutrients, and able to hold water around the roots while still letting air in. Sundews, the temperate pitcher plants, Venus flytraps and many others grow well in it, alone or cut with lime-free horticultural sand or perlite.</p>

      <h2>Live or dried</h2>
      <p>Both have a place. Dried long-fibre sphagnum, rehydrated, makes a clean, airy potting medium and is what most growers use as the bulk. Living sphagnum grown over the surface of the pot is even better where you can get it: it keeps the conditions acid, signals the moisture level by its own health, and looks the part. Milled sphagnum, ground fine, is useful for sowing the dust-like seed of many carnivorous plants, since its mild acidity discourages the fungus that damps off seedlings. The wider uses are gathered in <a href="sphagnum-moss.html">sphagnum moss and its many uses</a>.</p>

      <h2>The water rule</h2>
      <p>This is the part that catches people out, and it is non-negotiable: water carnivorous plants and their sphagnum only with mineral-free water, meaning rainwater, distilled or reverse-osmosis. Hard tap water steadily loads the medium with the very minerals these plants evolved to do without, and it kills them slowly but surely. They also want no feeding at the roots whatsoever; they feed themselves through their traps. Most are stood in a tray of that pure water through the growing season so the sphagnum stays wet from below.</p>

      <h2>A note on peat</h2>
      <p>Traditional carnivorous-plant mixes leaned on peat, which raises the same conservation problem set out in <a href="peat-and-peat-free.html">sphagnum, peat and why peat-free matters</a>. Sustainably sourced or cultivated sphagnum, and the growing range of peat-free bog mixes, let you grow these plants well without digging up the very habitat they come from.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-and-pets"] = dict(
    title="Is moss safe for pets?",
    description="Whether moss is safe around cats, dogs, reptiles and aquarium animals: which mosses are non-toxic, the real cautions with preserved and decorative moss, and using moss safely in vivariums and tanks.",
    active="guides",
    blurb="Cats, dogs, reptiles and fish: which moss is safe, what to watch for, and the preserved-moss caution.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss turns up around a lot of animals, in vivariums, aquariums, on a houseplant the cat chews, so it is reasonable to ask whether it is safe. For living moss the short answer is reassuring; the cautions lie elsewhere.</p>

      <h2>Living moss</h2>
      <p>The true mosses are not toxic. A cat that nibbles a terrarium, a dog that noses at a mossy log, a tortoise grazing a patch, none are poisoned by the moss itself. It has no toxins to speak of and passes through as roughage. The realistic worry is not the plant but what might be on or in it: a wild-collected clump can carry slug pellets, lawn chemicals, fertiliser or parasites, so anything destined for a pet's enclosure should be cleaned, rinsed and ideally quarantined first, or bought from a supplier who grows it clean.</p>

      <h2>The preserved-moss caution</h2>
      <p>Preserved and decorative moss is a different matter. To stay soft and green it is treated with glycerine and often dyed, and those dyes and preservatives are not meant to be eaten. It is not classed as highly poisonous, but a pet that chews a preserved moss wall or a craft arrangement can get an upset stomach from the chemicals, and loose fibres are a choking and blockage risk. Keep preserved pieces out of reach of animals inclined to chew, and treat reindeer moss decorations the same way.</p>

      <h2>In vivariums and aquariums</h2>
      <p>Living moss is a positive for the animals it shares a tank or vivarium with. Dart frogs, geckos and the cleanup-crew invertebrates of a bioactive setup all benefit from the cover and humidity it provides, and aquarium fish and shrimp graze and shelter in it. The one rule that matters here is what touches the water: shrimp and other invertebrates are acutely sensitive to copper, so never introduce moss treated with any pesticide or copper-containing product, and quarantine new moss for hitchhikers. Those points are covered in <a href="moss-for-shrimp.html">moss for shrimp</a> and <a href="moss-in-vivariums.html">moss in a bioactive vivarium</a>.</p>

      <h2>The sensible line</h2>
      <p>Treat living moss as the harmless plant it is, clean anything wild before it goes near an animal, and keep dyed and preserved moss away from chewers. Do that and moss is one of the safer green things to have around pets, which is part of why it features so often in the enclosures we build for them.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-paludarium"] = dict(
    title="Moss in a paludarium",
    description="Using moss in a paludarium, the half-water half-land tank: where moss thrives on the emersed banks and hardscape, which species suit the humid air above the waterline, and how to establish and maintain it.",
    active="guides",
    hero="paludarium.jpg",
    blurb="The half-land, half-water tank is ideal moss country. Where it thrives, which species, and how to grow it in.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A paludarium, part aquarium and part terrarium, with water below and land and air above, is close to perfect moss country. The humid air over the waterline gives moss exactly the damp, sheltered conditions it craves, and the result can be a vertical green landscape running from the water up the back wall.</p>

      <h2>Where moss thrives in a paludarium</h2>
      <p>The sweet spot is the emersed zone: the banks, rocks, wood and background that sit just above the water in saturated air. There the moss stays constantly moist without being drowned, and grows lush. Moss fully underwater behaves as an aquatic plant, while moss high and dry near a vent will struggle, so the band around and above the waterline is where it does best. Many keepers run moss from a little below the surface up the hardscape, blending the aquatic and emersed forms.</p>

      <h2>Which mosses</h2>
      <p>The aquarium mosses double brilliantly here, since species like Java, Christmas and weeping moss grow happily both submerged and emersed, which suits a tank that straddles both. For the purely land portions, the resilient terrestrial cushion and carpet mosses used in vivariums also work in the high humidity. Java moss is the reliable workhorse to start with, spreading over wood and rock with little fuss.</p>

      <h2>Establishing and maintaining it</h2>
      <p>Attach moss thinly to the hardscape exactly as in an aquarium, tying or gluing a light layer over wood and rock, since a thick wad rots in the middle. Keep the emersed sections misted or within reach of the splash from a trickle or waterfall feature, which is why paludariums so often include moving water. Bright but indirect light and a humid, lidded environment do the rest. Trim to shape as it fills in, and the clippings will seed new growth wherever they land. For attaching technique and species detail see <a href="aquarium-moss.html">aquarium mosses</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["wabi-kusa"] = dict(
    title="Wabi-kusa: moss and emersed planting balls",
    description="Wabi-kusa explained: the Japanese aquascaping style of a ball or mound of substrate planted with aquatics and moss and grown emersed, how moss fits, making one, and growing it on before flooding.",
    active="guides",
    hero="dicranum.jpg",
    blurb="The aquascaping ball of emersed plants and moss. What wabi-kusa is, how moss fits, and how to grow one.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Wabi-kusa is a quietly beautiful corner of the aquascaping world: a mound or ball of substrate planted with aquatic plants and moss, grown emersed, out of the water, as a living arrangement that can sit in a shallow dish or be dropped into a tank later. Moss is one of its natural ingredients.</p>

      <h2>What it is</h2>
      <p>The name nods to the wabi-sabi aesthetic of rustic, imperfect simplicity. In practice a wabi-kusa is a free-standing ball or low mound of soil, often bound with a little mesh or simply shaped by hand, planted with a mix of aquarium plants and moss and kept in humid air rather than underwater. The plants grow in their emersed forms, flowering and spreading in ways they never do submerged, and the whole thing reads as a miniature meadow.</p>

      <h2>Where moss comes in</h2>
      <p>Moss clothes the wabi-kusa as it does any hardscape, softening the base, knitting the planting together and holding moisture at the surface. The same aquarium mosses used elsewhere, Java and its relatives, take to emersed life readily and spread over the mound. Because the arrangement lives in damp air, moss thrives on it far more easily than it would on a dry surface indoors.</p>

      <h2>Making and growing one</h2>
      <p>Shape a ball of aquatic soil, sometimes around a core to hold its form, press in your chosen plants and a thin scatter of moss fragments, and stand it in a shallow dish with a little water and under a cover or in a humid spot with good light. Mist it, crack the cover daily for air to keep mould down, and let it grow in over several weeks; the technique is the same emersed growing described in <a href="dry-start-method.html">the dry start method</a>. Kept as a display it is an arrangement in its own right; dropped into a flooded tank, it becomes an instant planted scape.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["aquarium-moss-types"] = dict(
    title="Aquarium mosses compared: Java, Christmas, flame and weeping",
    description="A comparison of the common aquarium mosses: Java, Christmas, flame, weeping, Taiwan and phoenix moss, how they differ in shape, difficulty and growth habit, and which to choose for your scape.",
    active="guides",
    hero="thuidium.jpg",
    blurb="Java, Christmas, flame, weeping and the rest, side by side. How they differ and which to pick for your tank.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Once you go looking, the aquarium trade offers a surprising spread of mosses, and they are not interchangeable. They differ in shape, speed, fuss and the look they give a scape, so it pays to know one from another before you tie it to your wood.</p>

      <h2>Java moss</h2>
      <p>The default, and rightly so. Nearly indestructible, tolerant of low light and a wide temperature range, fast to establish and forgiving of neglect. The trade-off is tidiness: left alone it grows shaggy and shapeless, so it rewards regular trimming. For a beginner, a shrimp tank or a low-tech setup, it is the obvious starting point.</p>

      <h2>Christmas and Taiwan moss</h2>
      <p>A step up in looks. Christmas moss grows in tiered, drooping fronds that genuinely resemble little fir branches, giving a denser, more deliberate texture than Java. Taiwan moss is similar, with neat layered growth. Both are a little slower and a little more demanding than Java, preferring decent light and gentle flow, and both look superb draped over wood.</p>

      <h2>Flame and weeping moss</h2>
      <p>These two earn their keep through their unusual habit. Flame moss grows upward in twisting, vertical columns that really do suggest green flames, useful for height and movement in a scape. Weeping moss does the opposite, trailing downward in soft curtains that look wonderful flowing off a branch or an overhang. Neither is difficult, though both reward stable conditions.</p>

      <h2>Phoenix moss, and choosing</h2>
      <p>Phoenix moss (a <em>Fissidens</em>) is a compact, slow, fern-like moss prized for foreground detail and for staying small and tidy. As a rough guide: pick Java for ease and shrimp, Christmas or Taiwan for a fuller draped look, flame for vertical accents, weeping for curtains, and phoenix for fine detailed work. They all attach and grow the same way, covered in <a href="aquarium-moss.html">aquarium mosses</a> and <a href="propagating-aquarium-moss.html">propagating aquarium moss</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-for-orchids"] = dict(
    title="Moss for orchids",
    description="Using sphagnum moss for orchids: why it suits epiphytes like Phalaenopsis, potting in moss versus bark, mounting orchids with a moss pad, the watering balance, and avoiding rot.",
    active="guides",
    hero="sphagnum.jpg",
    blurb="Why sphagnum suits Phalaenopsis and friends, potting and mounting with it, and the watering balance to avoid rot.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Many orchids grow in the wild as epiphytes, perched on tree branches with their roots in the air, taking water from rain and humidity rather than soil. Sphagnum moss suits that life well, which is why it is a staple of orchid growing, especially for the popular Phalaenopsis.</p>

      <h2>Why sphagnum works</h2>
      <p>Orchid roots want two things that seem to pull against each other: moisture and air. Long-fibre sphagnum delivers both, holding water while staying open and springy enough for air to reach the roots. It is also low in nutrients and gently acidic, which suits plants adapted to a sparse, airy perch rather than rich earth. Packed loosely around the roots, it keeps them evenly damp without the suffocating wetness of ordinary compost.</p>

      <h2>Moss or bark</h2>
      <p>The two common orchid media are sphagnum and bark, and the choice shapes how you water. Moss holds far more water and dries slowly, so it suits drier homes and growers who water less often, but it is less forgiving of a heavy hand. Bark drains fast and dries quickly, suiting those who tend to overwater. Many growers use moss for young plants and seedlings, which like steadier moisture, and move to bark as the plant matures.</p>

      <h2>Mounting and the watering balance</h2>
      <p>For the epiphytic look, an orchid can be mounted on a slab of cork or wood with a pad of sphagnum tucked under its roots to hold moisture; this needs frequent misting but mimics the wild beautifully. Whether mounted or potted, the key is the watering balance: sphagnum should be moist, never sodden, and should be allowed to approach dryness before rewetting. Constant saturation is the usual cause of root rot, so err towards letting it breathe between waterings, and use rainwater or low-mineral water where you can.</p>

      <h2>When to refresh it</h2>
      <p>Sphagnum breaks down in the pot over a year or two, growing dense and sour and holding too much water as it does. Repot into fresh moss when it starts to look matted and stays wet, usually every one to two years, checking the roots over as you go. The wider uses of the moss are gathered in <a href="sphagnum-moss.html">sphagnum moss and its many uses</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["fairy-gardens"] = dict(
    title="Moss fairy gardens and miniature landscapes",
    description="Making a moss fairy garden or miniature landscape: using moss as the lawn of a tiny world, choosing a container, building hills and paths, keeping it alive, and ideas for a project with children.",
    active="guides",
    hero="hero.jpg",
    blurb="Moss as the lawn of a tiny world. Building a miniature landscape or fairy garden, and keeping it green.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss is the natural turf of any miniature world. At a small scale its fine texture reads convincingly as rolling lawn, woodland floor or hillside, which is why it is the heart of fairy gardens and model landscapes alike, and a lovely project to build with children.</p>

      <h2>Moss as the lawn of a tiny world</h2>
      <p>The trick of a miniature landscape is scale, and moss gets the scale right where grass or ordinary plants would tower absurdly over a little scene. A cushion moss becomes a hill, a flat carpet moss becomes a meadow, and a fern moss becomes a stand of miniature trees. Around those, small stones turn into boulders and a saucer of water into a pond, so the moss does most of the work of suggesting a whole landscape.</p>

      <h2>Choosing the container</h2>
      <p>A shallow bowl, an old drawer, a wooden tray or a large saucer all work, and a clear glass dish or a lidded jar holds humidity best and keeps the moss greener with less effort. Whatever you use wants a little drainage material in the base if it is open, since moss dislikes standing water, and bright but indirect light. A covered container behaves like a terrarium and is the easiest to keep alive indoors.</p>

      <h2>Building the scene</h2>
      <p>Lay a thin base of free-draining substrate, then press in your moss as the ground layer, butting pieces together and using cushions for high ground and carpets for the flats. Add the features, a pebble path, a piece of bark, a small ornament or fairy door, before the moss knits in, so it settles around them naturally. Keep the planting sparse and let the moss carry the composition; an overcrowded scene loses the calm that makes these little worlds appealing.</p>

      <h2>Keeping it alive</h2>
      <p>Mist it to keep the moss damp, stand it out of direct sun, and use rainwater if your tap is hard. In an open dish it will need misting every few days; under glass it can go a fortnight or more between sprays. Treat it as you would a <a href="terrariums.html">terrarium</a>, and the green lawn of your tiny world will hold for a long time, which is part of what makes it such a rewarding thing to make with a child.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["reviving-dried-moss"] = dict(
    title="How to revive dried-out moss",
    description="Reviving dried-out or brown moss: why moss goes dormant rather than dying when it dries, how to rehydrate a brown patch, when it is genuinely dead, and reviving moss bought dried.",
    active="guides",
    blurb="Brown and crispy is usually dormant, not dead. How to bring dried moss back, and when it has really gone.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A patch of moss gone brown and crisp looks finished, and people dig it out or throw it away. Most of the time that is a mistake, because moss does not die when it dries; it shuts down and waits, and a good soaking brings it back.</p>

      <h2>Why brown moss is usually just dormant</h2>
      <p>Moss has the ability to let its water content fall to almost nothing, going dormant in a desiccated state and resuming life when moisture returns. In that state it looks dead, brown and brittle, but the cells are intact and merely paused. This is how it survives drought on a wall or a roof, and it is why a summer-scorched patch greens up again after autumn rain. The default assumption with brown moss should be that it is resting.</p>

      <h2>Bringing it back</h2>
      <p>Rehydration is simple. Give the moss a thorough wetting with rainwater or low-mineral water and keep it damp, by misting daily or, for a detached piece, by soaking it in a bowl for a quarter of an hour. Within a day or two living moss starts to swell, soften and green from the tips. Set it somewhere shaded and humid while it recovers rather than back in the sun that dried it, and be patient over a week or so; a badly desiccated cushion can be slow to wake fully.</p>

      <h2>When it really is dead</h2>
      <p>Moss does have limits. Prolonged drought, baking heat, being smothered under wet leaves until it rots, or a dose of mosskiller will genuinely kill it, and dead moss stays brown, goes slimy or simply crumbles away without ever greening after repeated wetting. If a fortnight of consistent moisture brings no flush of green anywhere in the patch, accept that it has gone and start fresh, as in the <a href="growing.html">growing guide</a>.</p>

      <h2>Reviving moss bought dried</h2>
      <p>Dried sphagnum and some dried sheet mosses sold for crafts and orchids can sometimes be coaxed back to life, since fragments may still be viable, but it is hit and miss; preserved moss, treated with glycerine, is dead for good and will never grow. If you want living moss, start with living moss or fresh fragments rather than counting on reviving a bag of the dried stuff.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["kusamono"] = dict(
    title="Kusamono: moss and accent plantings",
    description="Kusamono, the Japanese art of accent plantings displayed alongside bonsai: what they are, the place of moss, choosing plants and pots, and caring for these small seasonal arrangements.",
    active="guides",
    hero="kusamono.jpg",
    blurb="The little seasonal plantings shown beside bonsai, where moss is the finishing ground. What they are and how to grow one.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Kusamono are the small plantings of grasses, wildflowers and herbs grown and displayed in their own right, often alongside bonsai to set a season and a mood. Moss is their usual finishing ground, the green skin that ties the planting to its pot and makes it look settled and complete.</p>

      <h2>What kusamono are</h2>
      <p>The word means "grass thing", and that captures the spirit: humble, seasonal plants rather than grand specimens, arranged to evoke a particular time of year or kind of place, a damp meadow, an autumn bank, a patch of spring woodland. Shown beside a bonsai they provide context and contrast; shown alone they are a quiet art of their own. The closely related accent plantings used specifically to complement a bonsai display are sometimes called shitakusa.</p>

      <h2>The place of moss</h2>
      <p>Moss does for a kusamono what it does for a bonsai: it covers the soil, keeps it cool and damp, stops it washing out, and finishes the composition with a natural, aged look. Beyond the practical, it belongs to the aesthetic, suggesting the mossy ground these little plants would grow on in the wild. A fine, flat carpet moss over the surface, with the chosen plants rising from it, is the typical treatment.</p>

      <h2>Plants and pots</h2>
      <p>Choose modest, seasonal material: ferns, sedges, grasses, small wildflowers, miniature hostas, anything that reads as a scrap of wild ground rather than a showy garden plant. The pot matters as much as the planting, usually a small, understated, often handmade ceramic or a simple slab, chosen to suit the plant and the season rather than to dominate. Restraint is the whole point.</p>

      <h2>Care</h2>
      <p>These are small, shallow plantings, so they dry quickly and want regular watering and a position out of harsh sun, much like the moss that dresses them. Many are treated as seasonal, brought to their best for a display when their plant is at its peak and rested afterwards. Keep the moss damp with rainwater, clear debris, and divide or replant as the material grows, and a kusamono can be kept and refined for years. The moss side of it follows the same principles as <a href="bonsai-moss.html">moss for bonsai</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-biophilic-design"] = dict(
    title="Moss walls and biophilic design",
    description="Moss in biophilic design: why moss walls appear in offices and homes, the wellbeing and acoustic case, living versus preserved moss for interiors, and an honest look at the claimed benefits.",
    active="guides",
    blurb="Why moss walls turn up in offices and lobbies, the wellbeing and acoustic case, and living versus preserved.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss walls have become a fixture of offices, lobbies and smart interiors, and they sit under the banner of biophilic design, the idea that bringing nature indoors makes the spaces we live and work in healthier and more pleasant. Moss is a natural fit for the look; it helps to be clear about what it does and does not deliver.</p>

      <h2>Why moss, and the wellbeing case</h2>
      <p>Biophilic design rests on a simple, well-supported observation: people generally feel calmer, focus better and report lower stress in spaces with greenery, daylight and natural materials than in bare ones. Moss appeals to designers because it provides that green, textured, natural presence on a wall with no soil, no irrigation in the preserved form, and very little weight. A moss wall reads instantly as nature in a way a flat painted surface never will.</p>

      <h2>The acoustic angle</h2>
      <p>One benefit is more concrete than the rest. A deep, soft moss surface absorbs sound, taking the edge off the echo and chatter of hard-surfaced open-plan rooms. This acoustic softening is a genuine, measurable effect and a real part of why moss panels are specified in busy offices, quite apart from how they look.</p>

      <h2>Living or preserved indoors</h2>
      <p>Most interior moss walls are preserved rather than living, and for good reason: a heated, dry, often dimly lit office is hostile to living moss, which needs humidity and light to stay green. Preserved moss gives the look and the acoustic benefit with no upkeep, which is covered in <a href="preserved-moss-wall.html">preserved moss walls</a>. A living wall indoors is possible but demands humidity, light and tending, as set out in <a href="moss-walls.html">living moss walls</a>; one honest caveat is that a preserved wall, being no longer alive, does not purify air or do the other things a living plant might.</p>

      <h2>An honest view</h2>
      <p>Taken for what it is, a moss wall is a sound piece of biophilic design: it brings a convincing scrap of nature indoors, softens noise, and asks little. Taken as a health device or an air purifier, the claims often run ahead of the evidence, a point looked at in <a href="moss-and-air-quality.html">moss and air quality</a>. Specify it for the calm and the quiet it genuinely brings, and it earns its place on the wall.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["ageing-with-moss"] = dict(
    title="Ageing pots, stone and ornaments with moss",
    description="How to age pots, statues, stone and garden ornaments with moss for an instant weathered look: the buttermilk and moss slurry method, where it works, and how to keep the patina going.",
    active="guides",
    blurb="Give a new pot or ornament a weathered, decades-old look. The slurry method for ageing stone and terracotta.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A new terracotta pot or a freshly cast stone ornament announces its newness, all sharp edges and bright clean surfaces. A skin of moss is the quickest way to take the edge off and lend the weathered, long-settled look that otherwise takes years of weather to earn.</p>

      <h2>The slurry method</h2>
      <p>The technique is the same moss milkshake used for graffiti and walls. Blend a couple of handfuls of clean moss with enough buttermilk or natural yoghurt, thinned with water, to make a paint, then brush it over the surfaces you want aged. The dairy helps it cling and feeds the moss a little while it takes hold. Paint it into crevices, around rims and over textured areas where moss would naturally settle, rather than evenly all over, for a believable result.</p>

      <h2>What it works on</h2>
      <p>Porous, rough materials take moss best: terracotta, unglazed ceramic, natural stone, concrete and cast reconstituted stone all give the moss something to grip. Smooth, glazed or sealed surfaces are far harder, since there is nothing for the rhizoids to hold and the slurry simply slides off. Pick a piece destined for shade and damp, because the same conditions that grow moss anywhere apply here; an ornament in full sun will stay stubbornly clean.</p>

      <h2>Keeping the patina</h2>
      <p>Once painted, keep the piece in shade and mist it regularly for the first few weeks while the moss establishes, exactly as for any new moss. After that, a position that stays cool and damp will maintain the patina with little help, while a dry spell will send it dormant and dull until the moisture returns. Over a season or two the moss thickens and the piece looks as though it has stood in the garden for decades, which is the whole idea. The underlying method is set out in the <a href="spraying-moss.html">slurry and spraying guide</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["will-it-grow"] = dict(
    title="Will moss grow in my spot?",
    description="A quick interactive check: answer four questions about your spot, light, moisture, surface and foot traffic, and find out how well moss is likely to do there and which kind to use.",
    active="will-it-grow",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss lives or dies by a few simple conditions. Answer these four questions about the place you have in mind and you will get an honest sense of how it is likely to do, and which sort of moss to reach for. Nothing is sent anywhere; it all works in your browser.</p>

      <style>
        .checker label{display:block;font-weight:600;color:var(--green-deep);margin:16px 0 5px}
        .checker select{width:100%;max-width:520px;padding:10px 12px;border:1px solid var(--line);border-radius:9px;font-size:1rem;background:#fff;font-family:inherit}
        .checker button{margin-top:22px;background:var(--green);color:#fff;border:0;border-radius:999px;padding:13px 28px;font-size:1rem;font-weight:600;cursor:pointer}
        .checker button:hover{background:var(--green-deep)}
        #verdict{display:none;margin-top:28px;border:1px solid var(--line);border-radius:14px;padding:22px 24px;background:#fff}
        #verdict h2{margin:0 0 6px}
        #verdict .score{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
        #verdict ul{margin:14px 0 0;padding-left:20px}
        #verdict li{margin:0 0 10px;color:#34402f}
      </style>

      <div class="checker">
        <label for="ck-light">How much light does the spot get?</label>
        <select id="ck-light">
          <option value="2">Deep shade most of the day</option>
          <option value="1" selected>Partial or dappled shade</option>
          <option value="-2">Full sun for much of the day</option>
        </select>

        <label for="ck-moist">How damp does it stay?</label>
        <select id="ck-moist">
          <option value="2">Usually damp, slow to dry</option>
          <option value="1" selected>Average, dries between rain</option>
          <option value="-2">Dries out fast, bakes in summer</option>
        </select>

        <label for="ck-surface">What is the surface?</label>
        <select id="ck-surface">
          <option value="ground" selected>Bare soil or ground</option>
          <option value="stone">Stone, brick or concrete</option>
          <option value="paving">Joints between paving</option>
          <option value="pot">A pot, bonsai or container</option>
          <option value="wall">A wall or vertical panel</option>
        </select>

        <label for="ck-traffic">Will it be walked on?</label>
        <select id="ck-traffic">
          <option value="1">No, it is just to look at</option>
          <option value="0" selected>The odd footstep, light use</option>
          <option value="-3">Yes, regular or heavy traffic</option>
        </select>

        <button id="ck-go">Check my spot</button>
      </div>

      <div id="verdict">
        <p class="score" id="ck-band"></p>
        <h2 id="ck-head"></h2>
        <p id="ck-lead"></p>
        <ul id="ck-notes"></ul>
      </div>

      <p class="next" style="margin-top:28px">Whatever the verdict, the method is in the <a href="growing.html">growing guide</a>. For a lawn see <a href="moss-lawn.html">how to make a moss lawn</a>, and for the cushion-versus-carpet question, <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>
    </div>
  </section>

  <script>
  (function(){
    var $=function(id){return document.getElementById(id);};
    $("ck-go").addEventListener("click",function(){
      var light=parseInt($("ck-light").value,10);
      var moist=parseInt($("ck-moist").value,10);
      var traffic=parseInt($("ck-traffic").value,10);
      var surface=$("ck-surface").value;
      var score=light+moist+traffic;
      if(surface==="wall")score-=1;
      var notes=[];
      if(light<0)notes.push("Sun is the hardest thing to work around. Moss wants shade, so unless you can cast some over the spot, this is the factor most likely to defeat it.");
      if(light>1)notes.push("Deep shade is a gift here. This is exactly where grass and most plants give up and moss takes over.");
      if(moist<0)notes.push("It dries out, which moss hates. You will need to water it, ideally with rainwater, especially while it establishes, or it will sit brown and dormant.");
      if(moist>1)notes.push("Reliable damp is half the battle won.");
      if(traffic<0)notes.push("Moss will not take regular footfall or play. If the area is walked daily, set stepping stones through it and let the moss grow around them rather than under boots.");
      // surface-specific
      if(surface==="ground")notes.push("On bare ground, clear the grass and weeds, firm the surface, and press in patches or paint on a slurry. Carpet-forming mosses knit fastest.");
      if(surface==="stone")notes.push("On stone, brick or concrete the slurry method works best: blend moss with rainwater or buttermilk and paint it on in the shade.");
      if(surface==="paving")notes.push("In paving joints, leave them be and brush a little moss slurry into the gaps. The stepping-stone-in-moss look is exactly this.");
      if(surface==="pot")notes.push("For a pot, bonsai or container, a cushion moss pressed onto the firmed surface keeps its shape and looks settled.");
      if(surface==="wall")notes.push("A wall is the trickiest, needing a moisture-holding backing and patience. Worth reading the living moss walls guide before you start.");
      // recommend type
      if(surface==="pot")notes.push("Reach for a cushion (acrocarpous) moss here for shape.");
      else if(surface==="ground"||surface==="wall"||surface==="paving")notes.push("Reach for a creeping, carpet-forming (pleurocarpous) moss for continuous cover.");
      var band,head,lead;
      if(score>=3){band="Good prospects";head="This is a strong spot for moss";lead="The basics are in your favour. With a little preparation and patience, moss should establish and thicken here nicely.";}
      else if(score>=0){band="Workable";head="Workable, with some effort";lead="It can be done, but one or two conditions are against you. Address the notes below and keep your expectations to a season or two for full cover.";}
      else{band="Uphill";head="An uphill battle, honestly";lead="The conditions here lean against moss. You can try, but unless you can change the light or the moisture, it may never really take. The notes below show what would have to give.";}
      $("ck-band").textContent=band;
      $("ck-head").textContent=head;
      $("ck-lead").textContent=lead;
      var ul=$("ck-notes");ul.innerHTML="";
      notes.forEach(function(n){var li=document.createElement("li");li.textContent=n;ul.appendChild(li);});
      $("verdict").style.display="block";
      $("verdict").scrollIntoView({behavior:"smooth",block:"nearest"});
    });
  })();
  </script>
''',
)

# Guides hub: auto-built from the list below so new articles only need adding here.
PAGES["plait-moss"] = dict(
    title="Plait moss (Hypnum cupressiforme)",
    description="Plait moss or cypress-leaved feather moss (Hypnum cupressiforme): how to recognise the commonest temperate moss, where it grows, why it is the sheet moss of terrariums and walls, and how to grow it.",
    active="guides",
    hero="hypnum.jpg",
    blurb="The glossy creeping mat on every fence post and tree trunk, and the sheet moss behind countless terrariums and living walls.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Few plants are as quietly everywhere as <em>Hypnum cupressiforme</em>. Glance along a fence rail, a churchyard wall or the shaded side of an old apple tree, and the flat green mat pressed against the wood or stone is very often this single species, reckoned the commonest moss across much of the temperate world.</p>

      <h2>Recognising it</h2>
      <p>Plait moss creeps. Its shoots run along the surface and branch as they go, so it builds a flat, trailing mat rather than a standing dome. Each shoot is clothed in small curved leaves that all hook over to one side, like teeth on a comb or the foliage of a cypress, which is where the older name cypress-leaved comes from. The mat takes on a faint gloss as it dries, brighter than most mosses, and shades from fresh green in deep shade to a bronzed yellow-green out in the open. It sits squarely among the creeping, branching mosses, the group set out in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>The moss that grows almost anywhere</h2>
      <p>Tolerance is its whole trick. You will find it on bark, dead wood, fence posts, roof tiles, brick, bare rock, gravestones and packed soil, coping with sun or shade and with ground that is acid or limey, in clean country air and in town. Hardly any other moss spans so many situations, which is exactly why it turns up so reliably. Botanists have long divided it into several varieties and look-alike segregates according to the surface it grows on, so the plait moss on a tree trunk may not be quite the same plant as the one on a rock; for anyone gardening with it, though, they behave as one.</p>

      <h2>The sheet moss of terrariums and walls</h2>
      <p>When a supplier sells "sheet moss" for terrariums, floristry or a living wall, a <em>Hypnum</em> is very often what is in the bag. The flat growth lifts away in coherent sheets, drapes obediently over a curved surface and knits back down wherever it meets damp bark or soil, which makes it ideal for lining a <a href="moss-walls.html">living moss wall</a> or carpeting the floor of a glass case. That same low, even habit is why it features so heavily in the <a href="best-moss-for-terrariums.html">terrarium species roundup</a>, usually as the carpet that runs between the cushion mosses. Living or preserved, it is one of the staples of the moss trade.</p>

      <h2>Growing and keeping it</h2>
      <p>Because it asks for so little, plait moss is among the easiest mosses to establish. Lay a sheet moss-side up on firm, weeded ground, press it into close contact and keep it damp with rainwater, and it will usually take hold and start creeping outward within a season. Behind glass it revels in the steady humidity and wants only soft light and the odd misting. The conditions it dislikes are few: stagnant deep shade with no moving air, where it thins and grows leggy, and a thick sodden wad of itself, which rots from the middle as any moss eventually will. Thin it, give it a little light and air, and it largely sees to itself.</p>

      <h2>Worth learning first</h2>
      <p>For all its commonness, plait moss repays a close look. It is the species that trains you to read a surface, because once you can name it on sight you begin to notice the scarcer mosses growing in among it. Anyone learning to <a href="telling-moss-apart.html">tell mosses from their look-alikes</a> could do worse than start here, using its familiar glossy mat as the green against which everything less ordinary stands out.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["haircap-moss"] = dict(
    title="Common haircap (Polytrichum commune)",
    description="Common haircap moss (Polytrichum commune): recognising one of the world's tallest mosses, its surprising internal plumbing, where it grows on acid bog and heath, its long history of human use, and how to grow it.",
    active="guides",
    hero="polytrichum.jpg",
    blurb="One of the tallest mosses, a forest of green spires on wet acid ground, with real internal plumbing and a long human history.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Most mosses keep their heads down; the common haircap stands up. On a wet heath or the floor of a sodden wood it raises what looks like a miniature pine forest, ankle-deep and sometimes deeper, every shoot a stiff stem set with narrow dark leaves. It ranks among the tallest mosses on earth, and it is one of the more satisfying to learn by sight.</p>

      <h2>A forest in miniature</h2>
      <p><em>Polytrichum commune</em> grows as unbranched upright stems, often a hand-span high and, in a really wet bog, taller still, each one crowned in its prime by a spreading star of leaves. Run a finger along a leaf and it feels faintly rough; the upper surface carries rows of tiny green plates called lamellae, which deepen the colour and do much of the plant's photosynthesis. Dry weather folds the leaves in tight against the stem, and a shower throws them open again into that characteristic star. The English name points to the spore capsules, lifted high on reddish stalks through summer, each wearing a shaggy golden cap of hairs.</p>

      <h2>Plumbing inside the stem</h2>
      <p>What really sets the haircaps apart is hidden in the stem. A typical moss drinks over its whole surface and has next to no internal transport, but <em>Polytrichum</em> runs a central core of stretched, specialised cells, hydroids and leptoids, that carry water up and sugars down in much the way the veins of a larger plant do. That inner plumbing is a good part of why it can afford to grow so tall and stand so stiffly where flatter mosses would flop. It offers a glimpse of the very problem, lifting water against gravity, that the flowering plants would later answer on a far grander scale, which is why this humble moss turns up so often in botany classes.</p>

      <h2>Where it grows</h2>
      <p>Seek common haircap on wet, acid, peaty ground: bogs, the margins of moorland pools, damp heath and the boggy floors of acid woodland. It is a plant of the sour and the saturated, intolerant of lime, and where the ground suits it can sheet over wide stretches. On drier banks you are more likely to meet its shorter cousins, the juniper and bristly haircaps, which take more sun; true <em>commune</em> wants its feet in the wet. As an upright, dome-forming moss it is a textbook acrocarp, the contrasting habit described in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>A long record of use</h2>
      <p>Haircap has served people for centuries, which wins it a place in any account of <a href="moss-in-history.html">moss through human history</a>. The wiry, durable stems were bundled into besoms, the old twig brooms used to sweep yards and hearths. In parts of Scotland and Scandinavia the same toughness saw it twisted into ropes and woven into baskets and mats, and gathered by the sackful to stuff mattresses and pillows, where its springiness and slight water-resistance made a serviceable filling. Households on the northern moors are recorded sleeping the winter through on beds of it.</p>

      <h2>Growing it</h2>
      <p>In the garden, common haircap is less obliging than the creeping carpet mosses, since it insists on the acid, perpetually damp conditions of its native bog. Meet those, in a boggy corner, at a pond margin or in a lime-free terrarium kept good and humid, and it lends a height and forest-floor character the flat mosses cannot. Move it as intact clumps carrying their own pad of peaty substrate rather than as loose fragments, water it only with rainwater, and never lime it. Whether it will settle for you comes down almost entirely to acidity and wetness, the sort of judgement worth making before you start, as weighed up in <a href="will-it-grow.html">will moss grow where I want it?</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["broom-fork-moss"] = dict(
    title="Broom fork-moss (Dicranum scoparium)",
    description="Broom fork-moss (Dicranum scoparium): how to recognise the swept, combed cushions of one of the handsomest woodland mosses, where it grows, why terrarium and moss-garden makers prize it, and how to keep it.",
    active="guides",
    hero="dicranum.jpg",
    blurb="The combed, all-one-way cushions of a woodland favourite, much wanted for terrariums and moss gardens.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Run your eye across a patch of broom fork-moss and the whole cushion seems to lean. Every leaf curves the same way, as though a draught had passed through and swept them flat, and that combed, all-one-direction look is the surest way to know it on sight. It is among the handsomest of the woodland mosses, and one of the most asked-for by people building terrariums and moss gardens.</p>

      <h2>Recognising it</h2>
      <p><em>Dicranum scoparium</em> builds deep, rounded cushions of upright shoots, each shoot thickly clothed in long, narrow leaves that taper to a fine point. The giveaway is the set of those leaves: instead of standing out evenly all round the stem, they curve to one side in a smooth sweep, so that even on a still day under cover the cushion looks brushed by wind. The colour is a rich mid to dark green, drying a shade paler with a faint sheen, and a mature cushion is deep enough to lose a fingertip in. Its specific name, <em>scoparium</em>, means broom-like, for the way the swept shoots call to mind the worn head of a besom.</p>

      <h2>Where it grows</h2>
      <p>This is a moss of acid ground in shade. It carpets the floor of oak and birch woods, mounds over rotting logs and the swollen bases of trees, and spreads across peaty banks, heath and the tops of boulders wherever a skin of acid humus has gathered. Lime it will not tolerate, so chalk downland and mortared walls are the wrong places to look. Through the cooler temperate world it is common and widely spread, often keeping company with bun moss and the haircaps in the same sour, shaded conditions; learning the three together teaches your eye the whole acid-woodland palette.</p>

      <h2>Where the name comes from</h2>
      <p>The fork in fork-moss has nothing to do with the leaves and everything to do with the fruit. When <em>Dicranum</em> ripens its spores it raises curved capsules on tall yellow stalks, and the ring of teeth around each capsule mouth is split, or forked, at the tips. You need a lens to see it properly, but it is the feature that names the whole genus. The capsules hang nodding to one side, quietly echoing the sweep of the foliage below. One more habit is worth knowing: the shoots grow brittle when dry, and a cushion handled roughly sheds its tips, which happens to be one of the ways the moss spreads, since each snapped fragment can settle and grow into a fresh plant.</p>

      <h2>A favourite under glass and out of doors</h2>
      <p>Terrarium makers want <em>Dicranum</em> for exactly the quality that catches the eye in the wild. Set as a low mound it lends a planted jar movement and a sense of scale that flat carpet mosses never manage, and it holds its domed form for a long while in the even humidity behind glass; it features for that reason in the <a href="best-moss-for-terrariums.html">terrarium species roundup</a>. As a standing, dome-forming moss it sits firmly among the acrocarps, the upright growers set against the creeping carpets in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>. Out in a shaded moss garden it does the same work at a larger size, reading as soft green hummocks among the flatter feather mosses, and it is a staple of the Japanese gardens described in <a href="japanese-moss-gardens.html">Japanese moss gardens</a>.</p>

      <h2>Keeping it</h2>
      <p>Of the cushion mosses, broom fork-moss is one of the fussier to settle. It wants cool, humid, shaded, lime-free surroundings and dislikes both drying to a crisp and stewing in stagnant wet, so a spot with a little air movement suits it. Move it as whole cushions carrying their own pad of peaty substrate rather than as loose handfuls, press them into firm contact and water only with rainwater; hard tap water and its lime will sicken the plant. It spreads slowly, so treat each cushion as a specimen to place rather than a quick cover. Taking it from the wild deserves restraint, lifting small pieces only where it grows in plenty, along the lines set out in <a href="collecting-moss.html">collecting moss responsibly</a>. Given clean, damp air and shade, it repays the care with one of the most distinctive textures in the moss world.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["photographing-moss"] = dict(
    title="How to photograph moss",
    description="A practical guide to photographing moss close up: working with soft light and damp weather, getting down to its level, handling shallow depth of field and focus stacking, catching the capsules, and shooting well with a phone or a camera.",
    active="guides",
    blurb="Getting close to the small green world: light, angle, focus and patience, with a phone or a proper camera.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Moss repays a camera more than almost any plant its size, because most of what makes it lovely shows only up close: the capsules swaying on their stalks, the leaves lit from behind, the beads of water it carries after rain. That same closeness is the difficulty, since at this range light, focus and the faintest breath of wind all work against you. A little method beats expensive kit here.</p>

      <h2>Wait for soft light and damp air</h2>
      <p>Moss looks its best under gentle, even light, which makes an overcast day a gift rather than a disappointment. Bright sun is the thing to avoid: it burns out the pale capsules, drops hard black shadows between the shoots and drains the colour from everything. The half hour after rain is the moment to be out, when the plants are plumped up, glowing and dotted with water. Wind is the other quiet saboteur of close work, because at high magnification a shoot stirring a single millimetre turns to mush in the frame; find shelter, wait for a lull, or steady the stem with a twig held just outside the picture.</p>

      <h2>Get down to its level</h2>
      <p>The usual mistake is to photograph moss from standing height, looking down on it as a flat green smear. The picture comes alive only when the lens drops to the height of the capsules themselves, so be ready to kneel, lie down, or rest the camera straight on the ground. A phone or a camera with a screen that tilts saves your neck a good deal of strain in that position. A beanbag, or even a folded glove, props the camera at an awkward low angle more easily than a full tripod, though a tripod whose centre column swings horizontal is worth having if you photograph moss often.</p>

      <h2>Tame the shallow focus</h2>
      <p>The closer you focus, the thinner the slice of sharpness becomes, until only a sliver of a single capsule sits crisp while the rest dissolves. Switch off autofocus, which hunts hopelessly among the shoots, and set the point by hand. A smaller aperture, meaning a higher f-number, deepens the sharp zone, though stopping down too far softens the whole frame through diffraction, so there is a sweet spot to find around the middle of the range. When you want a whole forest of sporophytes sharp from front to back, focus stacking is the technique: take a run of frames shifting the focus a touch through the subject, then blend them in software. It asks for a still subject, which is one more reason to wait out the wind.</p>

      <h2>Wet it, and hunt the sporophytes</h2>
      <p>A small spray bottle of water is the most useful thing in a moss photographer's pocket. A light misting deepens the colour, coaxes open leaves that had curled shut in the dry, and strings droplets along the shoots that catch the light beautifully. The real prize is the sporophyte, the slender stalk and its capsule lifted above the cushion; these are at their most photogenic shot against a dark background or with the light coming through them from behind, so the translucent stalks seem to glow. A sharp frame of leaf and capsule is also half the work of naming a moss later, which dovetails neatly with <a href="how-to-identify-moss.html">how to identify moss</a>.</p>

      <h2>Phone or camera, it scarcely matters</h2>
      <p>A current phone takes excellent moss pictures, especially in its macro mode, and a clip-on macro lens costing a few pounds pushes it closer still; tap to set focus, lock the exposure, and brace your elbows. A system camera with a true macro lens goes further again, reaching life-size reproduction, easy focus stacking and real control over how the background melts away. Either route works. What decides the picture is the eye and the patience behind it, not the badge on the body.</p>

      <h2>Leave the patch as you found it</h2>
      <p>Working close tempts you to tidy the scene, plucking away a stray leaf or snapping off a stem that crosses the frame. Do as little of that as you can, and put nothing dead back in to fake a result. Resist trampling the surrounding cushion to reach one good capsule, since a moss bank is slow-grown and scars easily, a point the field-craft in <a href="collecting-moss.html">collecting moss responsibly</a> dwells on for good reason. The aim is to walk away with the photograph and leave the moss looking as though nobody had been there at all.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["wall-screw-moss"] = dict(
    title="Wall screw-moss (Tortula muralis)",
    description="Wall screw-moss (Tortula muralis): how to recognise the small grey-green cushions on almost every garden wall, the spiral peristome that names it, the hair-points that let it bake and revive, where it grows and how to encourage it.",
    active="guides",
    hero="wall-screw-moss.jpg",
    blurb="The little hoary cushions on every wall top and mortar joint, named for the spiral of teeth that flings out its spores.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">On almost every garden wall in the temperate world there is a moss you have walked past a thousand times without a glance. Small grey-green cushions, each no bigger than a coin, sit along the coping and in the mortar joints, looking frosted and dead in dry weather and freshening to green after rain. This is wall screw-moss, <em>Tortula muralis</em>, and learning to name it puts a face to one of the most reliable plants in any built-up place.</p>

      <h2>Recognising it</h2>
      <p>The cushions are low and neat, a centimetre or two across, packed tight with short upright shoots. Each tongue-shaped leaf finishes in a long, colourless hair-point, a fine glassy thread, and it is the massed fringe of these pale tips that lends a dry cushion its hoary, almost silvered look. Wet the moss and the leaves spread out and flush a clean mid-green; let it dry and they twist inward and the hair-points close over the top like a drawstring. From early spring it lifts slender reddish stalks, each bearing a narrow upright capsule, and on a thriving wall these are produced so freely that the whole surface seems to bristle.</p>

      <h2>The twist behind the name</h2>
      <p>The screw is hidden inside the ripe capsule and rewards a hand lens. Around the capsule mouth sits a ring of long, thread-like teeth, the peristome, and in <em>Tortula</em> these are wound into a tight spiral, coiling like the thread of a screw or a stick of barley sugar. They are hygroscopic, flexing as the air's humidity changes, so that with every swing between damp and dry the spiral works loose a few spores and lobs them clear of the parent cushion. <em>Tortula</em> means, plainly enough, "little twist". If you want to see it for yourself, the close-looking techniques in <a href="how-to-identify-moss.html">how to identify moss</a> will get you there.</p>

      <h2>Built for the wall top</h2>
      <p>A sun-baked wall top offers no soil, little shelter and long droughts broken by sudden downpours, conditions that see off most mosses. Wall screw-moss prospers there on two tricks. That glassy hair-point on every leaf acts as a tiny parasol, reflecting fierce light and slowing evaporation from the green tissue below. And in common with all mosses it can dry to a brittle crisp and simply wait, snapping back into growth within minutes of a shower, though few manage the trick after as thorough a baking as this one shrugs off. It is fond of lime too, which is why mortar, concrete and limestone suit it so well, and it shrugs off urban soot, so it greens the walls of cities where choosier mosses fail. Standing upright in compact domes, it is a textbook acrocarp, the habit set against the creeping carpet mosses in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>Where to look</h2>
      <p>The name does not mislead: walls come first. Glance along the coping of an old garden wall, the joints between bricks, the capping of a churchyard wall or the parapet of a road bridge and the grey-green cushions are very probably this. From there it strays onto pavements, the plinths of statues, gravestones, asbestos sheeting and old roof tiles, settling on any limey, stable surface out in the light. Across Europe and much further afield it ranks among the commonest mosses of pavements and masonry, often growing cheek by jowl with silvery thread-moss in the same gritty cracks, a pairing worth knowing when you start <a href="moss-in-paving.html">reading the moss in paving</a>. Damp acid woodland and bog are where it will not be; this moss belongs to bare stone and open sky.</p>

      <h2>Encouraging it, and living with it</h2>
      <p>You seldom need to plant wall screw-moss, since it finds any suitable masonry by itself given a few seasons. To hurry it onto a new wall or a concrete ornament, the slurry method serves well: blend a pinch of the moss with rainwater or buttermilk, work the paint into the joints and crevices of a shaded face, and keep it damp while it knits down. Skip the rich compost, because what it wants is the lime and grit it would meet in the wild. On sound stonework it does no harm whatever, taking nothing from the wall and only softening its lines; only where the mortar is already failing does it root into the gaps, and there its presence is a nudge to repoint rather than anything to blame. For most of us it stays what it has always been, the quiet green proof that even bare brick is never truly without life.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-green-roof"] = dict(
    title="Making a moss green roof",
    description="How to build a moss green roof on a shed, garage or bin store: why moss beats sedum in shade, the waterproofing and drainage layers beneath, establishing moss by slurry or transplant, choosing slope and aspect, and looking after it.",
    active="guides",
    blurb="Greening a shaded shed or garage where sedum sulks: the layers beneath, getting the moss to take, and keeping it.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">A green roof need not mean sedum. On a shaded shed, a north-facing garage or a bin store tucked under trees, the very damp and gloom that starve a sedum mat are what moss likes best, so a moss roof can clothe a structure that would otherwise stay bare felt. It weighs next to nothing, asks for no mowing or feeding, and once it has settled it runs itself.</p>

      <h2>Why moss suits a roof</h2>
      <p>Most off-the-shelf green roofs are planted with sedum, the low succulents that ride out the heat and glare of an exposed roof in full sun. Set that same mat in shade, beneath overhanging branches or on a slope turned away from the south, and it thins, weakens and lets weeds march in. Moss runs the opposite way. It seeks out the cool, the damp and the soft light that defeat sedum, and it carries barely any weight, which counts for a great deal on a thin shed roof that could never bear a deep planted system. Soaked right through, a skin of moss weighs a fraction of a soil-based roof and wants none of the irrigation those systems depend on.</p>

      <h2>What goes under the moss</h2>
      <p>A moss roof is still a roof, so the layers below earn their keep. Begin with a sound, fully waterproof deck; over boarding, a butyl or EPDM pond liner is the usual home-build answer, carried up under the edges so no water can creep beneath. On top of that a thin drainage course, even a sheet of dimpled plastic or a spread of coarse grit, keeps the moss from standing in trapped water, which rots it from below. Because moss roots into almost nothing, a shallow base is plenty: a centimetre or two of a lean, gritty mix, or one of the water-holding mats sold for green roofs, does far better than deep rich soil, which only feeds weeds. Finish the perimeter with a batten or upstand to stop everything sliding off, leaving gaps or a gravel margin so rain can drain away at the edge.</p>

      <h2>Getting the moss to take</h2>
      <p>Three approaches will establish it. The fastest is to lay sheets or cushions of moss lifted from elsewhere, pressing them firmly onto the damp base so they make full contact and butting the pieces tight together. For a larger or more awkward roof the slurry works better: blend moss with rainwater or buttermilk to a thin paint, spread it evenly and mist it while the fragments regenerate, much as described in <a href="spraying-moss.html">spraying moss slurry at scale</a>. You can also simply let it arrive, since a shaded, grit-topped roof in a mossy district often greens over within a couple of years if you keep it weeded and damp. Whichever you pick, moisture in the first few weeks decides the outcome, while the rhizoids are still gripping; water with rainwater through any dry spell until the moss has knitted down.</p>

      <h2>Slope, aspect and the right moss</h2>
      <p>Aspect rules everything here. A roof facing north or east, or one shaded by trees or a taller building, holds the damp and gives moss its best chance, whereas a baking south pitch in full sun will defeat it as surely as it rewards sedum. A gentle slope sheds heavy rain without letting the surface dry too fast; a flat roof wants reliable drainage so it never ponds. For the covering itself, lean on the creeping carpet mosses that knit into continuous cover and cling on a slope, the plait and feather mosses rather than the loose, tumbling cushions. The plait moss that mats over a shaded woodland boulder will happily mat over a shaded roof, and there is more on it in <a href="plait-moss.html">plait moss (Hypnum cupressiforme)</a>.</p>

      <h2>Looking after it</h2>
      <p>As roof coverings go this is about as undemanding as they come, though it is not quite a case of laying it and forgetting it. Sweep off fallen leaves in autumn before they smother and rot the moss, particularly under trees, and tug out any seedlings of grass, willowherb or birch that try to gain a foothold, since these are what eventually break a moss roof apart. Through a long summer drought the moss will brown and go dormant, which unsettles people new to it; almost always it is merely thirsty and will green up with the next steady rain, so leave it be rather than stripping it off. Keep gutters and outlets clear so water keeps moving. This is a different matter from the unwanted moss that gathers on a house's tiled roof, a nuisance dealt with in <a href="moss-on-roofs.html">moss on roofs</a>. Done with a little care, a moss roof gives you a soft green covering that cools the structure beneath and soaks up rainfall, with a patch of habitat thrown in, for very little weight and almost no work.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["tamarisk-moss"] = dict(
    title="Tamarisk moss (Thuidium tamariscinum)",
    description="Tamarisk moss or common fern moss (Thuidium tamariscinum): recognising the flat, thrice-branched fern-like fronds of one of the most graceful woodland mosses, the fuzzy paraphyllia on its stem, where it grows, and how to use and keep it.",
    active="guides",
    hero="thuidium.jpg",
    blurb="The elegant fern-frond moss of damp woodland floors, prized in moss gardens and terrariums for the movement its arching sprays bring.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Some mosses look like nothing but moss; tamarisk moss looks like a fern that has been left out in the rain and shrunk in the wash. Across the floor of a damp wood it spreads in loose green wefts, each shoot opening into a flat, branched frond no longer than a finger. At ground level it is about the most graceful thing a temperate woodland has to show.</p>

      <h2>A fern cut down to size</h2>
      <p><em>Thuidium tamariscinum</em> builds its shoots like little trees. From a dark, almost blackish creeping stem rise repeatedly divided fronds, the side branches themselves branching again and then once more, so the whole spray comes out two or three times pinnate and lies as flat as a pressed fern leaf. The colour is a deep, faintly yellowish green, and the fronds arch and overlap into a soft, springy weft instead of pressing tight to the soil. At arm's length a patch could pass for a colony of tiny bracken, and close up the likeness only sharpens, which is why the name fern moss clings to it as readily as the bookish tamarisk.</p>

      <h2>The fuzz on the stem</h2>
      <p>Lift a single shoot and run a lens along the main stem. It is clothed in a felt of minute green threads, the paraphyllia, branched filaments scattered so thickly that the stem looks faintly woolly. Few mosses carry them in such quantity, and they make a useful confirmation when a young frond has not yet opened out enough to show its full pattern. The plant fruits only now and then, raising curved capsules on long red stalks, so for most of the year the frond and the fuzz are how you will know it. Creeping and freely branching, it belongs among the pleurocarps, the trailing growers set against the upright cushion mosses in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>Where it grows</h2>
      <p>This is a plant of shade and of ground with a little body to it. It favours neutral to base-rich woodland floors, the cool, humus-rich earth under ash, hazel and oak on heavier soils, and it runs over shaded banks, the sides of ditches and the bottoms of old hedges. Where the acid-loving bun moss and broom fork-moss insist on sour peat, tamarisk moss takes a milder, even slightly limey soil quite happily, though it will have nothing to do with a baking open wall. Given the damp shade it wants, it can sheet across a wide stretch of woodland floor, threaded through the leaf litter among the flatter feather mosses.</p>

      <h2>In the moss garden and under glass</h2>
      <p>Little else brings such movement to a planting. The arching fern fronds register at a glance as a wholly different texture from the flat carpets and tight domes around them, so a drift of tamarisk moss lends a moss garden or a shaded border the air of a miniature woodland floor; it is a mainstay of the plantings described in <a href="japanese-moss-gardens.html">Japanese moss gardens</a> and a rewarding choice where you want living <a href="moss-ground-cover.html">ground cover</a> with genuine character. Behind glass it plays the part of the fern in a terrarium, set as a tall accent above lower mosses, so long as the case stays cool, humid and out of direct sun. In a hot, dry room it soon looks tired and thin.</p>

      <h2>Keeping it</h2>
      <p>Patience suits this moss better than fussing. Give it steady shade, humid air and soil that never bakes, water it with rainwater, and leave it largely to itself once it has knitted down. It travels best as whole wefts carrying a little of their own leaf-mould rather than as pulled-apart strands, laid on firm damp ground and pressed gently so the undersides make contact. It settles more slowly than the toughest carpet mosses and dislikes both drought and stagnant wet, so a shaded spot with a breath of moving air goes a long way. Should you gather it from the wild, take small pieces only where it grows in plenty and leave any thin or struggling patch alone, in the spirit set out under <a href="collecting-moss.html">collecting moss responsibly</a>.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["silvery-thread-moss"] = dict(
    title="Silvery thread-moss (Bryum argenteum)",
    description="Silvery thread-moss (Bryum argenteum): the metallic silver-green moss of pavements, gutters and city roofs, where its sheen comes from, why it is one of the most widespread plants on earth, how it spreads without spores, and living with it.",
    active="guides",
    hero="silvery-thread-moss.jpg",
    blurb="The metallic silver cushions in every pavement crack and gutter: a true city moss, and one of the most widespread plants on the planet.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">There is a moss that lives where almost nothing green has any business growing, in the crack of a city pavement, along a clogged gutter, on a flat roof baking in the sun. It gives itself away by a metallic shimmer that no other common moss quite manages. Silvery thread-moss, <em>Bryum argenteum</em>, ranks among the most widespread plants on earth, and once its sheen is in your eye you will catch it on half the pavements you walk.</p>

      <h2>Where the silver comes from</h2>
      <p>The shimmer is a trick of the leaves. Each tiny shoot is packed with leaves that overlap closely all the way up, so the shoot stays smooth and rounded like a green catkin or a short length of plaited cord, a shape botanists call julaceous. The upper half of every leaf carries no chlorophyll and stays colourless and translucent, and it is the massed gleam of those pale tips over the green beneath that turns a dry cushion the soft silver-grey behind the name. A shower greens it again as the leaves drink; let it dry and the silver creeps back. The shoots are short, a centimetre at most, mounded into low, neat turf wherever a film of grit has lodged. Upright and tuft-forming, it counts as an acrocarp, the habit explained in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>.</p>

      <h2>A moss of the city</h2>
      <p>Other mosses put up with towns; this one seems to relish them. It does best on the hard, hot, disturbed surfaces that see off nearly everything else: the mortar at the foot of a wall, the silt in a paving joint, the gravel of a flat roof, the dust along a kerb. Part of the secret is a hunger for nitrogen, since it grows lushest where bird droppings, dog urine or plain street grime enrich the ground, so a colony will often mark the spot beneath a favourite perch or beside a much-used corner. It shrugs off trampling, drought, road salt and the heavy metals of traffic, and is studied as a quiet gauge of urban pollution for exactly that toughness. Well beyond the city it reaches almost anywhere wind and people can carry it, from Antarctic gravel to high on the world's mountains, which puts it among the small handful of truly cosmopolitan mosses.</p>

      <h2>How it gets everywhere</h2>
      <p>Spores barely account for its success. In many districts it seldom bothers to fruit, though where it does it hangs reddish, drooping capsules on short stalks. Its real means of travel is breakage. The brittle shoots part at a touch, and each loose scrap can root and grow afresh, so a fragment caught on a shoe sole or a bicycle tyre is ferried off to found a fresh colony streets away. Many shoots also pinch off minute green pellets, gemmae, that achieve the same thing in miniature. Between the two it spreads without ever waiting on a partner or a ripe capsule, which goes most of the way to explaining how one small moss came to circle the globe.</p>

      <h2>Living with it</h2>
      <p>On a path or a drive a haze of silver moss does no harm worth the name, binding a little grit and softening the bare stone underfoot; where it makes a paving joint slippery after rain a stiff brush lifts it easily, the mild end of the methods gathered under <a href="removing-moss.html">removing moss</a>. Should you want to encourage it instead, you need do very little, for a shaded, gritty, faintly grimy surface left undisturbed tends to grow its own crop within a season or two. It keeps regular company with wall screw-moss in the same gritty cracks, the two of them the staple greenery of paved places and well worth learning side by side once you begin <a href="moss-in-paving.html">reading the moss in paving</a>. To pin a name on it among its neighbours, the close-looking habits in <a href="how-to-identify-moss.html">how to identify moss</a> will settle most doubts, because that silver catkin shoot, once properly seen, is hard to take for anything else.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["willow-moss"] = dict(
    title="Willow moss (Fontinalis antipyretica)",
    description="Willow moss or greater water-moss (Fontinalis antipyretica): how to recognise the keeled, three-ranked dark streamers of a true native aquatic moss, where it grows in clean cold rivers, the curious name that means against fire, its use in ponds and coldwater tanks, and how to keep it.",
    active="guides",
    hero="fontinalis.jpg",
    blurb="A true native of cold clean rivers, streaming out in the current like dark green hair. The aquatic moss for ponds and coldwater tanks.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Most of the mosses people keep underwater came from warm tropical streams and reached the hobby through the aquarium trade. Willow moss did neither. It is a true native of cold rivers across Europe and North America, a coarse dark plant that streams out in the current like green hair, and for anyone with a wildlife pond or a coldwater tank it is the natural moss to grow.</p>

      <h2>Recognising it</h2>
      <p><em>Fontinalis antipyretica</em> grows as long, branching strands, a hand's length or a good deal more, anchored at one end to stone or wood and trailing free for the rest. The leaves give it away. Set in three ranks along the stem, each is folded sharply down its midline into a keel, so a shoot held up to the light looks distinctly three-sided rather than round or flat. The colour runs from deep olive to a near-blackish green, darker than any tropical moss, and lifted out of water the whole plant collapses into limp, slippery ropes. Returned to the water it recovers at once, fanning out wherever the flow carries it.</p>

      <h2>Where it grows</h2>
      <p>This is a plant of moving, well-oxygenated, cool water. Look for it in clean streams and rivers, draped over submerged boulders and fallen branches, below the spill of weirs and along stony lake shores where the waves keep the water stirred. It puts up with a fair spread of conditions but draws the line at warmth and stagnation, so a sun-baked, sluggish pond in high summer is the one place it sulks. Since it fixes itself by tough anchoring threads rather than true roots and feeds straight from the water around it, the quality of that water counts for more than whatever it happens to sit on.</p>

      <h2>A name that means against fire</h2>
      <p>The species name puzzles everyone who meets it. <em>Antipyretica</em> is built from the Greek for "against fire", and the reason traces back to Linnaeus, who recorded that people in northern Sweden packed the dried moss into the gap between a chimney and the timber wall of a house. Rammed in thick, it was thought to lessen the chance of the wall taking light, a humble bit of fireproofing from an age before mineral wool. Whether it answered as well as hoped is hard to judge now, yet the name has held for two and a half centuries, a small fossil of old country practice carried along in the Latin.</p>

      <h2>In ponds and coldwater tanks</h2>
      <p>Willow moss suits the very setting that defeats the warm-water mosses. In a wildlife pond it oxygenates the water, shelters tadpoles and the larvae of dragonflies and caddis, and gives newts a place to fold their eggs; few submerged plants do as much for so little fuss. Under glass it belongs in coldwater and native setups, among white cloud minnows, sticklebacks or a temperate shrimp, rather than the heated tropical tanks where Java moss reigns. Wedge or tie a strand against rock or bogwood and it takes hold of its own accord in time. Tropical keepers who try it usually watch it melt away in the heat, which is partly why the warm-tank species are gathered separately in <a href="aquarium-moss-types.html">the aquarium mosses compared</a>.</p>

      <h2>What a healthy stand tells you</h2>
      <p>Because willow moss absorbs everything across its surface, it takes up dissolved metals and pollutants and locks them away in its tissue. Freshwater ecologists turn this to use, lowering bags of the moss into rivers and later measuring what has gathered inside, a cheap living gauge of how clean a watercourse runs. For the pond keeper the reading goes the other way: a thriving stand is fair evidence that the water is cool, clean and well aired. That same knack for harbouring small creatures puts it among the more rewarding mosses for a wildlife garden, a thread picked up in <a href="moss-and-wildlife.html">moss and wildlife</a>.</p>

      <h2>Keeping it</h2>
      <p>Cool water, a little movement and modest light are about all it asks. A pump, a filter return or the trickle off a small waterfall supplies the flow it prefers; still water it accepts only while the temperature stays down. Growth is unhurried, so put aside any hope of the quick sprawl a tropical moss gives, and thin it by pulling surplus strands once it crowds its neighbours. Should you lift a piece from a wild river, take a small fragment from where it grows thickly and leave the rest to close over, the same restraint laid out in <a href="collecting-moss.html">collecting moss responsibly</a>. Settled and content, it wants next to nothing and quietly does a great deal.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-in-floristry"] = dict(
    title="Moss in floristry: wreaths and arrangements",
    description="How florists use moss: the trade names and what they really mean, fresh versus dried versus preserved moss, mossing a wreath frame, moss as the hidden mechanic of an arrangement, sourcing it responsibly, and keeping it green.",
    active="guides",
    blurb="The quiet green material behind a wreath or a basket. The florist's mosses, what their muddled names mean, and how they are worked.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Long before moss became a houseplant in a jar, it was a florist's staple: the quiet green material that lines a basket, hides the mechanics of an arrangement and forms the body of a wreath. Step into almost any flower shop and there is moss somewhere, usually under another name and often doing the work nobody is meant to notice.</p>

      <h2>The florist's mosses, and their muddled names</h2>
      <p>Trade names for moss are gloriously unreliable. "Flat moss" or "sheet moss" is generally a genuine moss, frequently a <em>Hypnum</em>, sold in peeled-up sheets for covering surfaces. "Mood moss" tends to mean the rounded cushions of <em>Leucobryum</em> or <em>Dicranum</em>, wanted for their domed shape. Past those, the labels start to deceive. Reindeer moss is a lichen, the springy <em>Cladonia</em> dyed and preserved; Spanish moss is no moss at all but an air plant, a cousin of the pineapple; and the "Irish moss" of a garden centre may turn out to be a small flowering ground-cover. Sphagnum, the bog moss, keeps its own name and a set of uses all its own. Knowing what actually sits in the bag is worth the trouble, since care and conscience differ wildly between a plant, a lichen and a bromeliad; the wider muddle of mistaken identity is unpicked in <a href="telling-moss-apart.html">moss, lichen, liverwort or algae</a>.</p>

      <h2>Fresh, dried or preserved</h2>
      <p>Floristry draws on moss in three states. Fresh moss is living and soft, lifted not long ago and still green, used where it will be on show for a short spell and can be kept damp. Air-dried moss has merely been left to harden; it pales and turns crisp, useful as hidden packing where looks do not signify. Preserved moss has been steeped in glycerine and commonly dyed, which holds it pliable and vividly green for years with neither water nor light. Which to reach for follows from the job: fresh moss where it will be seen and watered, dried moss for bulk out of sight, preserved moss for anything that has to stay green on its own. That same preserved material filling a florist's order also makes the indoor panels covered in <a href="preserved-moss-wall.html">preserved moss walls</a>.</p>

      <h2>The wreath, mossed from the frame out</h2>
      <p>A classic wreath begins with moss. The maker binds a wire ring tightly with handfuls of damp sphagnum or carpet moss, winding round and round with reel wire until it forms a firm, even green doughnut. That mossed base does double duty: it gives a surface to pin foliage and flowers into, and, kept damp, it works as a reservoir that holds cut stems alive far longer than bare wire could. Funeral and Christmas wreaths are still built this way, and the technique, called mossing, ranks among the oldest in the florist's craft. A well-mossed frame is what separates a wreath that lasts a few days from one that lasts a month.</p>

      <h2>The hidden mechanic of an arrangement</h2>
      <p>Most of the moss in floristry is never meant to catch the eye. A pad of it laid over wet floral foam disguises the green brick and slows it drying out. Sheet moss lines the open sides of a wire basket or a hanging container so compost stays put and the rim reads soft rather than mechanical. Tucked round the base of a planted bowl it covers bare earth and lends an instant air of something woodland and settled. The same trick of binding a rootball in moss and twine, carried further, becomes the Japanese craft of <a href="kokedama.html">kokedama</a>.</p>

      <h2>Sourcing it with a clear conscience</h2>
      <p>Where the moss has come from deserves a thought, because much of it is gathered wild and not all that gathering is gentle. Commercial sheet moss is often stripped in quantity from forest floors, while the sphagnum behind so many wreaths is bound up with the draining of peat bogs, ground that takes thousands of years to build and locks away great quantities of carbon. Choosing preserved or cultivated moss eases the pressure, as does keeping a mossed wreath frame from one season to the next instead of starting fresh each winter. Anyone gathering their own should do so sparingly and from where moss grows in plenty, by the field manners set out in <a href="collecting-moss.html">collecting moss responsibly</a>.</p>

      <h2>Keeping it green</h2>
      <p>Fresh moss in an arrangement stays green only while it stays damp and clear of fierce light. A wreath hung outdoors in cool, humid weather can hold its colour for weeks; the same wreath above a warm radiator browns within days. An occasional light misting revives it much as it does a moss garden, and a wreath base will take a whole soak in the sink to recharge. When at last it fades, fresh moss composts away cleanly, among the gentler ends any floral material can come to.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["springy-turf-moss"] = dict(
    title="Springy turf-moss (Rhytidiadelphus squarrosus)",
    description="Springy turf-moss (Rhytidiadelphus squarrosus): how to recognise the coarse, star-shaped moss that invades lawns, where it grows, why damp shaded turf suits it so well, and how to fight it or make a lawn of it.",
    active="guides",
    hero="rhytidiadelphus.jpg",
    blurb="The loose, spongy, star-shaped moss that thickens in tired lawns. The one most gardeners meet first, and the one that makes a fine moss lawn.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Kneel to pull a soft, spongy handful from a tired lawn and this is very often the moss you are holding. Springy turf-moss is the bryophyte most gardeners meet before any other, the loose green stuffing that gathers in damp, shaded grass until the turf gives like a mattress underfoot.</p>

      <h2>Knowing it on sight</h2>
      <p>The look is shaggy and star-like. Stout shoots, tinged red or orange-brown along the stem, carry small leaves that bend sharply outward and back, standing away from the stem at almost a right angle so that each shoot bristles like a little bottlebrush. That spreading set of the leaves gives the plant its scientific name, <em>squarrosus</em> meaning turned back at the tip, and it is the surest field mark. The shoots branch loosely rather than in the neat herringbone of the true feather mosses, building a coarse, open, decidedly untidy mat that springs back when you press it. Colour runs from yellow-green to a tired olive depending on light and season.</p>

      <h2>Where it turns up</h2>
      <p>Grassland is its home ground. You meet it through lawns and playing fields, in old meadows and on grassy banks, along woodland rides, in churchyards and across the damp hollows of dune systems, right across the cooler temperate world. Unlike many mosses it tolerates a degree of nourishment and will sit happily in grass that has been fed, favouring ground that is neutral to mildly acid and, above all, reliably moist. Light it is easy about, taking open sun where the ground stays damp and shade just as readily.</p>

      <h2>The lawn invader</h2>
      <p>No other moss is so tied to lawns, and the reason is that springy turf-moss flourishes in precisely the conditions that leave grass weak. Shade beneath trees and walls, soil packed hard underfoot, a surface that stays sodden, mowing too close and a hungry, sour root-run all thin the sward and open gaps, and this moss moves straight into them. So a lawn turning spongy with it is really reporting on its own ground, a point worked through in <a href="lawn.html">moss in the lawn</a>. Blacken it with iron sulphate, as the boxed lawn treatments do, and it darkens within days, yet it returns the moment the underlying damp and shade reassert themselves, which is why <a href="removing-moss.html">removing moss</a> for good means changing the conditions and not merely the moss.</p>

      <h2>From nuisance to lawn</h2>
      <p>The same vigour that frustrates the lawn-keeper makes this one of the better mosses to grow on purpose. Because it creeps and branches into continuous, walkable cover rather than sitting in slow tight domes, it knits into a soft green sheet that takes light foot traffic, stays green through winter and drought, and never needs a mower. Where grass has long given up under a tree, letting the turf-moss take the whole patch is frequently the easier and the handsomer choice, and it is one of the carpet-formers leaned on in <a href="moss-lawn.html">how to make a moss lawn</a>. A springy turf-moss lawn asks chiefly that you keep autumn leaves swept off it.</p>

      <h2>Working with it or against it</h2>
      <p>Whichever side you take, it helps to know what kind of moss you are dealing with. Springy turf-moss is a creeping, branching pleurocarp, the sprawling habit set against the upright cushions in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>, and that spreading growth is exactly why it covers ground so well and why it shrugs off half-hearted raking. To favour the grass, lift the shade, ease the compaction, raise the mower and feed; to favour the moss, do the opposite and simply let the damp shade have its way. Either path works, so long as you commit to one.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["common-pincushion-moss"] = dict(
    title="Common pincushion (Grimmia pulvinata)",
    description="Common pincushion or grey-cushioned grimmia (Grimmia pulvinata): recognising the hoary grey domes on sunny walls and gravestones, its curiously buried capsules, how it endures drought, and how to tell it from wall screw-moss.",
    active="guides",
    hero="grimmia.jpg",
    blurb="The hoary grey-green domes, frosted with white hair-points, that stud sunny wall tops and gravestones. A moss built for sun and drought.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">On the baked top of a wall or the shoulder of an old gravestone, where most mosses dare not grow, you find tight grey domes that look as though they have been dusted with frost. That hoary cushion is common pincushion, a moss that has made its living in the one place the soft green carpets cannot follow: bare stone in full sun.</p>

      <h2>Recognising it</h2>
      <p>Look first for a neat, rounded cushion, seldom wider than a coin, packed tight enough to shed water. Its colour is a dull grey-green, and the grey is the point: each leaf ends in a long, clear, glassy hair, and the massed hair-points frost the whole dome so it reads silver from a pace away. Run a dry fingertip over it and it feels harsh and bristly. The cushions sit so firmly to the stone that you can rock one with a fingernail and feel it resist, anchored by a felt of rhizoids into every pore of the surface.</p>

      <h2>The capsules that hide</h2>
      <p>Catch it in fruit and naming it becomes almost certain. Where most mosses hoist their spore capsules proudly clear of the leaves on straight stalks, <em>Grimmia pulvinata</em> does the reverse: its stalk curves over like a shepherd's crook so that the ripening capsule is drawn back down and tucked into the cushion, half buried among the hairs. Part the hair-points and the little egg-shaped capsules lie there on their arched stalks, a quirk so reliable that it alone settles the identification. As the capsule dries and the spores ripen the stalk slowly straightens and lifts it clear again to scatter.</p>

      <h2>A moss for sun and stone</h2>
      <p>This is a plant of hard, sunlit surfaces. It colonises the mortared tops of walls, concrete, asphalt-capped posts, tombstones, limestone and other base-rich rock, generally where there is a little lime and plenty of light, conditions that would scorch a woodland moss to dust. It belongs to the small band of urban mosses that thrive on the built environment, keeping company with the <a href="wall-screw-moss.html">wall screw-moss</a> of mortar joints and the <a href="silvery-thread-moss.html">silvery thread-moss</a> of pavement cracks. In town it is genuinely everywhere, though so dry and grey that most people walk past it without a glance.</p>

      <h2>How it survives the drought</h2>
      <p>Living on sun-baked stone means coping with long spells without water, and the cushion is built for exactly that. Drawn together into a dome, the shoots shade one another and cut the surface left open to drying wind. The glassy hair-points work two ways at once, scattering fierce sunlight away from the living tissue below and snagging dew and mist so that droplets run down into the cushion. When the last of the water has gone the plant simply shuts down, greying and brittle, then revives within minutes of a shower, a feat of desiccation tolerance common to the mosses and explored in <a href="reviving-dried-moss.html">reviving dried-out moss</a>.</p>

      <h2>Telling it apart, and leaving it be</h2>
      <p>The moss most often confused with it is wall screw-moss, which shares the wall top and the hair-points but grows greener, in looser tufts, and stands its capsules upright on straight stalks rather than burying them. The buried, arch-stalked capsule settles the question every time. As a tight, upright, dome-forming moss the common pincushion sits among the acrocarps, the cushion-builders contrasted with the creepers in <a href="acrocarpous-vs-pleurocarpous.html">acrocarpous and pleurocarpous mosses</a>. There is little point trying to cultivate it, since it wants a baking exposure no terrarium or garden bed can offer, but it rewards a closer look on any walk through a churchyard, where a hand lens turns those frosted grey domes into one of the small marvels of the masonry.</p>

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

GUIDES_ORDER = [
    "preserved-moss-wall", "moss-lawn", "moss-ground-cover", "moss-as-living-mulch",
    "ageing-with-moss", "bun-moss", "plait-moss", "haircap-moss", "broom-fork-moss",
    "springy-turf-moss", "wall-screw-moss", "common-pincushion-moss", "tamarisk-moss",
    "silvery-thread-moss", "willow-moss",
    "moss-in-floristry",
    "moss-for-carnivorous-plants", "moss-for-orchids",
    "marimo-moss-balls", "reindeer-moss", "fairy-gardens", "moss-biophilic-design",
    "moss-and-pets", "reviving-dried-moss", "kusamono",
    "removing-moss",
    "moss-on-roofs", "moss-green-roof", "moss-in-paving", "watering-moss", "moss-through-the-seasons",
    "moss-pole", "spraying-moss", "sphagnum-moss", "aquarium-moss",
    "aquarium-moss-real-or-not", "propagating-aquarium-moss",
    "moss-propagation-machine", "moss-for-shrimp", "dry-start-method",
    "moss-in-vivariums", "best-moss-for-terrariums", "moss-indoors",
    "moss-terrarium-troubleshooting", "how-to-identify-moss",
    "acrocarpous-vs-pleurocarpous", "telling-moss-apart", "collecting-moss",
    "photographing-moss",
    "growing-moss-from-spores", "how-fast-does-moss-grow", "peat-and-peat-free",
    "moss-and-wildlife", "life-in-moss", "moss-and-air-quality",
    "moss-in-history", "moss-myths",
]


def _guide_tile(slug):
    p = PAGES[slug]
    return (f'        <a class="tile" href="{slug}.html"><h3>{html.escape(p["title"])}</h3>'
            f'<p>{html.escape(p.get("blurb", p["description"]))}</p></a>')


PAGES["guides"] = dict(
    title="Guides",
    description="Practical moss guides: making a moss lawn, preserved and living moss walls, moss poles, aquarium mosses, removing moss, telling moss from its lookalikes, and more.",
    active="guides",
    body='''
  <section class="section">
    <div class="wrap">
      <p class="lede">Practical, single-topic guides. New ones are added regularly; the <a href="projects.html">projects</a> have their own section.</p>
      <div class="grid-cards">
''' + "\n".join(_guide_tile(s) for s in GUIDES_ORDER) + '''
      </div>
    </div>
  </section>
''',
)


def _credit_row(c):
    fn, desc, author, lic = c
    return (f'        <tr><td><img src="assets/{fn}" alt="" loading="lazy" width="90" height="60" '
            f'style="object-fit:cover;border-radius:6px;display:block"></td>'
            f'<td>{html.escape(desc)}</td><td>{html.escape(author)}</td><td>{html.escape(lic)}</td></tr>')


PAGES["credits"] = dict(
    title="Image credits",
    description="Image credits for Mossbank: every photograph on the site with its source, author and licence. All images come from Wikimedia Commons and are served from this site, not hotlinked.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">Every photograph on Mossbank comes from Wikimedia Commons, is used under the licence shown, and is hosted here rather than linked from elsewhere. The site's own text is licensed CC BY-NC-SA 4.0; the images keep their individual licences listed below.</p>
      <table class="credits-table">
        <thead><tr><th></th><th>Image</th><th>Author</th><th>Licence</th></tr></thead>
        <tbody>
''' + "\n".join(_credit_row(c) for c in IMAGE_CREDITS) + '''
        </tbody>
      </table>
      <p>Licence terms: <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>, <a href="https://creativecommons.org/licenses/by/2.0/">CC BY 2.0</a>, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA 2.0</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>
    </div>
  </section>
''',
)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    written = []
    for slug, p in PAGES.items():
        out = page(slug, p["title"], p["description"], p["body"], p.get("hero"), p.get("active"))
        path = os.path.join(here, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        written.append(f"{slug}.html")

    # sitemap.xml
    today = date.today().isoformat()
    urls = []
    for slug in PAGES:
        loc = BASE + ("/" if slug == "index" else f"/{slug}.html")
        prio = "1.0" if slug == "index" else ("0.8" if slug in ("guides", "projects", "species", "growing") else "0.6")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # robots.txt
    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(here, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # IndexNow key file (Bing/Yandex instant indexing)
    with open(os.path.join(here, INDEXNOW_KEY + ".txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    print("built:", len(written), "pages + sitemap.xml + robots.txt + IndexNow key")


if __name__ == "__main__":
    main()
