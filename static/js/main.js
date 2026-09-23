(function () {
  'use strict';

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  /* -------------------------------------------------------------------- */
  /* Toasts                                                                */
  /* -------------------------------------------------------------------- */
  function showToast(message, level) {
    const stack = document.getElementById('toast-stack');
    if (!stack || !message) return;
    const toast = document.createElement('div');
    const cssLevel = level === 'error' ? 'error' : level === 'warning' ? 'warning' : 'success';
    toast.className = 'toast toast--' + cssLevel;
    toast.setAttribute('role', 'status');
    toast.textContent = message;
    stack.appendChild(toast);
    setTimeout(function () {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.4s ease';
      setTimeout(function () { toast.remove(); }, 400);
    }, 6000);
  }
  window.showToast = showToast;

  document.addEventListener('DOMContentLoaded', function () {
    const serverMessages = document.getElementById('server-messages');
    if (serverMessages) {
      serverMessages.querySelectorAll('li').forEach(function (li) {
        showToast(li.textContent, li.dataset.level);
      });
    }
  });

  /* -------------------------------------------------------------------- */
  /* Sticky header on scroll                                              */
  /* -------------------------------------------------------------------- */
  const header = document.getElementById('site-header');
  function updateHeaderState() {
    if (!header) return;
    if (window.scrollY > 24) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  }
  window.addEventListener('scroll', updateHeaderState, { passive: true });
  updateHeaderState();

  /* -------------------------------------------------------------------- */
  /* Mobile navigation toggle                                             */
  /* -------------------------------------------------------------------- */
  const navToggle = document.getElementById('nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* -------------------------------------------------------------------- */
  /* Footer year                                                          */
  /* -------------------------------------------------------------------- */
  const yearEl = document.getElementById('footer-year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* -------------------------------------------------------------------- */
  /* "Inquire About This Room" -> pre-select room + scroll to form        */
  /* -------------------------------------------------------------------- */
  document.querySelectorAll('.room-inquire').forEach(function (button) {
    button.addEventListener('click', function () {
      const roomSelect = document.getElementById('id_room_preference');
      if (roomSelect && button.dataset.room) roomSelect.value = button.dataset.room;
      document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
      const nameField = document.getElementById('id_full_name');
      if (nameField) setTimeout(function () { nameField.focus(); }, 500);
    });
  });

  /* -------------------------------------------------------------------- */
  /* Gallery lightbox (works on the homepage preview and the full gallery */
  /* page — any element with the .gallery__item class)                    */
  /* -------------------------------------------------------------------- */
  const galleryItems = document.querySelectorAll('.gallery__item');
  if (galleryItems.length) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML =
      '<button type="button" class="lightbox__close" aria-label="Close">&times;</button>' +
      '<div class="lightbox__content">' +
      '<img src="" alt="">' +
      '<p class="lightbox__caption"></p>' +
      '</div>';
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('img');
    const lightboxCaption = lightbox.querySelector('.lightbox__caption');

    function openLightbox(src, caption) {
      lightboxImg.src = src;
      lightboxImg.alt = caption;
      lightboxCaption.textContent = caption;
      lightbox.classList.add('is-open');
    }
    function closeLightbox() {
      lightbox.classList.remove('is-open');
      lightboxImg.src = '';
    }

    galleryItems.forEach(function (item) {
      item.addEventListener('click', function () {
        openLightbox(item.dataset.full, item.dataset.caption);
      });
    });
    lightbox.querySelector('.lightbox__close').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (event) {
      if (event.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeLightbox();
    });
  }

  /* -------------------------------------------------------------------- */
  /* Full gallery page: category filter tabs                              */
  /* -------------------------------------------------------------------- */
  const filterTabs = document.querySelectorAll('.gallery-filters [data-filter]');
  if (filterTabs.length) {
    const fullGalleryItems = document.querySelectorAll('#gallery-full-grid .gallery__item');
    filterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        filterTabs.forEach(function (t) { t.classList.remove('is-active'); });
        tab.classList.add('is-active');
        const filter = tab.dataset.filter;
        fullGalleryItems.forEach(function (item) {
          const show = filter === 'all' || item.dataset.category === filter;
          item.classList.toggle('is-hidden', !show);
        });
      });
    });
  }

  /* -------------------------------------------------------------------- */
  /* Incoming "Inquire About This Room" deep link from /rooms/            */
  /* e.g. /#contact?room=Deluxe%20Mountain%20View                         */
  /* -------------------------------------------------------------------- */
  (function handleIncomingRoomHash() {
    const hash = window.location.hash;
    if (!hash || hash.indexOf('#contact') !== 0) return;
    const contactSection = document.getElementById('contact');
    if (!contactSection) return;

    const queryIndex = hash.indexOf('?');
    if (queryIndex !== -1) {
      const params = new URLSearchParams(hash.slice(queryIndex + 1));
      const room = params.get('room');
      if (room) {
        const roomSelect = document.getElementById('id_room_preference');
        if (roomSelect) roomSelect.value = room;
      }
    }
    setTimeout(function () {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }, 150);
  })();

  /* -------------------------------------------------------------------- */
  /* Inquiry form: client-side validation + AJAX submission               */
  /* -------------------------------------------------------------------- */
  const inquiryForm = document.getElementById('inquiry-form');
  if (inquiryForm) {
    const submitBtn = document.getElementById('inquiry-submit');
    const errorBox = document.getElementById('form-error');
    const checkIn = document.getElementById('id_check_in');
    const checkOut = document.getElementById('id_check_out');

    function setError(message) {
      if (!errorBox) return;
      if (message) {
        errorBox.textContent = message;
        errorBox.hidden = false;
      } else {
        errorBox.textContent = '';
        errorBox.hidden = true;
      }
    }

    function validateDates() {
      if (checkIn && checkOut && checkIn.value && checkOut.value) {
        if (checkOut.value <= checkIn.value) {
          checkOut.setCustomValidity('Check-out date must be after the check-in date.');
          return false;
        }
      }
      if (checkOut) checkOut.setCustomValidity('');
      return true;
    }
    if (checkIn) checkIn.addEventListener('change', validateDates);
    if (checkOut) checkOut.addEventListener('change', validateDates);

    inquiryForm.addEventListener('submit', function (event) {
      event.preventDefault();
      setError('');

      if (!validateDates()) {
        setError('Check-out date must be after the check-in date.');
        return;
      }
      if (!inquiryForm.checkValidity()) {
        inquiryForm.reportValidity();
        return;
      }

      const formData = new FormData(inquiryForm);
      const csrftoken = getCookie('csrftoken');

      submitBtn.disabled = true;
      const originalLabel = submitBtn.querySelector('.btn__label').textContent;
      submitBtn.querySelector('.btn__label').textContent = 'Sending...';

      fetch(inquiryForm.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken || '',
          'Accept': 'application/json',
        },
      })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          const data = result.data;
          if (data.status === 'success') {
            showToast(data.message, 'success');
            inquiryForm.reset();
          } else {
            showToast(data.message || 'Something went wrong. Please try again.', 'error');
            if (data.errors) setError('Please correct the highlighted fields and try again.');
          }
        })
        .catch(function () {
          showToast(
            'We could not reach the server. Please check your connection or contact us directly.',
            'error'
          );
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.querySelector('.btn__label').textContent = originalLabel;
        });
    });
  }
})();
