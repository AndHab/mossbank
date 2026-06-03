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


def page(slug, title, description, body, hero=None):
    full_title = title if slug == "index" else f"{title} | {SITE}"
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
        {nav_html(slug)}
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
      <p class="copy">&copy; <span>{YEAR}</span> Mossbank. Text free to share under CC BY-SA 4.0. Analytics are cookieless and self-hosted; see the <a href="privacy.html">privacy page</a>.</p>
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
      <p class="lede">Once you can keep moss alive, it becomes a material. A few of the things people make with it.</p>
      <div class="grid-cards">
        <div class="tile static">
          <h3>Kokedama</h3>
          <p>The Japanese "moss ball": a plant whose roots are wrapped in a ball of soil, bound with moss and string, and hung or set on a dish. Soak to water. A good first project, and forgiving.</p>
        </div>
        <div class="tile static">
          <h3>Terrariums</h3>
          <p>A closed glass jar makes a near-perfect moss home: high humidity, soft light, no drying wind. Cushion mosses such as <em>Leucobryum</em> and broom fork-moss keep their shape beautifully under glass for years.</p>
        </div>
        <div class="tile static">
          <h3>Bonsai carpets</h3>
          <p>A skin of moss over the soil of a bonsai keeps the roots cool and damp, stops the surface washing out, and finishes the tree with a settled, aged look. Choose a fine, flat-growing species.</p>
        </div>
        <div class="tile static">
          <h3>Living walls</h3>
          <p>Moss panels green a shaded wall with almost no weight and no irrigation once established, soaking up rain and cooling the surface. They want shade and occasional misting, not full sun.</p>
        </div>
        <div class="tile static">
          <h3>Japanese moss gardens</h3>
          <p>The moss gardens of Kyoto treat the carpet itself as the planting, with stone, water and a few trees for structure. The effect is quiet and deep, and it rewards the same shade-and-damp conditions described in the growing guide.</p>
        </div>
        <div class="tile static">
          <h3>Moss graffiti</h3>
          <p>Paint a moss slurry onto a shaded wall in a shape or letters, keep it misted, and it grows into a living design. Lovely on your own damp north wall; ask first on anyone else's.</p>
        </div>
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
      <p>The photographs are from Wikimedia Commons under their respective licences, credited in the footer. The words are free to share under CC BY-SA 4.0. Corrections and additions are welcome.</p>
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


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    written = []
    for slug, p in PAGES.items():
        out = page(slug, p["title"], p["description"], p["body"], p.get("hero"))
        path = os.path.join(here, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        written.append(f"{slug}.html")
    print("built:", ", ".join(written))


if __name__ == "__main__":
    main()
