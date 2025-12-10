document.addEventListener('DOMContentLoaded', function() {
  const features = document.querySelectorAll('.mdx-spotlight__feature');
  let currentIndex = 0;
  
  // Show first 3, hide rest
  features.forEach((feature, index) => {
    if (index >= 3) {
      feature.setAttribute('hidden', '');
    }
  });
  
  // Rotate every 5 seconds
  setInterval(() => {
    // Hide current last feature
    features[currentIndex + 2].setAttribute('hidden', '');
    
    // Show next feature
    currentIndex = (currentIndex + 1) % (features.length - 2);
    features[currentIndex + 2].removeAttribute('hidden');
  }, 5000);
});