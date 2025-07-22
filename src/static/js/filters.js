/**
 * Système de filtres et de tri pour l'application Nuur-Library
 * Fonctions réutilisables pour différentes pages
 */

// Utilitaires généraux
const FilterUtils = {
  // Fonction pour masquer/afficher un élément
  toggleElement(element, show) {
    element.style.display = show
      ? element.dataset.defaultDisplay || "block"
      : "none";
  },

  // Fonction pour nettoyer les chaînes de recherche
  normalizeString(str) {
    return str
      .toLowerCase()
      .trim()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  },

  // Fonction pour extraire les nombres d'une chaîne
  extractNumber(str) {
    const match = str.match(/[\d.,]+/);
    return match ? parseFloat(match[0].replace(",", ".")) : 0;
  },

  // Fonction pour compter les éléments visibles
  countVisibleElements(selector) {
    const elements = document.querySelectorAll(selector);
    return Array.from(elements).filter(
      (el) => el.style.display !== "none" && !el.hasAttribute("hidden")
    ).length;
  },
};

// Filtres pour les livres (page admin et utilisateur)
const BookFilters = {
  filterBooks(options = {}) {
    const {
      searchSelector = "#search-books",
      availabilitySelector = "#filter-availability",
      stockSelector = "#filter-stock",
      cardSelector = ".book-card-admin, .book-card",
    } = options;

    const searchValue = FilterUtils.normalizeString(
      document.querySelector(searchSelector)?.value || ""
    );
    const availabilityFilter =
      document.querySelector(availabilitySelector)?.value || "";
    const stockFilter = document.querySelector(stockSelector)?.value || "";

    const bookCards = document.querySelectorAll(cardSelector);

    bookCards.forEach((card) => {
      let showCard = true;

      // Filtre par recherche (titre et auteur)
      if (searchValue && showCard) {
        const title = FilterUtils.normalizeString(
          card.getAttribute("data-title") ||
            card.querySelector(".book-title")?.textContent ||
            ""
        );
        const author = FilterUtils.normalizeString(
          card.getAttribute("data-author") ||
            card.querySelector(".book-author")?.textContent ||
            ""
        );

        if (!title.includes(searchValue) && !author.includes(searchValue)) {
          showCard = false;
        }
      }

      // Filtre par disponibilité
      if (availabilityFilter && showCard) {
        const available = card.getAttribute("data-available") === "true";
        if (availabilityFilter === "disponible" && !available) {
          showCard = false;
        } else if (availabilityFilter === "indisponible" && available) {
          showCard = false;
        }
      }

      // Filtre par stock
      if (stockFilter && showCard) {
        const stock = parseInt(card.getAttribute("data-stock")) || 0;
        if (stockFilter === "low" && stock >= 5) {
          showCard = false;
        } else if (stockFilter === "medium" && (stock < 5 || stock > 20)) {
          showCard = false;
        } else if (stockFilter === "high" && stock <= 20) {
          showCard = false;
        }
      }

      FilterUtils.toggleElement(card, showCard);
    });

    // Afficher le nombre de résultats
    this.updateResultsCount(cardSelector);
  },

  sortBooks(options = {}) {
    const {
      sortSelector = "#sort-books",
      gridSelector = "#books-grid",
      cardSelector = ".book-card-admin, .book-card",
    } = options;

    const sortValue = document.querySelector(sortSelector)?.value;
    const grid = document.querySelector(gridSelector);
    const cards = Array.from(document.querySelectorAll(cardSelector));

    if (!sortValue || !grid) return;

    cards.sort((a, b) => {
      const getTitle = (card) =>
        FilterUtils.normalizeString(
          card.getAttribute("data-title") ||
            card.querySelector(".book-title")?.textContent ||
            ""
        );
      const getAuthor = (card) =>
        FilterUtils.normalizeString(
          card.getAttribute("data-author") ||
            card.querySelector(".book-author")?.textContent ||
            ""
        );
      const getPrice = (card) => {
        return (
          parseFloat(card.getAttribute("data-price")) ||
          FilterUtils.extractNumber(
            card.querySelector(".book-price")?.textContent || "0"
          )
        );
      };
      const getStock = (card) => parseInt(card.getAttribute("data-stock")) || 0;

      switch (sortValue) {
        case "title-asc":
          return getTitle(a).localeCompare(getTitle(b));
        case "title-desc":
          return getTitle(b).localeCompare(getTitle(a));
        case "author-asc":
          return getAuthor(a).localeCompare(getAuthor(b));
        case "author-desc":
          return getAuthor(b).localeCompare(getAuthor(a));
        case "price-asc":
          return getPrice(a) - getPrice(b);
        case "price-desc":
          return getPrice(b) - getPrice(a);
        case "stock-asc":
          return getStock(a) - getStock(b);
        case "stock-desc":
          return getStock(b) - getStock(a);
        default:
          return 0;
      }
    });

    // Réorganiser les cartes dans le DOM
    cards.forEach((card) => grid.appendChild(card));
  },

  resetFilters(options = {}) {
    const {
      searchSelector = "#search-books",
      availabilitySelector = "#filter-availability",
      stockSelector = "#filter-stock",
      sortSelector = "#sort-books",
      cardSelector = ".book-card-admin, .book-card",
    } = options;

    // Reset des inputs
    const inputs = [
      searchSelector,
      availabilitySelector,
      stockSelector,
      sortSelector,
    ];
    inputs.forEach((selector) => {
      const element = document.querySelector(selector);
      if (element) element.value = "";
    });

    // Réafficher toutes les cartes
    document.querySelectorAll(cardSelector).forEach((card) => {
      FilterUtils.toggleElement(card, true);
    });

    this.updateResultsCount(cardSelector);
  },

  updateResultsCount(cardSelector) {
    const visibleCards = FilterUtils.countVisibleElements(cardSelector);
    const totalCards = document.querySelectorAll(cardSelector).length;

    // Mettre à jour l'affichage du compteur si il existe
    const counter = document.querySelector("#results-counter");
    if (counter) {
      counter.textContent = `${visibleCards} sur ${totalCards} livres affichés`;
    }

    console.log(`${visibleCards} livres affichés sur ${totalCards}`);
  },
};

// Filtres pour les commandes
const OrderFilters = {
  filterOrders() {
    const searchValue = FilterUtils.normalizeString(
      document.querySelector("#search-orders")?.value || ""
    );
    const statusFilter = document.querySelector("#filter-status")?.value || "";
    const amountFilter = document.querySelector("#filter-amount")?.value || "";

    const orderCards = document.querySelectorAll(".order-card-filter");

    orderCards.forEach((card) => {
      let showCard = true;

      // Filtre par recherche (client et numéro commande)
      if (searchValue && showCard) {
        const client = FilterUtils.normalizeString(
          card.getAttribute("data-client") || ""
        );
        const orderId = card.getAttribute("data-order-id") || "";
        if (!client.includes(searchValue) && !orderId.includes(searchValue)) {
          showCard = false;
        }
      }

      // Filtre par statut
      if (statusFilter && showCard) {
        const status = card.getAttribute("data-status");
        if (status !== statusFilter) {
          showCard = false;
        }
      }

      // Filtre par montant
      if (amountFilter && showCard) {
        const total = parseFloat(card.getAttribute("data-total")) || 0;
        if (amountFilter === "low" && total >= 5000) {
          showCard = false;
        } else if (
          amountFilter === "medium" &&
          (total < 5000 || total > 20000)
        ) {
          showCard = false;
        } else if (amountFilter === "high" && total <= 20000) {
          showCard = false;
        }
      }

      FilterUtils.toggleElement(card, showCard);
    });

    this.updateResultsCount();
  },

  sortOrders() {
    const sortValue = document.querySelector("#sort-orders")?.value;
    const grid = document.querySelector("#orders-grid");
    const cards = Array.from(document.querySelectorAll(".order-card-filter"));

    if (!sortValue || !grid) return;

    cards.sort((a, b) => {
      switch (sortValue) {
        case "date-desc":
          return (
            new Date(b.getAttribute("data-date")) -
            new Date(a.getAttribute("data-date"))
          );
        case "date-asc":
          return (
            new Date(a.getAttribute("data-date")) -
            new Date(b.getAttribute("data-date"))
          );
        case "amount-desc":
          return (
            parseFloat(b.getAttribute("data-total")) -
            parseFloat(a.getAttribute("data-total"))
          );
        case "amount-asc":
          return (
            parseFloat(a.getAttribute("data-total")) -
            parseFloat(b.getAttribute("data-total"))
          );
        case "client-asc":
          return FilterUtils.normalizeString(
            a.getAttribute("data-client")
          ).localeCompare(
            FilterUtils.normalizeString(b.getAttribute("data-client"))
          );
        case "client-desc":
          return FilterUtils.normalizeString(
            b.getAttribute("data-client")
          ).localeCompare(
            FilterUtils.normalizeString(a.getAttribute("data-client"))
          );
        default:
          return 0;
      }
    });

    cards.forEach((card) => grid.appendChild(card));
  },

  resetFilters() {
    const inputs = [
      "#search-orders",
      "#filter-status",
      "#filter-amount",
      "#sort-orders",
    ];
    inputs.forEach((selector) => {
      const element = document.querySelector(selector);
      if (element) element.value = "";
    });

    document.querySelectorAll(".order-card-filter").forEach((card) => {
      FilterUtils.toggleElement(card, true);
    });

    this.updateResultsCount();
  },

  updateResultsCount() {
    const visibleCards = FilterUtils.countVisibleElements(".order-card-filter");
    const totalCards = document.querySelectorAll(".order-card-filter").length;

    console.log(`${visibleCards} commandes affichées sur ${totalCards}`);
  },
};

// Filtres pour les clients
const ClientFilters = {
  filterClients() {
    const searchValue = FilterUtils.normalizeString(
      document.querySelector("#search-clients")?.value || ""
    );
    const statusFilter =
      document.querySelector("#filter-client-status")?.value || "";
    const ordersFilter =
      document.querySelector("#filter-orders-count")?.value || "";

    const clientCards = document.querySelectorAll(".client-card-filter");

    clientCards.forEach((card) => {
      let showCard = true;

      // Filtre par recherche (nom et email)
      if (searchValue && showCard) {
        const name = FilterUtils.normalizeString(
          card.getAttribute("data-client-name") || ""
        );
        const email = FilterUtils.normalizeString(
          card.getAttribute("data-client-email") || ""
        );
        if (!name.includes(searchValue) && !email.includes(searchValue)) {
          showCard = false;
        }
      }

      // Filtre par statut
      if (statusFilter && showCard) {
        const status = card.getAttribute("data-client-status");
        if (status !== statusFilter) {
          showCard = false;
        }
      }

      // Filtre par nombre de commandes
      if (ordersFilter && showCard) {
        const ordersCount =
          parseInt(card.getAttribute("data-orders-count")) || 0;
        if (ordersFilter === "no-orders" && ordersCount > 0) {
          showCard = false;
        } else if (
          ordersFilter === "low" &&
          (ordersCount === 0 || ordersCount > 5)
        ) {
          showCard = false;
        } else if (
          ordersFilter === "medium" &&
          (ordersCount < 6 || ordersCount > 15)
        ) {
          showCard = false;
        } else if (ordersFilter === "high" && ordersCount <= 15) {
          showCard = false;
        }
      }

      FilterUtils.toggleElement(card, showCard);
    });

    this.updateResultsCount();
  },

  sortClients() {
    const sortValue = document.querySelector("#sort-clients")?.value;
    const grid = document.querySelector("#clients-grid");
    const cards = Array.from(document.querySelectorAll(".client-card-filter"));

    if (!sortValue || !grid) return;

    cards.sort((a, b) => {
      switch (sortValue) {
        case "name-asc":
          return FilterUtils.normalizeString(
            a.getAttribute("data-client-name")
          ).localeCompare(
            FilterUtils.normalizeString(b.getAttribute("data-client-name"))
          );
        case "name-desc":
          return FilterUtils.normalizeString(
            b.getAttribute("data-client-name")
          ).localeCompare(
            FilterUtils.normalizeString(a.getAttribute("data-client-name"))
          );
        case "orders-desc":
          return (
            parseInt(b.getAttribute("data-orders-count")) -
            parseInt(a.getAttribute("data-orders-count"))
          );
        case "orders-asc":
          return (
            parseInt(a.getAttribute("data-orders-count")) -
            parseInt(b.getAttribute("data-orders-count"))
          );
        case "status-active":
          const aStatus = a.getAttribute("data-client-status");
          const bStatus = b.getAttribute("data-client-status");
          if (aStatus === "ACTIF" && bStatus !== "ACTIF") return -1;
          if (bStatus === "ACTIF" && aStatus !== "ACTIF") return 1;
          return 0;
        case "status-inactive":
          const aStatusInactive = a.getAttribute("data-client-status");
          const bStatusInactive = b.getAttribute("data-client-status");
          if (aStatusInactive === "INACTIF" && bStatusInactive !== "INACTIF")
            return -1;
          if (bStatusInactive === "INACTIF" && aStatusInactive !== "INACTIF")
            return 1;
          return 0;
        default:
          return 0;
      }
    });

    cards.forEach((card) => grid.appendChild(card));
  },

  resetFilters() {
    const inputs = [
      "#search-clients",
      "#filter-client-status",
      "#filter-orders-count",
      "#sort-clients",
    ];
    inputs.forEach((selector) => {
      const element = document.querySelector(selector);
      if (element) element.value = "";
    });

    document.querySelectorAll(".client-card-filter").forEach((card) => {
      FilterUtils.toggleElement(card, true);
    });

    this.updateResultsCount();
  },

  updateResultsCount() {
    const visibleCards = FilterUtils.countVisibleElements(
      ".client-card-filter"
    );
    const totalCards = document.querySelectorAll(".client-card-filter").length;

    console.log(`${visibleCards} clients affichés sur ${totalCards}`);
  },
};

// Exposition globale des fonctions pour compatibilité avec les templates existants
window.filterBooks = () => BookFilters.filterBooks();
window.sortBooks = () => BookFilters.sortBooks();
window.resetFilters = () => BookFilters.resetFilters();

window.filterOrders = () => OrderFilters.filterOrders();
window.sortOrders = () => OrderFilters.sortOrders();
window.resetOrderFilters = () => OrderFilters.resetFilters();

window.filterClients = () => ClientFilters.filterClients();
window.sortClients = () => ClientFilters.sortClients();
window.resetClientFilters = () => ClientFilters.resetFilters();

// Initialisation automatique au chargement de la page
document.addEventListener("DOMContentLoaded", function () {
  // Détecter la page actuelle et initialiser les filtres appropriés
  if (document.querySelector(".book-card-admin")) {
    BookFilters.updateResultsCount(".book-card-admin");
  } else if (document.querySelector(".book-card")) {
    BookFilters.updateResultsCount(".book-card");
  }

  if (document.querySelector(".order-card-filter")) {
    OrderFilters.updateResultsCount();
  }

  if (document.querySelector(".client-card-filter")) {
    ClientFilters.updateResultsCount();
  }
});
