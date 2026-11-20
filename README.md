# Hop To It Events — Website

National food & drink experiential events company website.

## Quick Deploy to GitHub Pages

### 1. Create the repo

Go to [github.com/new](https://github.com/new) and create a new repository called `hop-to-it-events` (or whatever you'd like — e.g., `hoptoit.events`). Keep it public if you want free GitHub Pages hosting.

### 2. Push the code

```bash
cd hop-to-it-events
git init
git add .
git commit -m "Initial site launch"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hop-to-it-events.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repo on GitHub
2. **Settings** → **Pages** (left sidebar)
3. Under "Source," select **Deploy from a branch**
4. Branch: **main**, Folder: **/ (root)**
5. Click **Save**

Your site will be live at `https://YOUR_USERNAME.github.io/hop-to-it-events/` within a minute or two.

### 4. Connect your custom domain (optional)

If you want this on `hoptoit.events` or `www.hoptoit.events`:

1. In your repo: **Settings** → **Pages** → **Custom domain** → enter `www.hoptoit.events` → Save
2. At your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.), add these DNS records:

**For apex domain (`hoptoit.events`):**
| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

**For www subdomain:**
| Type | Name | Value |
|------|------|-------|
| CNAME | www | YOUR_USERNAME.github.io |

3. Back in GitHub Pages settings, check **Enforce HTTPS** once DNS propagates (can take up to 24 hours)

## Alternative: Netlify (drag & drop)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag the entire `hop-to-it-events` folder onto the page
3. Site is live instantly with a random URL
4. Add your custom domain in Netlify's domain settings

## File Structure

Every page lives in its own folder so URLs are short: `/corporate-event-planning/`,
`/locations/los-angeles/food-truck-catering/`.

```
index.html                     Home
services/                      All services hub
<15 service folders>/          corporate-event-planning, food-truck-catering, brand-activations, ...
locations/                     Locations hub
locations/los-angeles/         LA hub + 8 LA service pages
events/  about/  plan-your-event/
404.html  donutfestvegas.html  privacypolicy.html
sitemap.xml  robots.txt  llms.txt   Search + AI crawler files (generated)
assets/                        styles.css, main.js, self-hosted fonts, logo, share image
_src/                          Build script and page copy (not served)
CNAME
```

## Editing

1. Copy lives in `_src/services.py` (service pages), `_src/locations.py` (city pages) and
   `_src/build.py` (home, events, about, plan, shared header/footer).
2. Run `python3 _src/build.py` from the repo root. It regenerates every page, the sitemap,
   robots.txt and llms.txt. (`--preview` builds links that work when opening files directly.)
3. Commit everything, including the generated files.

City page rollout: `PUBLISH_PHASE` in `_src/locations.py` controls which LA pages are indexed.
Phase 2 pages are built but marked noindex and left out of the sitemap until you raise it to 2.

Photos: `_src/photos.py` is the shot list. Save each photo as `assets/photos/<key>.jpg`
(e.g. `chef-battle-teams.jpg`) and rebuild; one photo fills every slot that shares it. Edit the
alt text there to describe the real photo.

Social links: add URLs to `SOCIAL` in `_src/build.py`; they appear in the footer and structured data.

## Leads (Google Sheet + email alert)

Both forms (Plan Your Event and the food truck quote) can save every submission to a Google
Sheet and email you each lead. Until it's set up, forms open the visitor's email app instead.

1. Create a new Google Sheet (e.g. "Hop To It Leads") in the Google account that should own the leads.
2. Extensions > Apps Script. Delete the sample code, paste in `_src/google-apps-script.gs`, save.
   Change `NOTIFY` at the top if alerts should go somewhere other than matt@hoptoit.events.
3. Pick `testLead` in the function menu and click Run. Approve the permissions (Google warns it's
   "unverified" because it's your own script: Advanced > Go to project). Check that a "Leads" tab
   appeared with a test row and that the alert email arrived.
4. Deploy > New deployment > type Web app. Execute as: Me. Who has access: Anyone. Deploy and
   copy the Web app URL (ends in /exec).
5. Paste it into `LEADS_URL` in `_src/build.py`, run `python3 _src/build.py`, and push.

Lead emails use the visitor's address as Reply-To, so you can hit Reply to answer them. A hidden
spam-trap field drops most bot submissions. If you edit the script later, use Deploy > Manage
deployments > Edit > New version so the URL stays the same.

## After launch

- Submit `https://hoptoit.events/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- Validate a few pages at https://search.google.com/test/rich-results.

## Contact

hello@hoptoit.events
