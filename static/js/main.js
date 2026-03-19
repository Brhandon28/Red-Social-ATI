/*
 * SocialIT — Main JavaScript
 *
 * Heurísticas de Nielsen aplicadas:
 * - H1: Feedback visual (botón enviando, alertas auto-cierre)
 * - H3: Control usuario (Escape cierra modales/dropdowns, click fuera cierra)
 * - H5: Prevención errores (password strength, validación)
 * - H7: Flexibilidad (atajos teclado: / para búsqueda, Escape para cerrar)
 */

document.addEventListener('DOMContentLoaded', function () {

  // ============================================
  // H3 + H7: Profile Dropdown toggle
  // ============================================
  const profileBtn = document.querySelector('.header-profile-btn');
  const profileDropdown = document.querySelector('.profile-dropdown');

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      profileDropdown.classList.toggle('open');
    });

    document.addEventListener('click', function (e) {
      if (!profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('open');
      }
    });
  }

  // ============================================
  // H3 + H7: Close dropdowns/modals with Escape
  // ============================================
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      // Close profile dropdown
      if (profileDropdown) {
        profileDropdown.classList.remove('open');
      }
      // Close any open modal
      document.querySelectorAll('.modal-overlay.open').forEach(function (modal) {
        modal.classList.remove('open');
      });
    }

    // H7: "/" to focus search
    if (e.key === '/' && !isTyping(e.target)) {
      e.preventDefault();
      var searchInput = document.getElementById('global-search');
      if (searchInput) {
        searchInput.focus();
      }
    }

    // H7: "n" to go to new post (only when not typing)
    if (e.key === 'n' && !isTyping(e.target)) {
      var createLink = document.querySelector('a[href*="publicar"]');
      if (createLink) {
        window.location.href = createLink.href;
      }
    }
  });

  function isTyping(el) {
    var tag = el.tagName.toLowerCase();
    return tag === 'input' || tag === 'textarea' || tag === 'select' || el.isContentEditable;
  }

  // ============================================
  // H3: Modal open/close
  // ============================================
  document.querySelectorAll('[data-modal-target]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var modal = document.getElementById(this.dataset.modalTarget);
      if (modal) {
        modal.classList.add('open');
      }
    });
  });

  document.querySelectorAll('.modal-overlay').forEach(function (overlay) {
    // Close on clicking overlay background
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        overlay.classList.remove('open');
      }
    });

    // Close on X button
    var closeBtn = overlay.querySelector('.modal-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        overlay.classList.remove('open');
      });
    }
  });

  // ============================================
  // H1: Alert auto-dismiss & manual close
  // ============================================
  function dismissAlert(alert) {
    if (!alert) return;
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-10px)';
    setTimeout(function () {
      if (alert.parentNode) {
        alert.remove();
      }
    }, 200);
  }

  document.querySelectorAll('.alert-close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var alert = this.closest('.alert') || this.closest('[role="alert"]');
      dismissAlert(alert);
    });
  });

  // Auto-dismiss alerts (defaults to 6 seconds)
  document.querySelectorAll('.alert[data-auto-dismiss="true"], [role="alert"][data-auto-dismiss="true"]').forEach(function (alert) {
    var timeout = Number(alert.dataset.timeout || 6000);
    setTimeout(function () {
      if (alert.parentNode) {
        dismissAlert(alert);
      }
    }, timeout);
  });

  // ============================================
  // H10: Welcome banner dismiss
  // ============================================
  var welcomeDismiss = document.querySelector('.welcome-dismiss');
  if (welcomeDismiss) {
    welcomeDismiss.addEventListener('click', function () {
      var banner = this.closest('.welcome-banner');
      if (banner) {
        banner.style.opacity = '0';
        banner.style.transform = 'translateY(-10px)';
        setTimeout(function () {
          banner.remove();
        }, 200);
      }
    });
  }

  // ============================================
  // H5: Password strength indicator
  // ============================================
  var passwordInput = document.getElementById('password');
  var strengthBar = document.querySelector('.password-strength-bar');
  var strengthText = document.querySelector('.password-strength-text');

  if (passwordInput && strengthBar) {
    passwordInput.addEventListener('input', function () {
      var val = this.value;
      var score = 0;

      if (val.length >= 8) score++;
      if (val.length >= 12) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;

      strengthBar.className = 'password-strength-bar';

      if (val.length === 0) {
        strengthBar.style.width = '0%';
        if (strengthText) strengthText.textContent = '';
      } else if (score <= 2) {
        strengthBar.classList.add('weak');
        if (strengthText) {
          strengthText.textContent = 'Débil';
          strengthText.style.color = '#E74C3C';
        }
      } else if (score <= 3) {
        strengthBar.classList.add('medium');
        if (strengthText) {
          strengthText.textContent = 'Aceptable';
          strengthText.style.color = '#F39C12';
        }
      } else {
        strengthBar.classList.add('strong');
        if (strengthText) {
          strengthText.textContent = 'Fuerte';
          strengthText.style.color = '#27AE60';
        }
      }
    });
  }

  // ============================================
  // H1: Submit button loading state
  // ============================================
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      var submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn && !submitBtn.dataset.noLoading) {
        var originalText = submitBtn.textContent;
        submitBtn.setAttribute('aria-busy', 'true');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Enviando...';

        // Restore after 5s in case of issues
        setTimeout(function () {
          submitBtn.removeAttribute('aria-busy');
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }, 5000);
      }
    });
  });

  // ============================================
  // H7: Mobile search toggle
  // ============================================
  var mobileSearchBtn = document.querySelector('.mobile-search-btn');
  var searchGlobal = document.querySelector('.search-global');

  if (mobileSearchBtn && searchGlobal) {
    mobileSearchBtn.addEventListener('click', function () {
      searchGlobal.style.display = searchGlobal.style.display === 'block' ? 'none' : 'block';
      if (searchGlobal.style.display === 'block') {
        searchGlobal.querySelector('input').focus();
      }
    });
  }

  // ============================================
  // Cards clicables de publicaciones
  // ============================================
  document.querySelectorAll('.js-clickable-card[data-click-url]').forEach(function (card) {
    function isInteractiveTarget(target) {
      return Boolean(
        target.closest('a, button, input, textarea, select, label, form, [role="button"]')
      );
    }

    card.addEventListener('click', function (e) {
      if (isInteractiveTarget(e.target)) {
        return;
      }

      var url = card.dataset.clickUrl;
      if (url) {
        window.location.href = url;
      }
    });

    card.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') {
        return;
      }
      if (isInteractiveTarget(e.target)) {
        return;
      }

      e.preventDefault();
      var url = card.dataset.clickUrl;
      if (url) {
        window.location.href = url;
      }
    });
  });

  // ============================================
  // Smooth scroll for anchor links
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ============================================
  // Landing slider
  // ============================================
  var landingSlider = document.querySelector('[data-slider]');

  if (landingSlider) {
    var slides = Array.from(landingSlider.querySelectorAll('[data-slide]'));
    var dots = Array.from(landingSlider.querySelectorAll('[data-slider-dot]'));
    var prevButton = landingSlider.querySelector('[data-slider-prev]');
    var nextButton = landingSlider.querySelector('[data-slider-next]');
    var currentIndex = slides.findIndex(function (slide) {
      return slide.classList.contains('is-active');
    });
    var autoplayId = null;

    if (currentIndex < 0) {
      currentIndex = 0;
    }

    function renderSlide(index) {
      slides.forEach(function (slide, slideIndex) {
        slide.classList.toggle('is-active', slideIndex === index);
      });

      dots.forEach(function (dot, dotIndex) {
        var isActive = dotIndex === index;
        dot.classList.toggle('is-active', isActive);
        dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      currentIndex = index;
    }

    function goToSlide(nextIndex) {
      var normalizedIndex = nextIndex;

      if (nextIndex < 0) {
        normalizedIndex = slides.length - 1;
      }

      if (nextIndex >= slides.length) {
        normalizedIndex = 0;
      }

      renderSlide(normalizedIndex);
    }

    function stopAutoplay() {
      if (autoplayId) {
        window.clearInterval(autoplayId);
        autoplayId = null;
      }
    }

    function startAutoplay() {
      stopAutoplay();
      autoplayId = window.setInterval(function () {
        goToSlide(currentIndex + 1);
      }, 4500);
    }

    if (prevButton) {
      prevButton.addEventListener('click', function () {
        goToSlide(currentIndex - 1);
        startAutoplay();
      });
    }

    if (nextButton) {
      nextButton.addEventListener('click', function () {
        goToSlide(currentIndex + 1);
        startAutoplay();
      });
    }

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        var targetIndex = Number(dot.dataset.slideIndex);
        if (!Number.isNaN(targetIndex)) {
          goToSlide(targetIndex);
          startAutoplay();
        }
      });
    });

    landingSlider.addEventListener('mouseenter', stopAutoplay);
    landingSlider.addEventListener('mouseleave', startAutoplay);
    landingSlider.addEventListener('focusin', stopAutoplay);
    landingSlider.addEventListener('focusout', function (event) {
      if (!landingSlider.contains(event.relatedTarget)) {
        startAutoplay();
      }
    });

    renderSlide(currentIndex);
    startAutoplay();
  }

});
