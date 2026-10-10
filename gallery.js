// Shared helpers for the gallery and watch pages.

// An entry can share another's folder (e.g. a read-aloud version) by naming it in "dir".
function animationDir(a) {
  return 'animations/' + (a.dir || a.slug) + '/';
}

// The file to play: "index.html" by default for HTML animations.
function animationFile(a) {
  return animationDir(a) + (a.file || 'index.html');
}

function metaLine(a) {
  return [a.model, a.date].filter(Boolean).join(' · ');
}

function loadAnimations() {
  return fetch('animations.json', { cache: 'no-cache' }).then(function (res) {
    if (!res.ok) throw new Error('Could not load animations.json');
    return res.json();
  });
}

function el(tag, className, text) {
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

// Gallery page

function renderThumb(a) {
  var thumb = el('div', 'thumb');
  if (a.poster) {
    var img = el('img');
    img.src = animationDir(a) + a.poster;
    img.alt = '';
    img.loading = 'lazy';
    thumb.appendChild(img);
  } else if (a.type === 'video') {
    var video = el('video');
    video.src = animationFile(a);
    video.muted = true;
    video.loop = true;
    video.autoplay = true;
    video.playsInline = true;
    thumb.appendChild(video);
  } else {
    var frame = el('iframe');
    // previewTime shows a single still frame instead of playing the whole animation in the card.
    frame.src = animationFile(a) + (a.previewTime != null ? '?t=' + a.previewTime : '');
    frame.title = a.title;
    frame.loading = 'lazy';
    frame.tabIndex = -1;
    frame.setAttribute('sandbox', 'allow-scripts');
    thumb.appendChild(frame);
  }
  return thumb;
}

function renderCard(a) {
  var card = el('a', 'card');
  card.href = 'watch.html?a=' + encodeURIComponent(a.slug);
  card.appendChild(renderThumb(a));
  var body = el('div', 'card-body');
  body.appendChild(el('h3', 'card-title', a.title));
  if (a.direction) body.appendChild(el('p', 'card-direction', '“' + a.direction + '”'));
  var meta = metaLine(a);
  if (meta) body.appendChild(el('div', 'meta', meta));
  card.appendChild(body);
  return card;
}

// The gallery is split into sections by each entry's "section" field (fiction when absent).
// Within a section, cards keep their order in animations.json.
var SECTIONS = [
  { key: 'fiction', title: 'Fiction' },
  { key: 'essay', title: 'Essays/Technical documents' }
];

function renderGallery(list) {
  var gallery = document.getElementById('gallery');
  if (!list.length) {
    gallery.appendChild(el('p', 'empty', 'No animations yet.'));
    return;
  }
  SECTIONS.forEach(function (s) {
    var items = list.filter(function (a) { return (a.section || 'fiction') === s.key; });
    if (!items.length) return;
    var section = el('section', 'gallery-section');
    section.appendChild(el('h2', 'section-title', s.title));
    var grid = el('div', 'gallery');
    items.forEach(function (a) { grid.appendChild(renderCard(a)); });
    section.appendChild(grid);
    gallery.appendChild(section);
  });
}

if (document.getElementById('gallery')) {
  loadAnimations().then(renderGallery).catch(function (err) {
    document.getElementById('gallery').appendChild(el('p', 'error', err.message));
  });
}
