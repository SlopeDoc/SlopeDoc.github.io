function styleHeaderTitle() {
  const el = document.querySelector(
    '.md-header__title .md-header__topic:first-child .md-ellipsis'
  );
  if (!el || el.querySelector(".slope-hl")) return;
  el.innerHTML =
    'Slope: <span class="slope-hl">Sl</span>ides with Polysc<span class="slope-hl">ope</span>';
}
if (typeof document$ !== "undefined") document$.subscribe(styleHeaderTitle);
else document.addEventListener("DOMContentLoaded", styleHeaderTitle);
