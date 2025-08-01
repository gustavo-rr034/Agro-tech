// Mobile Navigation
document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger")
  const navMenu = document.querySelector(".nav-menu")

  if (hamburger && navMenu) {
    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("active")
      navMenu.classList.toggle("active")
    })

    // Close menu when clicking on a link
    document.querySelectorAll(".nav-menu a").forEach((link) => {
      link.addEventListener("click", () => {
        hamburger.classList.remove("active")
        navMenu.classList.remove("active")
      })
    })
  }

  // Flash messages auto-close
  const flashMessages = document.querySelectorAll(".flash-message")
  flashMessages.forEach((message) => {
    const closeBtn = message.querySelector(".close-flash")
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        message.style.animation = "slideOut 0.3s ease"
        setTimeout(() => message.remove(), 300)
      })
    }

    // Auto-close after 5 seconds
    setTimeout(() => {
      if (message.parentNode) {
        message.style.animation = "slideOut 0.3s ease"
        setTimeout(() => message.remove(), 300)
      }
    }, 5000)
  })

  // Product filtering
  const filterBtns = document.querySelectorAll(".filter-btn")
  const productCards = document.querySelectorAll(".product-card")

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Remove active class from all buttons
      filterBtns.forEach((b) => b.classList.remove("active"))
      // Add active class to clicked button
      btn.classList.add("active")

      const category = btn.getAttribute("data-category")

      productCards.forEach((card) => {
        if (category === "all" || card.getAttribute("data-category") === category) {
          card.style.display = "block"
          card.style.animation = "fadeIn 0.5s ease"
        } else {
          card.style.display = "none"
        }
      })
    })
  })

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Navbar scroll effect
  window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar")
    if (window.scrollY > 100) {
      navbar.style.background = "rgba(255, 255, 255, 0.95)"
      navbar.style.backdropFilter = "blur(10px)"
    } else {
      navbar.style.background = "#ffffff"
      navbar.style.backdropFilter = "none"
    }
  })
})

// Weather functionality
function searchWeather() {
  const cityInput = document.getElementById("cityInput")
  const city = cityInput.value.trim()

  if (!city) {
    alert("Por favor, digite o nome de uma cidade")
    return
  }

  performWeatherSearch(city)
}

function searchCity(cityName) {
  document.getElementById("cityInput").value = cityName
  performWeatherSearch(cityName)
}

function performWeatherSearch(city) {
  // Show loading state
  const weatherResult = document.getElementById("weatherResult")
  const cityName = document.getElementById("cityName")
  const temperature = document.getElementById("temperature")
  const searchButton = document.querySelector(".weather-search button")

  // Reset button state and show loading
  searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Buscando dados reais...'
  searchButton.disabled = true

  weatherResult.style.display = "block"
  cityName.textContent = "Carregando dados meteorológicos..."
  temperature.textContent = "..."

  // Fetch weather data from our API
  fetch(`/api/weather/${encodeURIComponent(city)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`)
      }
      return response.json()
    })
    .then((data) => {
      if (data.error) {
        throw new Error(data.error)
      }
      updateWeatherDisplay(data)
    })
    .catch((error) => {
      console.error("Erro ao buscar dados do clima:", error)

      // Show error message in the weather display
      cityName.textContent = "Erro ao carregar dados"
      temperature.textContent = "--°C"
      document.getElementById("description").textContent =
        error.message || "Cidade não encontrada ou dados indisponíveis"
      document.getElementById("humidity").textContent = "--%"
      document.getElementById("windSpeed").textContent = "-- km/h"

      // Clear forecast
      document.getElementById("forecastGrid").innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: #e74c3c; padding: 20px;">
          <i class="fas fa-exclamation-triangle"></i><br>
          Não foi possível carregar a previsão do tempo.<br>
          Verifique o nome da cidade e tente novamente.<br>
          <small>Tente usar o nome completo da cidade ou adicione o país (ex: "Paris, France")</small>
        </div>
      `
    })
    .finally(() => {
      // Always restore button state
      searchButton.innerHTML = '<i class="fas fa-search"></i> Buscar'
      searchButton.disabled = false
    })
}

function updateWeatherDisplay(data) {
  // Update current weather
  document.getElementById("cityName").textContent = data.city
  document.getElementById("temperature").textContent = `${data.temperature}°C`
  document.getElementById("description").textContent = data.description
  document.getElementById("humidity").textContent = `${data.humidity}%`
  document.getElementById("windSpeed").textContent = `${data.wind_speed} km/h`

  // Update weather icon
  const weatherIcon = document.querySelector(".weather-icon i")
  weatherIcon.className = data.icon

  // Update additional info
  const feelsLike = document.getElementById("feelsLike")
  const pressure = document.getElementById("pressure")
  const visibility = document.getElementById("visibility")
  const uvIndex = document.getElementById("uvIndex")

  if (feelsLike) feelsLike.textContent = `${data.feels_like}°C`
  if (pressure) pressure.textContent = `${data.pressure} hPa`
  if (visibility) visibility.textContent = `${data.visibility} km`
  if (uvIndex) uvIndex.textContent = data.uv_index || "N/A"

  // Update forecast
  const forecastGrid = document.getElementById("forecastGrid")
  forecastGrid.innerHTML = ""

  if (data.forecast && data.forecast.length > 0) {
    data.forecast.forEach((item) => {
      const forecastItem = document.createElement("div")
      forecastItem.className = "forecast-item"

      forecastItem.innerHTML = `
        <div class="forecast-day">${item.day}</div>
        <div class="forecast-icon">
          <i class="${item.icon}"></i>
        </div>
        <div class="forecast-temps">${item.temp_max}°/${item.temp_min}°</div>
        <div class="forecast-condition">${item.condition}</div>
      `
      forecastGrid.appendChild(forecastItem)
    })
  } else {
    forecastGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; color: #7f8c8d; padding: 20px;">
        <i class="fas fa-info-circle"></i><br>
        Previsão não disponível para esta localização
      </div>
    `
  }

  // Show success message
  showSuccessMessage(`Dados meteorológicos reais carregados para ${data.city}`)
}

function showSuccessMessage(message) {
  // Create and show a temporary success message
  const successDiv = document.createElement("div")
  successDiv.className = "temp-success-message"
  successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`
  successDiv.style.cssText = `
    position: fixed;
    top: 90px;
    right: 20px;
    background: #d4edda;
    color: #155724;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 1002;
    animation: slideIn 0.3s ease;
  `

  document.body.appendChild(successDiv)

  setTimeout(() => {
    successDiv.style.animation = "slideOut 0.3s ease"
    setTimeout(() => successDiv.remove(), 300)
  }, 3000)
}

// Contact seller functionality
function contactSeller(phone) {
  if (confirm(`Deseja entrar em contato com o vendedor?\nTelefone: ${phone}`)) {
    window.open(`tel:${phone}`, "_self")
  }
}

// Form validation
function validateForm(formId) {
  const form = document.getElementById(formId)
  const inputs = form.querySelectorAll("input[required], select[required]")
  let isValid = true

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.style.borderColor = "#e74c3c"
      isValid = false
    } else {
      input.style.borderColor = "#e1e8ed"
    }
  })

  return isValid
}

// Add CSS animations
const style = document.createElement("style")
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
`
document.head.appendChild(style)

// Initialize tooltips and other interactive elements
document.addEventListener("DOMContentLoaded", () => {
  // Add hover effects to cards
  const cards = document.querySelectorAll(".feature-card, .product-card, .plantation-card, .blog-card")
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-10px)"
    })

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)"
    })
  })

  // Add loading states to buttons
  const buttons = document.querySelectorAll(".btn")
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      if (this.type === "submit") {
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...'
        this.disabled = true
      }
    })
  })
})

// Weather search on Enter key
document.addEventListener("DOMContentLoaded", () => {
  const cityInput = document.getElementById("cityInput")
  if (cityInput) {
    cityInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        searchWeather()
      }
    })
  }
})
