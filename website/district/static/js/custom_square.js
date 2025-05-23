document.addEventListener("DOMContentLoaded", function() {
  const container = document.getElementById('rain-container');
    const totalSquares = 50;

    for (let i = 0; i < totalSquares; i++) {
      const square = document.createElement("div");
      square.className = "w-2 h-2 bg-cyan-300 opacity-50 absolute falling-square";

      square.style.left = Math.random() * 100 + "%";
      square.style.top = "-" + 600 + "px";
      square.style.animationDelay = (Math.random() * 10) + "s";
      square.style.animationDuration = (5 + Math.random() * 15) + "s";

      container.appendChild(square);
    }

});