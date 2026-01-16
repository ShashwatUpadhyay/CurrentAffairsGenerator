// Global state
let currentLanguage = localStorage.getItem("language") || "en";
let allNews = [];
let currentPage = 1;
let hasNextPage = false;
let isLoading = false;

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  initializeLanguageToggle();
  loadNews();
  setupSearchAndFilters();
});

// Language Toggle
function initializeLanguageToggle() {
  const toggleBtn = document.getElementById("lang-toggle");
  updateToggleText(toggleBtn);

  toggleBtn.addEventListener("click", function () {
    currentLanguage = currentLanguage === "en" ? "hi" : "en";
    localStorage.setItem("language", currentLanguage);
    updateToggleText(toggleBtn);
    // Reset pagination and reload
    currentPage = 1;
    allNews = [];
    loadNews();
  });
}

function updateToggleText(toggleBtn) {
  toggleBtn.textContent = currentLanguage === "en" ? "हिंदी" : "English";
}

// Load News from API
async function loadNews(append = false) {
  if (isLoading) return;
  isLoading = true;
  
  const newsGrid = document.getElementById("news-grid");
  
  if (!append) {
    newsGrid.innerHTML = '<div class="loading">Loading news...</div>';
  }

  try {
    const response = await fetch(`/news_api/?lang=${currentLanguage}&page=${currentPage}`);
    const data = await response.json();
    
    // DRF returns paginated data in this format
    const newsData = data.results || data;
    hasNextPage = !!data.next;
    
    if (append) {
      allNews = [...allNews, ...newsData];
    } else {
      allNews = newsData;
    }
    
    displayNews(allNews, append);
  } catch (error) {
    console.error("Error fetching news:", error);
    newsGrid.innerHTML =
      '<div class="no-results">Failed to load news. Please try again.</div>';
  } finally {
    isLoading = false;
  }
}

// Load More News
function loadMoreNews() {
  currentPage++;
  loadNews(true);
}

// Display News Cards
function displayNews(newsData, append = false) {
  const newsGrid = document.getElementById("news-grid");

  if (newsData.length === 0 && !append) {
    newsGrid.innerHTML =
      '<div class="no-results">No news articles found.</div>';
    return;
  }

  const newsHTML = newsData
    .map(
      (news) => `
        <div class="news-card">
            <div class="news-card-label">News Article</div>
            <img src="${news.image || "/static/images/placeholder.jpg"}" 
                 alt="${news.title}" 
                 class="news-card-image"
                 onerror="if(!this.dataset.errorHandled){this.dataset.errorHandled='1';this.src='/static/images/placeholder.jpg'}">
            <div class="news-card-content">
                <h3 class="news-card-title">${news.title}</h3>
                <div class="news-card-meta">
                    ${new Date().toLocaleDateString(
                      currentLanguage === "hi" ? "hi-IN" : "en-US"
                    )}
                </div>
                <p class="news-card-description">
                    ${
                      news.description || news.content.substring(0, 150) + "..."
                    }
                </p>
                <div class="news-card-actions">
                    <a href="${
                      news.url
                    }" target="_blank" class="btn btn-primary">
                        ${currentLanguage === "en" ? "View More" : "और देखें"}
                    </a>
                    <button onclick="practiceNow('${
                      news.uid
                    }')" class="btn btn-success">
                        ${
                          currentLanguage === "en"
                            ? "Practice Now"
                            : "अभ्यास करें"
                        }
                    </button>
                </div>
            </div>
        </div>
    `
    )
    .join("");
  
  if (append) {
    newsGrid.innerHTML += newsHTML;
  } else {
    newsGrid.innerHTML = newsHTML;
  }
  
  // Add or remove Load More button
  updateLoadMoreButton();
}

// Update Load More Button
function updateLoadMoreButton() {
  let loadMoreContainer = document.getElementById("load-more-container");
  
  if (!loadMoreContainer) {
    // Create container if it doesn't exist
    loadMoreContainer = document.createElement("div");
    loadMoreContainer.id = "load-more-container";
    loadMoreContainer.style.textAlign = "center";
    loadMoreContainer.style.marginTop = "30px";
    loadMoreContainer.style.marginBottom = "30px";
    document.getElementById("news-grid").insertAdjacentElement("afterend", loadMoreContainer);
  }
  
  if (hasNextPage) {
    loadMoreContainer.innerHTML = `
      <button onclick="loadMoreNews()" class="btn btn-success" style="padding: 12px 40px; font-size: 1rem;">
        ${currentLanguage === "en" ? "Load More News" : "और समाचार लोड करें"}
      </button>
    `;
  } else {
    loadMoreContainer.innerHTML = '';
  }
}

// Practice Now - Navigate to Quiz
function practiceNow(newsUid) {
  window.location.href = `/mcq/${newsUid}/?lang=${currentLanguage}`;
}

// Search Functionality
function setupSearchAndFilters() {
  const searchBar = document.getElementById("search-bar");

  if (searchBar) {
    searchBar.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      const filtered = allNews.filter(
        (news) =>
          news.title.toLowerCase().includes(searchTerm) ||
          news.description.toLowerCase().includes(searchTerm) ||
          news.content.toLowerCase().includes(searchTerm)
      );
      displayNews(filtered, false);
    });
  }

  // Category tabs (placeholder - can be extended)
  const categoryTabs = document.querySelectorAll(".category-tab");
  categoryTabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      categoryTabs.forEach((t) => t.classList.remove("active"));
      this.classList.add("active");
      // Filter logic can be added here when categories are implemented
    });
  });
}
