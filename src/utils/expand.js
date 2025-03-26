function toggleExpand(event) {
  const button = event.target;
  const memberId = button.closest("div").querySelector("[data-child]").dataset.child;
  const childContainer = document.querySelector(`[data-child="${memberId}"]`);

  if (childContainer) {
    const isHidden = childContainer.classList.toggle("hidden");
    button.textContent = isHidden ? "open" : "roll";
  }
}

function toggleGrayscale(event) {
  const img = event.target.closest("div").querySelector("img");
  img.classList.toggle("grayscale");
}
export { toggleExpand, toggleGrayscale };

