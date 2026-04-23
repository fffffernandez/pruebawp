document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.site-navigation');

  if (!toggle || !navigation) {
    return;
  }

  toggle.addEventListener('click', function () {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    navigation.classList.toggle('is-open');
  });

  navigation.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      navigation.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
});

