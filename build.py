#!/usr/bin/env python3
"""Static builder for Mossbank. No dependencies: `python3 build.py` writes the
finished HTML pages into the repo root, wrapping each page body in the shared
chrome (nav, footer, analytics). Content lives in the PAGES dict below."""

import html
from datetime import date

SITE = "Mossbank"
YEAR = date.today().year

# GoatCounter: cookieless, self-hosted. One line, every page.
ANALYTICS = (
    '<script data-goatcounter="https://stats.mossbank.de/count" '
    'async src="//stats.mossbank.de/count.js"></script>'
)

NAV = [
    ("index", "Home"),
    ("biology", "What is moss"),
    ("species", "Species"),
    ("growing", "Growing"),
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
    full_title = title if slug == "index" else f"{title} | {SITE}"
    active = active or slug
    hero_block = ""
    if hero:
        hero_block = f'''
  <header class="hero hero--page" style="background-image:linear-gradient(rgba(20,32,18,.55),rgba(20,32,18,.7)),url('assets/{hero}')">
    <div class="wrap">
      <h1>{html.escape(title)}</h1>
    </div>
  </header>'''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
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
      <p class="credits">Photographs from Wikimedia Commons under their respective licences: forest moss by W. Carter (CC0); <em>Sphagnum capillifolium</em> by Krzysztof Ziarnek, Kenraiz (CC BY-SA 4.0); <em>Hypnum cupressiforme</em> by Robert Flogaus-Faust (CC BY 4.0); <em>Dicranum scoparium</em> by Rafael Medina (CC BY 4.0); <em>Thuidium tamariscinum</em> by Michael Becker (CC BY-SA 3.0).</p>
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
      <p>When a capsule ripens it dries, opens, and releases dust-fine spores to the wind. A spore that lands somewhere damp and shaded germinates into a fine green thread, the protonema, which in turn buds into a new cushion. The cycle begins again.</p>

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
''',
)

PAGES["lawn"] = dict(
    title="Moss in the lawn: friend or weed?",
    description="Why moss takes over a lawn, what it tells you about shade, drainage and soil, how to remove it if you must, and the case for letting a moss lawn take over.",
    body='''
  <section class="section">
    <div class="wrap prose">
      <p class="lede">More people meet moss as a lawn problem than in any other way. Before you reach for the iron sulphate, it is worth understanding what the moss is telling you.</p>

      <h2>Moss is a symptom, not the disease</h2>
      <p>Grass struggles and moss moves in for clear reasons: too much shade, poor drainage, compaction, mowing too low, or thin, acidic, hungry soil. The moss is not attacking the grass. It is simply better suited to those conditions than the grass is. Kill the moss without changing the conditions and it will be back within a season.</p>

      <h2>If you want the grass back</h2>
      <p>Treat the cause. Reduce shade where you can, spike or aerate to relieve compaction, improve drainage, raise the mowing height, and feed the grass so it can compete. Scarifying, raking out the dead moss, helps in the short term, and on lawns where the issue is genuinely acidity a measured liming can shift the balance. None of it lasts without fixing the underlying shade and drainage.</p>

      <h2>The case for giving in</h2>
      <p>There is another option, and a growing number of gardeners take it: stop fighting and let the moss lawn happen. In a shaded, damp garden a moss lawn is soft underfoot, stays green through drought and winter, needs no mowing, no feeding and no watering once established, and asks only that leaves be cleared off in autumn. It is the lower-effort, lower-input, more drought-resilient surface, and in deep shade it is often the only thing that will look good at all.</p>
      <p>Put plainly: if your "moss problem" is in a spot where grass will always struggle, the moss is not the problem. It is the solution, and it arrived on its own.</p>

      <p class="next"><a href="growing.html">If you are leaning in: how to encourage a moss lawn &rarr;</a></p>
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
      <p>In a closed terrarium, very happily, because the humidity stays high. Out in a dry, centrally heated room it will not last; it needs that damp, still air.</p>
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
    hero="sphagnum.jpg",
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
      <p>At 55 to 60 per cent humidity a living wall is borderline rather than impossible. It would need a genuinely shaded position out of direct sun, a small grow light, regular misting, and hardy cushion or sheet mosses rather than bog moss. That is a real ongoing project. If you want green on the wall and your time back, preserved is the sane choice; see the <a href="moss-walls.html">living moss walls</a> guide for the other path.</p>

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

      <h2>The honest caveat</h2>
      <p>If a surface is permanently shaded and damp, moss will keep coming. At that point you are choosing between regular clearing and accepting a little green. Where it is not a safety issue, the second option is a great deal less work.</p>

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

      <p class="next"><a href="guides.html">&larr; Back to guides</a></p>
    </div>
  </section>
''',
)

PAGES["moss-pole"] = dict(
    title="Moss poles for climbing houseplants",
    description="Moss poles explained: why climbing aroids like monstera and pothos benefit, sphagnum versus coir poles, how to make and mount one, and keeping it damp so aerial roots grip.",
    active="guides",
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

# Guides hub: auto-built from the list below so new articles only need adding here.
GUIDES_ORDER = [
    "preserved-moss-wall", "moss-lawn", "removing-moss", "moss-pole",
    "spraying-moss", "aquarium-moss", "telling-moss-apart",
    "growing-moss-from-spores", "life-in-moss",
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
    print("built:", ", ".join(written))


if __name__ == "__main__":
    main()
