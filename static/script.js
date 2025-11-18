// script.js - copy, search, show toggle, dark mode, delete confirmation

document.addEventListener("DOMContentLoaded", function(){

  // SEARCH functionality
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function(){
      const q = this.value.trim().toLowerCase();
      const rows = document.querySelectorAll("#pwTable tbody tr");
      rows.forEach(r => {
        const website = r.querySelector(".pw-website").innerText.toLowerCase();
        const username = r.querySelector(".pw-username").innerText.toLowerCase();
        if (!q || website.includes(q) || username.includes(q)) {
          r.style.display = "";
        } else {
          r.style.display = "none";
        }
      });
    });
  }

  // SHOW / HIDE toggle
  document.querySelectorAll(".show-btn").forEach(btn => {
    btn.addEventListener("click", function(){
      const id = this.getAttribute("data-id");
      const span = document.getElementById("p"+id);
      if (!span) return;
      if (span.classList.contains("masked")) {
        span.classList.remove("masked");
        span.classList.add("unmasked");
        span.innerText = span.dataset.real;
        this.innerText = "Hide";
      } else {
        span.classList.remove("unmasked");
        span.classList.add("masked");
        span.innerText = "********";
        this.innerText = "Show";
      }
    });
  });

  // COPY to clipboard
  document.querySelectorAll(".copy-btn").forEach(btn => {
    btn.addEventListener("click", async function(){
      const id = this.getAttribute("data-id");
      const span = document.getElementById("p"+id);
      if (!span) return;
      try {
        await navigator.clipboard.writeText(span.dataset.real);
        this.innerText = "Copied";
        setTimeout(()=> this.innerText = "Copy", 1200);
      } catch (e) {
        alert("Copy failed. Select and copy manually.");
      }
    });
  });

  // DELETE confirmation
  document.querySelectorAll(".delete-link").forEach(a=>{
    a.addEventListener("click", function(e){
      if(!confirm("Delete this entry? This action cannot be undone.")){
        e.preventDefault();
      }
    });
  });

  // DARK MODE toggle (stored in localStorage)
  const darkBtn = document.getElementById("darkToggle");
  function applyTheme(theme){
    if(theme === "dark"){
      document.documentElement.classList.add("dark");
      if(darkBtn) darkBtn.innerText = "Light";
    } else {
      document.documentElement.classList.remove("dark");
      if(darkBtn) darkBtn.innerText = "Dark";
    }
  }
  const saved = localStorage.getItem("pw_theme") || "light";
  applyTheme(saved);

  if(darkBtn) {
    darkBtn.addEventListener("click", function(){
      const current = document.documentElement.classList.contains("dark") ? "dark" : "light";
      const next = current === "dark" ? "light" : "dark";
      localStorage.setItem("pw_theme", next);
      applyTheme(next);
    });
  }

});
