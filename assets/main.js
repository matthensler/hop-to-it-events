// Hop To It Events — shared behavior
(function () {
  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  // Event Planning mega menu
  var mega = document.querySelector('.has-mega');
  if (mega) {
    var btn = mega.querySelector('button');
    var setOpen = function (open) {
      mega.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open);
    };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!mega.classList.contains('open'));
    });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  // Tabs
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = list.querySelectorAll('[role="tab"]');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute('aria-selected', on);
          document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
        });
      });
    });
  });

  // Event brand filter
  var filters = document.querySelectorAll('.filter');
  filters.forEach(function (f) {
    f.addEventListener('click', function () {
      var cat = f.dataset.filter;
      filters.forEach(function (x) { x.setAttribute('aria-pressed', x === f); });
      document.querySelectorAll('[data-cat]').forEach(function (tile) {
        tile.hidden = cat !== 'all' && tile.dataset.cat.split(' ').indexOf(cat) === -1;
      });
    });
  });

  // Preselect event type from ?type= on the plan page
  var params = new URLSearchParams(location.search);
  var type = params.get('type');
  if (type) {
    var radio = document.querySelector('input[name="event_type"][value="' + CSS.escape(type) + '"]');
    if (radio) radio.checked = true;
  }

  // Prefill guest count and budget from the budget calculator
  function pickRange(sel, n) {
    if (!sel || !n) return;
    for (var i = 1; i < sel.options.length; i++) {
      var t = sel.options[i].text.replace(/[$,]/g, '');
      var nums = t.match(/\d+/g); if (!nums) continue;
      var lo = +nums[0], hi = nums[1] ? +nums[1] : Infinity;
      if (/^Under/.test(t)) { lo = 0; hi = +nums[0]; }
      if (/\+$/.test(t)) hi = Infinity;
      if (n >= lo && n < hi + 1) { sel.selectedIndex = i; return; }
    }
  }
  var g = +params.get('guests');
  if (g) pickRange(document.getElementById('p-guests'), g);
  var bud = (params.get('budget') || '').split('-');
  if (bud[1]) pickRange(document.getElementById('p-budget'), (+bud[0] + +bud[1]) / 2);

  // "Flexible / not sure yet" date toggle
  document.querySelectorAll('[data-flex-for]').forEach(function (box) {
    var input = document.getElementById(box.dataset.flexFor);
    box.addEventListener('change', function () {
      input.disabled = box.checked;
      if (box.checked) input.value = '';
    });
  });

  // Inquiry forms. With data-leads set (a Google Apps Script web app URL) a
  // submission is saved to the leads sheet and emailed to the team. Without it,
  // the visitor's email app opens with every answer filled in.
  document.querySelectorAll('form[data-mailto]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      form.querySelectorAll('[data-flex-for]').forEach(function (box) {
        if (box.checked) data.set(document.getElementById(box.dataset.flexFor).name, 'Flexible / not sure yet');
      });
      var note = form.querySelector('.form-note');
      var btn = form.querySelector('button[type="submit"]');
      var url = form.dataset.leads;

      if (url) {
        data.set('form', form.dataset.form || 'Website form');
        data.set('page', location.pathname);
        btn.disabled = true;
        fetch(url, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) })
          .then(function () {
            form.reset();
            note.className = 'form-note show';
            note.textContent = 'Thanks! We got your request and will be in touch soon.';
          })
          .catch(function () {
            note.className = 'form-note show err';
            note.innerHTML = 'Something went wrong. Please email us at <a href="mailto:' + form.dataset.mailto + '">' + form.dataset.mailto + '</a>.';
          })
          .then(function () { btn.disabled = false; });
        return;
      }

      var lines = [];
      form.querySelectorAll('[data-label]').forEach(function (el) {
        var val = data.get(el.getAttribute('name'));
        if (val) lines.push(el.dataset.label + ': ' + val);
      });
      var subject = form.dataset.subject || 'Event inquiry';
      if (data.get('name')) subject += ' from ' + data.get('name');
      location.href = 'mailto:' + form.dataset.mailto + '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      if (note) note.classList.add('show');
    });
  });

  // Scroll reveal
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
})();
