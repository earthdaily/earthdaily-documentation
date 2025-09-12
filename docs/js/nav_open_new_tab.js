document.addEventListener("DOMContentLoaded", function() {

  const link = document.querySelector("nav a[href='https://cropid-demo.aws-dev.geosys.com/']");
  if (link) {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer"); 
  }
});
