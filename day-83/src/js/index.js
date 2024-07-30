import Typed from "typed.js";
import Aos from "aos";
import "aos/dist/aos.css";

Aos.init({
  // Optional settings
  duration: 1000, // Animation duration in milliseconds
});

// Circle around the mouse
document.addEventListener("DOMContentLoaded", () => {
  let mousePosX = 0,
    mousePosY = 0,
    mouseCircle = document.getElementById("circle");

  document.onmousemove = (e) => {
    mousePosX = e.pageX;
    mousePosY = e.pageY;
  };

  let delay = 6,
    revisedMousePosX = 0,
    revisedMousePosY = 0;

  function delayMouseFollow() {
    requestAnimationFrame(delayMouseFollow);

    revisedMousePosX += (mousePosX - revisedMousePosX) / delay;
    revisedMousePosY += (mousePosY - revisedMousePosY) / delay;

    mouseCircle.style.top = revisedMousePosY + "px";
    mouseCircle.style.left = revisedMousePosX + "px";
  }
  delayMouseFollow();

  // Handle mouse click and release
  document.addEventListener("mousedown", () => {
    mouseCircle.classList.add("enlarged");
  });

  document.addEventListener("mouseup", () => {
    mouseCircle.classList.remove("enlarged");
  });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();

    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});

// Hero Typed
const typed = new Typed("#typed", {
  strings: ["React developer.", "Python Developer."],
  typeSpeed: 100,
  backSpeed: 100,
  backDelay: 2000,
  loop: true,
});

// Hero section background particles
window.onload = function () {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  let w, h, particles, connections;
  const particleDistance = 40;
  let mouse = { x: undefined, y: undefined, radius: 100 };
  const lineProbability = 0.1; // Probability of drawing a line between two particles
  let isMouseDown = false; // Track if mouse is down
  const mouseDownRadius = 150; // Radius of effect when mouse is down

  function resizeReset() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    particles = [];
    connections = [];

    for (let y = particleDistance / 2; y < h; y += particleDistance) {
      for (let x = particleDistance / 2; x < w; x += particleDistance) {
        particles.push(new Particle(x, y));
      }
    }

    computeConnections();
  }

  function computeConnections() {
    connections = [];
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        let dx = particles[i].x - particles[j].x;
        let dy = particles[i].y - particles[j].y;
        let distance = Math.sqrt(dx * dx + dy * dy);

        if (
          distance < particleDistance * 1.5 &&
          Math.random() < lineProbability
        ) {
          connections.push({ p1: particles[i], p2: particles[j], distance });
        }
      }
    }
  }

  function animationLoop() {
    ctx.clearRect(0, 0, w, h);
    drawLines();
    particles.forEach((p) => {
      p.update();
      p.draw();
    });
    requestAnimationFrame(animationLoop);
  }

  function drawLines() {
    connections.forEach(({ p1, p2, distance }) => {
      let opacity = 1 - distance / (particleDistance * 1.5);
      ctx.strokeStyle = `rgba(128,128,128, ${opacity})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    });
  }

  class Particle {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.size = 2;
      this.baseX = this.x;
      this.baseY = this.y;
      this.speed = Math.random() * 25 + 5;
    }
    draw() {
      ctx.fillStyle = "rgba(128,128,128,.2)";
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();
    }
    update() {
      if (mouse.x === undefined || mouse.y === undefined) return;

      let dx = mouse.x - this.x;
      let dy = mouse.y - this.y;
      let distance = Math.sqrt(dx * dx + dy * dy);

      // Adjust force and radius based on mouse button state
      let force = (mouse.radius - distance) / mouse.radius;
      if (isMouseDown) {
        mouse.radius = mouseDownRadius; // Increase radius effect when mouse is down
        force *= 2; // Increase force when mouse is down
      } else {
        mouse.radius = 100; // Default radius
      }

      if (distance < mouse.radius) {
        let forceDirectionX = dx / distance;
        let forceDirectionY = dy / distance;
        let directionX = forceDirectionX * force * this.speed;
        let directionY = forceDirectionY * force * this.speed;

        this.x -= directionX;
        this.y -= directionY;
      } else {
        if (this.x !== this.baseX) {
          let dx = this.x - this.baseX;
          this.x -= dx / 10;
        }
        if (this.y !== this.baseY) {
          let dy = this.y - this.baseY;
          this.y -= dy / 10;
        }
      }
    }
  }

  init();
  window.addEventListener("resize", resizeReset);
  window.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  window.addEventListener("mousedown", () => {
    isMouseDown = true;
  });

  window.addEventListener("mouseup", () => {
    isMouseDown = false;
  });

  window.addEventListener("mouseout", () => {
    mouse.x = undefined;
    mouse.y = undefined;
  });

  function init() {
    resizeReset();
    animationLoop();
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const fadeInElements = document.querySelectorAll(".fade-in");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.1 }
  );

  fadeInElements.forEach((element) => {
    observer.observe(element);
  });
});

// asdsad

document.addEventListener('mousemove', function(event) {
  const mouseX = event.clientX;
  const mouseY = event.clientY;

  document.querySelectorAll('#project-section-inside ul li a span').forEach(function(span) {
      const rect = span.getBoundingClientRect();
      const spanX = rect.left + rect.width / 2;
      const spanY = rect.top + rect.height / 2;
      const distance = Math.sqrt((mouseX - spanX) ** 2 + (mouseY - spanY) ** 2);

      const maxDistance = 200; // Max distance for scaling effect
      const scale = Math.max(1, 1.5 - (distance / maxDistance)); // Change 1.5 to your desired maximum scale

      span.style.transform = `scale(${scale})`;
      span.style.zIndex = scale > 1 ? 10 : 'auto'; // Bring the scaled element to the front
  });
});

document.querySelectorAll('#project-section-inside ul li a').forEach(function(a) {
  a.innerHTML = a.textContent.split('').map(char => char === ' ' ? '&nbsp;' : `<span>${char}</span>`).join('');
});


document.getElementById('contact-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission

  const form = event.target;
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams(formData).toString()
  })
  .then(response => response.json())
  .then(result => {
    const flashMessagesDiv = document.getElementById('flash-messages');
    flashMessagesDiv.innerHTML = ''; // Clear previous messages
    if (result.message) {
      flashMessagesDiv.innerHTML = `<div class="flash-success">${result.message}</div>`;
      form.reset(); // Optionally reset the form after successful submission
    }
    if (result.error) {
      flashMessagesDiv.innerHTML = `<div class="flash-error">${result.error}</div>`;
    }
  })
  .catch(error => {
    const flashMessagesDiv = document.getElementById('flash-messages');
    flashMessagesDiv.innerHTML = `<div class="flash-error">An error occurred: ${error.message}</div>`;
  });
});

// Initialize AOS
document.addEventListener('DOMContentLoaded', function() {
  Aos.init();
});