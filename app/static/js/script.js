document.addEventListener("DOMContentLoaded", function() {
  const slidesContainer = document.getElementById("slides");
  let currentSlide = 0; // Başlangıç slaytı

  const tabletBreakpoint = 992; // Tablet ve bilgisayar modunu ayıran eşik
  const groupSize = window.innerWidth >= tabletBreakpoint ? 4 : 2; // Grup boyutunu belirleyin

  // Yeni ürünleri backend'den al ve grupları oluştur
  fetch('/new-products')  // Yeni ürünleri al
    .then(response => response.json()) // JSON formatına dönüştür
    .then(products => {
      products.forEach((product, index) => {
        if (index % groupSize === 0) {  // Grup boyutuna göre yeni 'slide' oluştur
          const slide = document.createElement("div");
          slide.className = "slide";
          slidesContainer.appendChild(slide);  // Yeni slayta ekle
        }

        const productDiv = document.createElement("div");
        productDiv.className = "product";
        productDiv.innerHTML = `
          <img src="${product.image}" alt="${product.name}" style="width: 222px; height: 333px;">
          <br>${product.name}
          <br>${product.price} TL
        `;
        slidesContainer.lastChild.appendChild(productDiv);  // Son slayta ürün ekle
      });

      updateSlide();  // Slaytı güncelle
    })
    .catch(err => console.error("Error fetching new products:", err)); // Hata kontrolü

  const updateSlide = () => {
    const totalSlides = slidesContainer.childElementCount; // Toplam slayt sayısı
    const offset = -currentSlide * 100; // Slayt ofseti
    slidesContainer.style.transform = `translateX(${offset}%)`; // Slaytı hareket ettir

    const indicators = document.querySelectorAll(".indicator");
    indicators.forEach((indicator, index) => {
      if (index === currentSlide) {
        indicator.classList.add("active");
      } else {
        indicator.classList.remove("active");
      }
    });
  };

  // Prev ve Next düğmeleri
  document.getElementById("prev").addEventListener("click", () => {
    const totalSlides = slidesContainer.childElementCount;
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides; // Dairesel kaydırma
    updateSlide(); // Slaytı güncelle
  });

  document.getElementById("next").addEventListener("click", () => {
    const totalSlides = slidesContainer.childElementCount;
    currentSlide = (currentSlide + 1) % totalSlides; // Dairesel kaydırma
    updateSlide(); // Slaytı güncelle
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const menuToggle = document.querySelector(".menu-toggle");
  const header = document.querySelector(".main-header");

  menuToggle.addEventListener("click", function() {
      header.classList.toggle("menu-open"); // Menü açıldığında sınıf ekle/kaldır
  });
});

window.onresize = function() {
  location.reload(); // Sayfayı yeniler
};
