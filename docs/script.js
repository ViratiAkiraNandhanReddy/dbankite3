// Smooth scroll for all navigation links
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Highlight active section in navigation
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.querySelectorAll('.sidebar a, .nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${entry.id}`) {
          link.classList.add('active');
        }
      });
    }
  });
}, {
  threshold: 0.3
});

document.querySelectorAll('section').forEach(section => {
  observer.observe(section);
});

// Add scroll effect to navbar
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  if (scrollTop > 100) {
    navbar.style.boxShadow = '0 4px 20px rgba(56, 189, 248, 0.1)';
  } else {
    navbar.style.boxShadow = 'none';
  }
  
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Mobile menu toggle (future enhancement)
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => {
    document.querySelector('.nav-menu').classList.toggle('active');
  });
}

// Add animation to elements on scroll
const animateOnScroll = () => {
  const elements = document.querySelectorAll('.feature-card, .tech-card, .roadmap-item');
  
  elements.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100) {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }
  });
};

// Initialize animations
document.querySelectorAll('.feature-card, .tech-card, .roadmap-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'all 0.6s ease-out';
});

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

// Copy code on click
document.querySelectorAll('pre code').forEach(codeBlock => {
  const pre = codeBlock.parentElement;
  const button = document.createElement('button');
  button.textContent = 'Copy';
  button.className = 'copy-btn';
  button.style.cssText = `
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 6px 12px;
    background: rgba(56, 189, 248, 0.2);
    border: 1px solid rgba(56, 189, 248, 0.5);
    color: #38bdf8;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.3s;
  `;
  
  button.addEventListener('mouseover', () => {
    button.style.background = 'rgba(56, 189, 248, 0.3)';
  });
  
  button.addEventListener('mouseout', () => {
    button.style.background = 'rgba(56, 189, 248, 0.2)';
  });
  
  button.addEventListener('click', () => {
    const text = codeBlock.textContent;
    navigator.clipboard.writeText(text).then(() => {
      button.textContent = 'Copied!';
      setTimeout(() => {
        button.textContent = 'Copy';
      }, 2000);
    });
  });
  
  pre.style.position = 'relative';
  pre.appendChild(button);
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelector('.nav-menu')?.classList.remove('active');
  }
});
