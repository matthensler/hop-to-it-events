"""Builds city hubs and city-service pages from the market research in citydata.py.

Copy is composed from each city's own districts, industries, venues, climate,
transport and coverage areas, with a different angle for each service, so a
page reads as written for that market and that service. Hop To It-specific
claims only appear when the market data says they're true (worked / note).
"""
import zlib

import citydata2  # noqa: F401  (registers batch 2)
from citydata import C as DATA


def lst(items, n=None):
    items = list(items)[:n] if n else list(items)
    if len(items) <= 1:
        return "".join(items)
    sep = ", and " if any(" and " in i for i in items) else " and "
    return ", ".join(items[:-1]) + sep + items[-1]


def pick(slug, key, options):
    return options[zlib.crc32((slug + key).encode()) % len(options)]


def cap(s):
    return s[:1].upper() + s[1:]


PROOF_WORKED = "We've produced events in {short}"
PROOF_NEW = "Experience From Producing Our Own Events"


def proof(d):
    if d["worked"]:
        extra = (" " + d["note"]) if d["note"] else ""
        return (PROOF_WORKED.format(short=d["short"]),
                f"{d['city']} is one of the 30+ markets where Hop To It Events has planned and produced events.{extra} "
                f"We bring that experience, plus our signature-event background with Chef Battle and Donut Fest, to every {d['short']} event.")
    return (PROOF_NEW,
            "Hop To It Events creates and runs its own signature events, including Chef Battle and Donut Fest, in markets across the country. "
            f"We bring that production experience to events in {d['city']}, working with local vendors and venues selected for your event.")


def faq_lead(d, what="events"):
    return (f"How far ahead should we plan {what} in {d['city']}?",
            f"For most {what if what.endswith('s') else what.removeprefix('a ').removeprefix('an ') + 's'}, start 6–10 weeks out, and earlier for dates in {d['outdoor']}, which is peak outdoor season in {d['city']}. "
            + (f"Dates that overlap with major events at {d['convention']} or big local weekends fill venues and hotels quickly. " if d["convention"] else
               "Popular weekends and holiday dates fill quickly. ")
            + "Share your target date and we'll tell you what's realistic.")


def faq_quote(d, svc):
    return (f"What affects the cost of {svc} in {d['city']}?",
            f"Guest count, date and season, venue type, food and beverage, entertainment and staffing are the biggest drivers. "
            f"In {d['city']}, peak dates in {d['outdoor']} and venue choice ({lst(d['venues'][:2]).lower()} versus a space you already have) "
            "move budgets the most. Try the calculator on this page for a quick range, then request a proposal.")


def areas_flat(d, n=8):
    out = []
    for _, towns in d["areas"]:
        out += towns
    return out[:n]


def hub(d):
    a = areas_flat(d)
    first, last = d["areas"][0][1][0], d["areas"][-1][1][0]
    return dict(
        title=f"{d['city']} Event Planning & Production | Hop To It Events",
        meta=f"Event planning and production in {d['city']}: corporate events, team building, food truck catering, brand activations, festivals and grand openings across {d['region']}.",
        h1=pick(d["slug"], "h1", [f"{d['city']} Events. *Unforgettable Experiences.*",
                                  f"Event Planning in {d['city']}, *Done Right.*",
                                  f"Big Ideas for *{d['city']} Events.*"]),
        intro=f"{d['hook']} Hop To It Events plans and produces corporate events, team building, food truck catering, brand activations and community festivals for organizations in {lst(d['districts'], 3)}, and throughout {d['region']}.",
        cta=f"Plan Your {d['short'] if len(d['short']) < 14 else d['city']} Event", photo="City event hero",
        services_title=f"Event Planning Services in {d['city']}",
        local=(f"Planning an Event in {d['city']}",
               f"Popular venue types here include {lst(d['venues'])}. The best outdoor window is {d['outdoor']}. {d['weather']} "
               f"For {d['indoor']}, we'll steer you toward indoor or covered options. {d['transport']}"),
        proof=proof(d),
        caps=("Full-Service Event Planning & Production",
              f"For {lst(d['industries'], 3)} teams and organizations across {d['region']}, our team can coordinate strategy, venue sourcing, vendor management, "
              "catering, entertainment, photography and video, sponsorships, logistics and on-site management."),
        coverage_title=f"Areas We Serve Around {d['city']}",
        coverage_intro=f"From {first} to {last}, we help organizations across {d['region']} plan events, with vendors, entertainment and production support matched to the location.",
        areas=d["areas"],
        closing=f"Let's Create Something Unforgettable in {d['city']}",
        faqs=[(f"Does Hop To It Events plan events in {d['city']}?",
               f"Yes. We plan corporate events, team building, food truck catering, brand activations, festivals and grand openings across {d['region']}, including {lst(a, 6)}."
               + ("" if d["worked"] else " Tell us your location and we'll confirm the vendors and support available for your date.")),
              (f"What kinds of venues work for events in {d['city']}?",
               f"It depends on the event and season. {cap(lst(d['venues'][:4]))} are common choices here, and for outdoor events we look at {lst(d['parks'])}. "
               f"We'll recommend venue types that fit your guest count, budget and the time of year."),
              faq_lead(d),
              (f"How does weather affect events in {d['city']}?",
               f"{d['weather']} We plan the format around the season: outdoors in {d['outdoor']}, and indoor or covered options for {d['indoor']}."),
              faq_quote(d, "events")],
    )


def svc_pages(d):
    city, short, slug = d["city"], d["short"], d["slug"]
    dist, ind, ven, parks = d["districts"], d["industries"], d["venues"], d["parks"]
    areas = areas_flat(d)
    conv = d["convention"]
    pages = []

    pages.append(dict(
        slug="corporate-events", national="corporate-event-planning", name="Corporate Event Planning",
        card=f"Company celebrations, client events and holiday parties for teams in {lst(dist, 2)}.",
        title=f"Corporate Event Planning {city} | Hop To It Events",
        meta=f"Corporate event planning in {city}: holiday parties, client events, employee celebrations and conferences for companies in {lst(dist, 2)} and across {d['region']}.",
        h1=pick(slug, "corp", [f"Corporate Events in {city} That *People Talk About.*",
                               f"{city} Corporate Events, *Planned and Produced.*",
                               f"Make Your Next {city} Company Event *Worth Showing Up For.*"]),
        intro=f"{city}'s {lst(ind, 3)} employers host everything from all-hands celebrations to client receptions. Hop To It Events plans and produces corporate events for teams in {lst(dist, 3)}, handling the concept, venue, food and beverage, entertainment and on-site management.",
        cta="Get a Corporate Event Quote", form_type="Corporate Event", photo="LA company celebration",
        cards_title="Corporate Events We Create",
        cards=[("Company Celebrations & Holiday Parties", "Milestones, year-end parties and all-hands celebrations with great food and entertainment."),
               ("Employee Appreciation Events", "Food truck lunches, office festivals and recognition events.", "employee-appreciation"),
               ("Client & Customer Events", "Receptions, networking events and VIP gatherings for clients and partners."),
               ("Company Picnics", "Outdoor celebrations with food, games and entertainment.", "company-picnics"),
               ("Corporate Team Building", "Chef Battle, Bartender Battle and interactive group experiences.", "team-building"),
               ("Conferences & Sales Meetings", "Receptions, kickoffs and programming around meetings" + (f" at {conv} and other venues." if conv else " and conferences."))],
        feature="chef_battle",
        sections=[(f"Corporate Venues Around {city}",
                   f"Companies in {lst(dist, 3)} often book {lst(ven[:3])}. We match the venue to your headcount, format and budget, or work with your office, campus or a space you already have."),
                  (f"Planning Around the {short} Calendar",
                   f"Holiday parties fill December quickly, and outdoor company events work best in {d['outdoor']}. {d['weather']} {d['transport']}"),
                  (f"Let's Plan Your {city} Corporate Event", f"Tell us what you're celebrating, how many people are coming and where around {d['region']} you'd like to host.")],
        related=["team-building", "employee-appreciation", "food-truck-catering"],
        faqs=[(f"Do you plan corporate events in {lst(dist, 2)}?",
               f"Yes. We plan corporate events across {d['region']}, including {lst(areas, 6)}, at your office, a venue we help source or an off-site location."),
               (f"What venues work for corporate events in {city}?",
                f"{cap(lst(ven[:4]))} are all popular here. The right fit depends on guest count, whether you want a seated dinner or a mingling format, and the season."),
               (f"When should we book a holiday party in {city}?",
                f"Start in late summer or early fall. December weekends and the first half of the month book first, especially at {ven[0]}. Weeknights and January celebrations are easier to secure."),
               faq_quote(d, "a corporate event")]))

    pages.append(dict(
        slug="team-building", national="corporate-team-building", name="Corporate Team Building",
        card="Chef Battle, Bartender Battle and interactive group challenges.",
        title=f"Corporate Team Building {city} | Hop To It Events",
        meta=f"Corporate team building in {city}: Chef Battle culinary competitions, Bartender Battle and group challenges for teams in {lst(dist, 2)}.",
        h1=pick(slug, "tb", [f"{city} Team Building That's Anything But *Ordinary.*",
                             f"Team Building in {city} People *Actually Enjoy.*",
                             f"Get Your {short} Team *Cooking, Competing and Connecting.*"]),
        intro=f"Give your {city} team something more memorable than another meeting. Hop To It Events runs Chef Battle culinary competitions, Bartender Battle cocktail and mocktail challenges and custom group experiences for companies across {d['region']}.",
        cta="Plan Your Team Experience", form_type="Team Building", photo="Chef Battle team cook-off",
        cards_title="Team Building Experiences",
        cards=[("Chef Battle", "Teams plan, cook and plate dishes, then compete for the judges' votes."),
               ("Bartender Battle", "A creative cocktail or mocktail competition led by a pro host."),
               ("Culinary Challenges", "Hands-on tastings and food challenges built for collaboration."),
               ("Custom Group Experiences", "Formats shaped around your goals, culture and group size.")],
        feature="chef_battle",
        sections=[("Indoor-Friendly, Any Time of Year",
                   f"{d['weather']} Chef Battle and Bartender Battle run indoors, so they work at your office, a {ven[0].rstrip('s')} or a {ven[2].rstrip('s')} any time of year."),
                  (f"On-Site or Off-Site Around {city}",
                   f"We bring the competition to offices in {lst(dist, 3)}, or run it off-site with a venue, open bar and passed apps. {d['transport']}"),
                  (f"Let's Bring Your {short} Team Together", "Tell us your participant count, preferred date, location and budget, and whether you'd like on-site or off-site.")],
        related=["corporate-events", "employee-appreciation", "company-picnics"],
        faqs=[(f"Can team building happen indoors in {city}?",
               f"Yes. Our culinary and cocktail competitions are built to run indoors, which helps from {d['indoor']}, and we can move outdoors in {d['outdoor']}."),
              (f"Can you run team building at our {city} office?",
               f"Yes. We set up at offices across {d['region']}, including {lst(areas, 5)}, as long as there's room for team stations. We'll confirm space and power needs in advance."),
              ("Can it work for large groups?", "Yes. On-site packages fit groups up to about 50, and our private-event format scales to hundreds of guests with a live pro chef competition, MC and AV."),
              ("Is there a non-alcoholic option?", "Yes. Bartender Battle runs as a mocktail competition, and Chef Battle doesn't require alcohol at all.")]))

    trucks_winter = d["indoor"] if any(m in d["indoor"] for m in ("November", "December", "October")) else ""
    pages.append(dict(
        slug="food-truck-catering", national="food-truck-catering", name="Food Truck Catering",
        card=f"Food trucks for office lunches, festivals and private events around {city}.",
        title=f"Food Truck Catering {city} | Hop To It Events",
        meta=f"Food truck catering in {city}: truck sourcing, scheduling and on-site coordination for office lunches, festivals and private events across {d['region']}.",
        h1=pick(slug, "ft", [f"{city} Food Truck Catering. *We Bring the Trucks.*",
                             f"Food Trucks for Your {city} Event, *Handled.*"]),
        intro=f"Food trucks turn a parking lot or courtyard into an event. Hop To It Events helps coordinate trucks for office lunches, employee appreciation days, festivals and private events across {d['region']}, from vendor selection to scheduling and site logistics.",
        cta="Get a Food Truck Quote", form_type="Food Truck Catering", photo="LA food truck lineup", hero_form=True,
        cards_title="Food Truck Catering for Every Occasion",
        cards=[("Corporate Lunches", f"Bring trucks to offices and campuses in {lst(dist, 2)}.", "corporate-events"),
               ("Employee Appreciation Events", "Turn an ordinary workday into a celebration.", "employee-appreciation"),
               ("Food Truck Festivals", "Multi-truck lineups for community events and public celebrations.", "festival-planning")],
        feature="menu",
        sections=[(f"Where Trucks Work in {city}",
                   f"{d['transport']} Office parks, campus lots, private lots and permitted event sites usually work best. Rules on where trucks can park and serve vary by city and property, so we review your site first."),
                  ("Planning Around the Season",
                   f"Truck events are easiest in {d['outdoor']}. {d['weather']}" + (f" From {trucks_winter}, we'll talk through tents, heaters or a covered pickup area." if trucks_winter else "")),
                  (f"Let's Feed Your {city} Crowd", "Whether you need one truck or a full lineup, tell us your date, location and guest count.")],
        related=["corporate-events", "employee-appreciation", "company-picnics"],
        faqs=[(f"Where can food trucks park for an event in {city}?",
               f"It depends on your site. Private lots, office parks and campuses around {lst(areas, 4)} are usually simplest. Street and public-space locations need city approvals, which we'll talk through."),
              (f"Do we need a permit for food trucks in {city}?",
               "Requirements vary by municipality and by whether the event is on private property or public space. We'll review what applies to your location as part of planning."),
              ("How many food trucks do we need?", "As a rule of thumb, plan about one truck per 75–100 guests for a 2-hour service window, then adjust for menu variety and timing."),
              faq_lead(d, "a food truck event")]))

    pages.append(dict(
        slug="brand-activations", national="brand-activations", name="Brand Activations & Experiential Marketing",
        card=f"Sampling, pop-ups and launches in {lst(d['dining'], 2)} and beyond.",
        title=f"Brand Activations {city} | Hop To It Events",
        meta=f"Experiential marketing and brand activations in {city}: product sampling, pop-ups, launches and festival activations in {lst(d['dining'], 2)} and across {d['region']}.",
        h1=pick(slug, "ba", [f"Make Your Brand an Experience in *{city}.*",
                             f"{city} Brand Activations That *Get People Talking.*"]),
        intro=f"From {lst(d['dining'], 2)} to event days that draw big crowds, {city} has plenty of places to put a brand in front of people. Hop To It Events helps brands plan and staff sampling programs, pop-ups, launches and festival activations across {d['region']}.",
        cta="Plan a Brand Activation", form_type="Brand Activation", photo="LA sampling pop-up",
        cards_title="Brand Experiences We Create",
        cards=[("Product Sampling", "Put products directly into consumers' hands with trained brand ambassadors."),
               ("Pop-Up Events", "Temporary branded spaces that invite people to stop and explore."),
               ("Product Launches", "Launch moments built around demos, tastings and media.", "grand-openings"),
               ("Festival Activations", "Interactive brand experiences at live events and festivals.", "festival-planning"),
               ("Trade Show Activations", "Programming that pulls traffic to your booth" + (f" at {conv}." if conv else "."))],
        brands=True,
        sections=[(f"Where to Activate in {city}",
                   f"High-foot-traffic districts like {lst(d['dining'], 3)} suit sampling and pop-ups, subject to property and city approvals. For B2B audiences, {lst(ind, 2)} events and trade shows are strong options."),
                  ("Staffing, Logistics and Season",
                   f"Outdoor activations perform best in {d['outdoor']}. {d['weather']} We handle booth setup, staffing, supplies and recap reporting."),
                  (f"Let's Bring Your Brand to Life in {city}", "Tell us what you're promoting, who you want to reach and the dates you're targeting.")],
        related=["grand-openings", "festival-planning", "corporate-events"],
        faqs=[(f"What kinds of brand activations do you run in {city}?",
               "Product sampling, pop-ups, product launches, festival activations and trade show programming, from a single staffed table to multi-day tours."),
              (f"Can you staff a sampling program in {city}?",
               f"Yes. We provide trained brand ambassadors and on-site managers, priced by days and hours on site, and can run activations around {lst(areas, 4)}."),
              ("Can my brand activate at one of your festivals?", "Our signature events, including Donut Fest and Chef Battle, offer sponsorship and activation opportunities. Ask which events are scheduled near your audience."),
              faq_lead(d, "a brand activation")]))

    pages.append(dict(
        slug="festival-planning", national="festival-event-planning", name="Festivals & Community Events",
        card="Food festivals, community celebrations and public events.",
        title=f"Festival & Community Event Planning {city} | Hop To It",
        meta=f"Festival and community event planning in {city}: food festivals, downtown celebrations and public events with vendor, sponsorship and production support.",
        h1=pick(slug, "fest", [f"Bringing {city} *Together.*", f"{city} Festivals Worth *Showing Up For.*"]),
        intro=f"We don't just plan festivals, we create our own, including Donut Fest and Chef Battle. Hop To It Events helps cities, business districts, shopping centers and organizations across {d['region']} produce food festivals and community celebrations.",
        cta="Plan a Festival", form_type="Festivals & Community", photo="LA food festival crowd",
        cards_title="Festivals & Events We Create",
        cards=[("Food & Beverage Festivals", "Restaurants, food trucks, beverage brands and culinary talent in one place."),
               ("Community Celebrations", f"Events for neighborhoods and business districts like {lst(d['dining'], 2)}."),
               ("Downtown & Shopping Center Events", "Programming that brings visitors in and keeps them around."),
               ("Culinary Competitions", "Live Chef Battle-style competitions with an audience.", "team-building"),
               ("Seasonal Festivals", f"Events built around {d['outdoor']} and local holidays.")],
        audiences=True,
        sections=[(f"Festival Season in {city}",
                   f"The prime window here is {d['outdoor']}. {d['weather']} Public events usually use {lst(parks)}, and each site comes with its own permits and approvals."),
                  ("From Concept to Crowd",
                   f"We help with concept, vendor recruitment, sponsorships, ticketing, marketing and production. {d['transport']}"),
                  (f"Let's Create Your Next {city} Festival", "Tell us about your community, location, expected attendance and goals.")],
        related=["food-truck-catering", "brand-activations", "grand-openings"],
        faqs=[(f"Who do you plan festivals for in {city}?",
               "Cities and municipalities, business districts, tourism groups, shopping centers, property managers and community organizations."),
              ("Do you handle permits for public events?",
               f"We coordinate permitting with you and the relevant agencies. Requirements differ between {city} and surrounding communities like {lst(areas[-3:], 3)}."),
              (f"What's the best time of year for a festival in {city}?",
               f"{cap(d['outdoor'])} is the strongest outdoor window. {d['weather']}"),
              faq_quote(d, "a festival")]))

    pages.append(dict(
        slug="employee-appreciation", national="employee-appreciation-events", name="Employee Appreciation Events",
        card="Food truck days, office festivals and recognition celebrations.",
        title=f"Employee Appreciation Events {city} | Hop To It",
        meta=f"Employee appreciation events in {city}: food truck days, office festivals and recognition celebrations for teams in {lst(dist, 2)}.",
        h1=pick(slug, "ea", [f"Give Your {city} Team Something to *Celebrate.*",
                             f"Employee Appreciation in {city}, *Made Easy.*"]),
        intro=f"Recognize your people with more than another catered lunch. Hop To It Events brings food trucks, office festivals, competitions and celebrations to workplaces across {d['region']}, from {dist[0]} offices to suburban campuses.",
        cta="Plan an Employee Appreciation Event", form_type="Corporate Event", photo="Office festival in a courtyard",
        cards_title="Employee Appreciation Ideas",
        cards=[("Food Truck Appreciation Days", "Bring trucks directly to the workplace.", "food-truck-catering"),
               ("Office Festivals", "Turn a parking lot, courtyard or office into a mini festival."),
               ("Employee Recognition Celebrations", "Awards, milestones and team wins."),
               ("Interactive Competitions", "Chef Battle and Bartender Battle for your team.", "team-building"),
               ("Holiday & Seasonal Celebrations", "Gatherings built around the time of year.")],
        sections=[(f"Appreciation Events for {city} Workplaces",
                   f"For offices in {lst(dist, 3)}, we plan around building rules, loading access and parking. {d['transport']}"),
                  ("Pick the Right Format for the Season",
                   f"Outdoor office festivals and truck days work best in {d['outdoor']}; for {d['indoor']}, we'll plan indoor celebrations or covered setups."),
                  (f"Let's Celebrate Your {short} Team", "Tell us about your team size, office location and what you'd like to celebrate.")],
        related=["food-truck-catering", "company-picnics", "team-building"],
        faqs=[(f"Can you host an appreciation event at our {city} office?",
               f"Yes. We bring food trucks, activities and entertainment to workplaces around {lst(areas, 5)}, based on your site and building rules."),
              ("Can we do it for multiple shifts or locations?", "Yes. We can schedule service windows for multiple shifts or set up at more than one site on the same day."),
              (f"What's a good time of year for employee appreciation in {city}?",
               f"Outdoor formats shine in {d['outdoor']}. Employee Appreciation Day in early March and the holidays are popular, and indoor formats work any time."),
              faq_quote(d, "an employee appreciation event")]))

    pages.append(dict(
        slug="company-picnics", national="company-picnics", name="Company Picnics",
        card=f"Outdoor celebrations with food, games and entertainment, best from {d['outdoor']}.",
        title=f"Company Picnic Planning {city} | Hop To It Events",
        meta=f"Company picnic planning in {city}: venues, food trucks, games and entertainment for employee and family picnics across {d['region']}.",
        h1=pick(slug, "cp", [f"{city} Company Picnics Worth *Looking Forward To.*",
                             f"Company Picnics in {city}, *Without the Stress.*"]),
        intro=f"A company picnic is one of the best ways to bring a whole team together. Hop To It Events plans picnics across {d['region']}, from venue and permits to food trucks, games, entertainment and on-site management.",
        cta="Get Started", form_type="Corporate Event", photo="Outdoor company picnic in a park",
        cards_title="Everything for a Great Company Picnic",
        cards=[("Food Trucks & Catering", "Variety for every guest, from BBQ to dessert.", "food-truck-catering"),
               ("Games & Activities", "Lawn games, competitions and activities for all ages."),
               ("Family-Friendly Experiences", "A welcoming setup for employees and their families."),
               ("Music & Entertainment", "DJs, hosts and live entertainment."),
               ("Venue & Vendor Coordination", "Sites, permits, rentals, vendors and logistics.")],
        sections=[(f"Picnic Season in {city}",
                   f"The best window is {d['outdoor']}. {d['weather']} We plan shade, tents and a backup so the date holds."),
                  ("Where to Host",
                   f"Common picnic sites around {city} include {lst(parks)}. Reserved park spaces often book months ahead, so lock in your site early."),
                  (f"Let's Plan Your {city} Company Picnic", "Tell us your headcount, whether families are invited and the part of town you'd like to host in.")],
        related=["food-truck-catering", "employee-appreciation", "team-building"],
        faqs=[(f"When should we hold a company picnic in {city}?",
               f"{cap(d['outdoor'])} is the safest window. Book reserved park space or a venue at least 2–3 months ahead for peak dates."),
              ("What if the weather doesn't cooperate?", f"{d['weather']} We plan tents, shade and a rain or heat backup as part of every outdoor event."),
              ("Can you find a park or venue for our picnic?", f"Yes. We help find sites around {lst(areas, 4)} and coordinate reservations, rentals and logistics."),
              ("Can families attend?", "Yes. We plan employee-only and family-inclusive picnics, with activities for kids and adults.")]))

    pages.append(dict(
        slug="grand-openings", national="grand-openings-product-launches", name="Grand Openings & Launches",
        card=f"Openings and launches for businesses in {lst(d['dining'], 2)} and beyond.",
        title=f"Grand Opening Event Planning {city} | Hop To It",
        meta=f"Grand opening and launch event planning in {city}: restaurant, retail and business openings, product launches and VIP events across {d['region']}.",
        h1=pick(slug, "go", [f"Make Your {city} Grand Opening a *Big Deal.*",
                             f"Open Big in *{city}.*"]),
        intro=f"Whether you're opening in {lst(d['dining'], 2)} or a suburban shopping center, the first day sets the tone. Hop To It Events plans grand openings, launch parties and VIP previews that bring customers, neighbors and media through the door.",
        cta="Plan Your Grand Opening", form_type="Grand Opening", photo="Ribbon cutting on an LA storefront",
        cards_title="Grand Openings & Launch Events",
        cards=[("Restaurant & Bar Openings", "Tastings, entertainment and opening-night celebrations."),
               ("Retail Store Openings", "Experiences that get shoppers exploring."),
               ("Product Launches", "Demos, sampling and interactive activations.", "brand-activations"),
               ("Business Grand Openings", "Celebrate with customers, employees, partners and neighbors."),
               ("VIP & Media Events", "Invitation-only previews and receptions.")],
        sections=[(f"Opening in {city}",
                   f"In busy districts like {lst(d['dining'], 3)}, sidewalk use, signage, amplified sound and food service can need approvals, so we plan those early. {d['transport']}"),
                  ("Timing Your Opening",
                   f"Outdoor elements like food trucks, sidewalk activations and live music work best in {d['outdoor']}. {d['weather']}"),
                  (f"Let's Make Your {city} Launch Unforgettable", "Tell us your business type, address, opening date, expected attendance and budget.")],
        related=["brand-activations", "festival-planning", "food-truck-catering"],
        faqs=[(f"Do you plan restaurant and retail openings in {city}?",
               f"Yes. We plan restaurant and bar openings, retail openings, business grand openings, product launches and VIP or media events across {d['region']}."),
              ("Can you add food trucks, music or sampling to our opening?", "Yes. We coordinate food trucks, entertainment, sampling and activities, subject to your site and local approvals."),
              faq_lead(d, "a grand opening")]))

    for p in pages:
        p["phase"] = 1
    return pages


def build():
    out = []
    for d in DATA:
        out.append(dict(slug=d["slug"], city=d["city"], short=d["short"], region=d["region"], state=d["state"],
                        nearby=d["nearby"], worked=d["worked"], batch=d["batch"], hub=hub(d), pages=svc_pages(d)))
    return out


CITY_PAGES = build()
