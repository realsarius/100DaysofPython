import Typed from "typed.js";



// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();

    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
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

        if (distance < particleDistance * 1.5 && Math.random() < lineProbability) {
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
      if (mouse.x == undefined || mouse.y == undefined) return;

      let dx = mouse.x - this.x;
      let dy = mouse.y - this.y;
      let distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < mouse.radius) {
        let force = (mouse.radius - distance) / mouse.radius;
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
  window.addEventListener("mouseout", () => {
    mouse.x = undefined;
    mouse.y = undefined;
  });

  function init() {
    resizeReset();
    animationLoop();
  }
};
