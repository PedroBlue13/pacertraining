// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Efeito de scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animar elementos quando entrarem na viewport
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .testimonial-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animate__animated', 'animate__fadeInUp');
            }
        });
    };

    // Executar no carregamento e no scroll
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Adicionar classe ativa à navegação baseada na seção atual
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const sections = document.querySelectorAll('section');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // Efeito de hover para os cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 1rem 3rem rgba(0, 0, 0, 0.175)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1)';
        });
    });

    // Adicionar efeito de parallax ao hero
    window.addEventListener('scroll', function() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const scrollPosition = window.pageYOffset;
            heroSection.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        }
    });

    // Contador de números animado
    function animateCounter(element, target, duration) {
        let start = 0;
        const startTime = performance.now();
        
        function updateCount(currentTime) {
            const elapsedTime = currentTime - startTime;
            if (elapsedTime > duration) {
                element.textContent = target;
                return;
            }
            
            const progress = elapsedTime / duration;
            const current = Math.round(progress * target);
            element.textContent = current;
            requestAnimationFrame(updateCount);
        }
        
        requestAnimationFrame(updateCount);
    }

    // Ativar contador quando elementos estiverem visíveis
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const observerOptions = {
            threshold: 0.5
        };
        
        const observer = new IntersectionObserver(function(entries, observer) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-target'));
                    animateCounter(entry.target, target, 2000);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
});