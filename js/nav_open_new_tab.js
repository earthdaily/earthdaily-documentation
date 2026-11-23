document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("a[href^='http']").forEach(link => {
    if (!link.href.startsWith(window.location.origin)) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  });
});
