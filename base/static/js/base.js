const menuIcon = document.getElementById("menuIcon");
const dropdownMenu = document.getElementById("dropdownMenu");

// Toggle dropdown on icon click
menuIcon.addEventListener("click", (e) => {
    e.stopPropagation(); // prevent the click from bubbling to window
    dropdownMenu.classList.toggle("show");
});

// Prevent dropdown clicks from closing immediately
dropdownMenu.addEventListener("click", (e) => {
    e.stopPropagation();
});

// Close dropdown if clicked outside
window.addEventListener("click", () => {
    dropdownMenu.classList.remove("show");
});
