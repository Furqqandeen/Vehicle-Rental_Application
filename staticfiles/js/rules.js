const checkbox = document.getElementById("acceptRules");
const proceedBtn = document.getElementById("proceedBtn");

checkbox.addEventListener("change", function () {
    proceedBtn.disabled = !this.checked;
});




