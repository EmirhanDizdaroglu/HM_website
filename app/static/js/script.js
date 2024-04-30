document.addEventListener("DOMContentLoaded", function () {
  const slidesContainer = document.getElementById("slides");
  const indicatorsContainer = document.getElementById("indicators");
  const menuToggle = document.querySelector(".menu-toggle");
  const header = document.querySelector(".main-header");


  
  let currentSlide = 0;
  const groupSize = 4; // Her slaytta 4 ürün


  menuToggle.addEventListener("click", function() {
    header.classList.toggle("menu-open"); // Menü açıldığında sınıf ekle/kaldır
});
  const updateSlide = () => {
    const offset = -currentSlide * 100;
    slidesContainer.style.transform = `translateX(${offset}%)`;

    const indicators = document.querySelectorAll(".indicator");
    indicators.forEach((indicator, index) => {
      indicator.classList.toggle("active", index === currentSlide);
    });
  };

  const fetchProducts = (category_id = '') => {
    const url = `/new-products${category_id ? `?category=${encodeURIComponent(category_id)}` : ''}`;

    fetch(url)
      .then((response) => response.json())
      .then((products) => {
        slidesContainer.innerHTML = ''; // Slaytları temizle
        indicatorsContainer.innerHTML = ''; // Göstergeleri temizle

        products.forEach((product, index) => {
          if (index % groupSize === 0) { // Her 4 üründe bir yeni slayt
            const slide = document.createElement("div");
            slide.className = "slide";
            slidesContainer.appendChild(slide);

            const indicator = document.createElement("span");
            indicator.className = "indicator";
            indicator.addEventListener("click", () => {
              currentSlide = Math.floor(index / groupSize);
              updateSlide();
            });
            indicatorsContainer.appendChild(indicator);
          }

          const productDiv = document.createElement("div");
productDiv.className = "product";
productDiv.innerHTML = `
  <img src="${product.image}" alt="${product.name}">
  ${product.is_new ? "<span class='new-tag'>New</span>" : ""}
  <br>${product.name}
  <br>${product.price} TL
`;


          slidesContainer.lastChild.appendChild(productDiv);
        });

        currentSlide = 0; // İlk slayta geri dön
        updateSlide();
      })
      .catch((err) => {
        console.error("Error fetching products:", err);
      });
  };

  document.getElementById("prev").addEventListener("click", () => {
    currentSlide = (currentSlide - 1 + slidesContainer.childElementCount) % slidesContainer.childElementCount;
    updateSlide();
  });

  document.getElementById("next").addEventListener("click", () => {
    currentSlide = (currentSlide + 1) % slidesContainer.childElementCount;
    updateSlide();
  });

  const categoryButtons = document.querySelectorAll(".category-btn");

  categoryButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault(); // Varsayılan davranışı engelle

      // Tüm butonlardan 'selected' sınıfını kaldır
      categoryButtons.forEach((btn) => btn.classList.remove("selected"));

      // Tıklanan butona 'selected' sınıfını ekle
      button.classList.add("selected");

      const category_id = button.getAttribute("data-category");
      fetchProducts(category_id); // Ürünleri getir
    });
  });

  // Başlangıçta ilk kategori seçili olsun
  const firstButton = document.querySelector(".category-btn[data-category='1']");
  firstButton.classList.add("selected");

  fetchProducts('1'); // Varsayılan olarak kadın kategorisinden ürünleri getir

  document.getElementById("search-btn").addEventListener("click", function() {
    const searchText = document.getElementById("search-box").value;
    if (searchText.trim() !== "") {
      window.location.href = `/search?query=${encodeURIComponent(searchText.trim())}`;
    }
  });
  
  document.getElementById("search-box").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Varsayılan form gönderimini önler
      document.getElementById("search-btn").click();
    }
  });
  
});
