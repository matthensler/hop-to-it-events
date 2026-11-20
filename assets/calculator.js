// Event Budget Calculator. Rates live in the page's #calc-rates JSON
// (generated from CALC_RATES in _src/build.py) so they can be changed without touching this file.
(function () {
  var root = document.getElementById('calc');
  if (!root) return;
  var R = JSON.parse(document.getElementById('calc-rates').textContent);
  var $ = function (id) { return document.getElementById(id); };
  var round = function (n) { return Math.round(n / 50) * 50; };
  var money = function (n) { return '$' + round(n).toLocaleString('en-US'); };
  var range = function (l, h) { return round(l) === round(h) ? money(l) : money(l) + ' – ' + money(h); };
  var pmoney = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var prange = function (l, h) { return Math.round(l) === Math.round(h) ? pmoney(l) : pmoney(l) + ' – ' + pmoney(h); };
  var num = function (id) { return parseFloat($(id).value) || 0; };

  function sum(items, qty, factor) {
    var rows = [], lo = 0, hi = 0;
    items.forEach(function (it) {
      var box = $('c-' + it.id);
      if (!box || !box.checked) return;
      var q = qty[it.unit] !== undefined ? qty[it.unit] : 1;
      var l = it.low * q * factor, h = it.high * q * factor;
      if (it.min) { l = Math.max(l, it.min); h = Math.max(h, it.min); }
      rows.push({ label: it.label, low: l, high: h }); lo += l; hi += h;
    });
    return { rows: rows, lo: lo, hi: hi };
  }

  function interp(points, x) {
    if (x <= points[0][0]) return points[0][1];
    for (var i = 1; i < points.length; i++) {
      var a = points[i - 1], b = points[i];
      if (x <= b[0]) return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]);
    }
    var p = points[points.length - 1], q = points[points.length - 2];
    return p[1] + (p[1] - q[1]) / (p[0] - q[0]) * (x - p[0]);
  }

  function compute() {
    var type = R.types[$('c-type').value];
    var mode = type.mode || 'event';
    root.querySelectorAll('[data-show]').forEach(function (el) {
      el.hidden = el.dataset.show.split(' ').indexOf(mode) < 0;
    });

    var guests = Math.max(10, Math.min(5000, parseInt($('c-guests').value, 10) || 0));
    var hours = num('c-hours'), days = num('c-act-days'), samples = num('c-act-samples');
    var att = num('c-att'), vendors = num('c-vend');
    var rows = [], lo = 0, hi = 0, per = '', offset = '', plus = false, sizeNote = '';

    if (mode === 'package') {
      var pkg = R.packages[$('c-pkg').value];
      var tier = pkg.tiers.filter(function (t) { return t[0] === null || guests <= t[0]; })[0];
      plus = tier[0] === null;
      lo = hi = tier[1];
      rows.push({ label: pkg.label.split(' (')[0] + (plus ? ' (' + (pkg.tiers[pkg.tiers.length - 2][0]) + '+ guests)' : ' (up to ' + tier[0] + ' guests)'), low: lo, high: hi });
      per = 'About ' + pmoney(lo / guests) + ' per guest' + (plus ? ' at ' + guests + ' guests' : '');
    } else if (mode === 'activation') {
      var res = sum(R.activation_items, { day_hour: hours * days, day: days, sample: samples, flat: 1 }, 1);
      rows = res.rows; lo = res.lo; hi = res.hi;
      var core = R.activation_items.filter(function (i) { return i.core; }).map(function (i) { return i.label; });
      var el = 0, eh = 0;
      rows.forEach(function (r) { if (core.indexOf(r.label) < 0) { el += r.low; eh += r.high; } });
      if (el) {
        var ap = R.activation_planning;
        rows.push({ label: ap.label, low: el * ap.low, high: eh * ap.high });
        lo += el * ap.low; hi += eh * ap.high;
      }
      per = 'About ' + prange(lo / days, hi / days) + ' per activation day';
    } else if (mode === 'trucks') {
      var T = R.trucks, n = Math.max(1, Math.ceil(guests / T.guests_per_truck));
      var fl = Math.max(guests * T.low, n * T.truck_min_low), fh = Math.max(guests * T.high, n * T.truck_min_high);
      rows.push({ label: 'Food (' + n + (n === 1 ? ' truck' : ' trucks') + ', truck minimums included)', low: fl, high: fh });
      var cl = Math.max(T.fee_min, fl * T.fee_low), ch = Math.max(T.fee_min, fh * T.fee_high);
      rows.push({ label: T.fee_label, low: cl, high: ch });
      lo = fl + cl; hi = fh + ch;
      per = 'About ' + prange(lo / guests, hi / guests) + ' per guest';
    } else if (mode === 'festival') {
      var F = R.festival;
      var fee = interp(F.fee_points, att);
      rows.push({ label: F.fee_label, low: fee, high: fee * F.fee_high });
      rows.push({ label: F.expense_label, low: att * F.expense_low, high: att * F.expense_high });
      if (vendors) rows.push({ label: 'Vendor allowances (' + vendors + ' × ' + money(F.vendor_allowance) + ')', low: vendors * F.vendor_allowance, high: vendors * F.vendor_allowance });
      rows.forEach(function (r) { lo += r.low; hi += r.high; });
      per = 'About ' + prange(lo / att, hi / att) + ' per attendee';
      offset = 'Potential offsets: ticket sales of about ' + range(att * F.ticket_low, att * F.ticket_high) +
        ' (at $' + F.ticket_low + '–' + F.ticket_high + ' average), plus sponsorships.';
    } else {
      var r2 = sum(R.items, { guest: guests, guest_hour: guests * hours, hour: hours, flat: 1 }, type.factor || 1);
      rows = r2.rows; lo = r2.lo; hi = r2.hi;
      var fee2 = R.planning;
      var fl = Math.max(fee2.min, lo * fee2.low), fh = Math.max(fee2.min, hi * fee2.high);
      rows.push({ label: fee2.label, low: fl, high: fh });
      lo += fl; hi += fh;
      per = 'About ' + prange(lo / guests, hi / guests) + ' per guest';
    }

    $('c-total').textContent = range(lo, hi) + (plus ? '+' : '');
    $('c-per').textContent = per;
    $('c-offset').hidden = !offset; $('c-offset').textContent = offset;
    var max = Math.max.apply(null, rows.map(function (r) { return r.high; })) || 1;
    $('c-rows').innerHTML = rows.map(function (r) {
      return '<li><span>' + r.label + '</span><b>' + range(r.low, r.high) + '</b>' +
        '<i style="width:' + Math.max(4, r.high / max * 100) + '%"></i></li>';
    }).join('');
    $('c-guests-out').textContent = guests.toLocaleString('en-US');
    $('c-hours-out').textContent = hours + (hours === 1 ? ' hour' : ' hours');
    $('c-act-days-out').textContent = days;
    $('c-act-samples-out').textContent = samples.toLocaleString('en-US');
    $('c-att-out').textContent = att.toLocaleString('en-US');
    $('c-vend-out').textContent = vendors;

    var size = { event: guests + ' guests', package: guests + ' guests, ' + R.packages[$('c-pkg').value].label,
                 activation: days + ' day(s), ' + samples + ' samples', trucks: guests + ' guests', festival: att.toLocaleString('en-US') + ' attendees, ' + vendors + ' vendors' }[mode];
    $('h-type').value = type.planType;
    $('h-guests').value = size;
    $('h-hours').value = (mode === 'event' || mode === 'activation' || mode === 'trucks') ? hours + (mode === 'activation' ? ' per day' : '') : '';
    $('h-services').value = rows.filter(function (r) { return !/^Planning/.test(r.label); }).map(function (r) { return r.label; }).join(', ');
    $('h-estimate').value = range(lo, hi) + (plus ? '+' : '');

    var q = new URLSearchParams({ type: type.planType, budget: lo + '-' + hi });
    if (mode === 'event' || mode === 'package' || mode === 'trucks') q.set('guests', guests);
    if (mode === 'festival') q.set('guests', att);
    $('c-cta').href = root.dataset.plan + '?' + q.toString();
  }

  root.addEventListener('input', compute);
  root.addEventListener('change', compute);
  $('c-guests-range').addEventListener('input', function () { $('c-guests').value = this.value; compute(); });
  $('c-guests').addEventListener('input', function () { $('c-guests-range').value = this.value; });
  compute();
})();
