(() => {
  const cards = Array.from(document.querySelectorAll("[data-product-card]"));
  const searchInputs = Array.from(document.querySelectorAll("#product-search, #catalog-search"));
  const count = document.querySelector("#results-count");
  const resultLabel = document.querySelector("#results-label");
  const noResults = document.querySelector("#no-results");
  const status = document.querySelector("#search-status");
  const categoryLinks = Array.from(document.querySelectorAll("[data-category-link]"));
  const allLink = document.querySelector(".category-nav__link--active");
  let activeCategory = "";

  document.querySelectorAll("[data-message]").forEach((message) => {
    const dismiss = () => {
      message.classList.add("message--leaving");
      window.setTimeout(() => message.remove(), 180);
    };
    const timer = message.hasAttribute("data-autodismiss")
      ? window.setTimeout(dismiss, 2500)
      : null;
    message.querySelector("[data-dismiss-message]")?.addEventListener("click", () => {
      if (timer !== null) window.clearTimeout(timer);
      dismiss();
    });
  });

  const normalize = (value) => value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("es-CL")
    .trim();

  const filterProducts = () => {
    const query = normalize(searchInputs[0]?.value || "");
    let visible = 0;

    cards.forEach((card) => {
      const matchesSearch = normalize(card.dataset.search || "").includes(query);
      const matchesCategory = !activeCategory || normalize(card.dataset.search || "").includes(normalize(activeCategory));
      const show = matchesSearch && matchesCategory;
      card.hidden = !show;
      if (show) visible += 1;
    });

    if (count) count.textContent = String(visible);
    if (resultLabel) resultLabel.textContent = visible === 1 ? "producto disponible" : "productos disponibles";
    if (noResults) noResults.hidden = visible !== 0 || cards.length === 0;
    if (status) {
      status.textContent = query || activeCategory
        ? `${visible} ${visible === 1 ? "producto encontrado" : "productos encontrados"}`
        : "";
    }
  };

  searchInputs.forEach((input) => {
    input.addEventListener("input", () => {
      searchInputs.forEach((other) => {
        if (other !== input) other.value = input.value;
      });
      filterProducts();
    });
  });

  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      searchInputs[0]?.focus();
    }
  });

  categoryLinks.forEach((link) => {
    link.addEventListener("click", () => {
      activeCategory = link.dataset.categoryLink || "";
      categoryLinks.forEach((other) => other.classList.toggle("category-nav__link--active", other === link));
      allLink?.classList.remove("category-nav__link--active");
      filterProducts();
    });
  });

  allLink?.addEventListener("click", () => {
    activeCategory = "";
    categoryLinks.forEach((link) => link.classList.remove("category-nav__link--active"));
    allLink.classList.add("category-nav__link--active");
    filterProducts();
  });

})();
