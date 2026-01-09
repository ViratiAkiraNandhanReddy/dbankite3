// Scroll Progress Bar
window.addEventListener("scroll", () => {
  const h = document.documentElement.scrollHeight - innerHeight;
  document.querySelector(".scroll-progress").style.width =
    (scrollY / h) * 100 + "%";
});

// Hamburger Menu Logic
const hamburger = document.getElementById('hamburger-btn');
const mobileMenu = document.getElementById('mobile-menu');

// Toggle menu
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('active');
  // Prevent body scroll when menu is open
  document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : 'auto';
});

// Close mobile menu when a link is clicked
document.querySelectorAll('.mobile-menu a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('active');
    document.body.style.overflow = 'auto';
  });
});

// Scroll Reveal Animation
const revealElements = document.querySelectorAll(".reveal");

const revealOnScroll = () => {
  const windowHeight = window.innerHeight;
  const elementVisible = 100; // Trigger slightly earlier

  revealElements.forEach((reveal) => {
    const elementTop = reveal.getBoundingClientRect().top;
    if (elementTop < windowHeight - elementVisible) {
      reveal.classList.add("active");
    }
  });
};

window.addEventListener("scroll", revealOnScroll);
// Trigger once on load to show initial sections
revealOnScroll();