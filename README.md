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

```
hop-to-it-events/
├── index.html    ← Entire site (single file, no dependencies)
├── CNAME         ← Custom domain config for GitHub Pages
└── README.md     ← This file
```

## Contact

hello@hoptoit.events
