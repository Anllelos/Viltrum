document.addEventListener("DOMContentLoaded", function () {
  const userIcon = document.getElementById("userIcon");
  const dropdownMenu = document.getElementById("dropdownMenu");
  const notifyIcon = document.getElementById("notifyIcon");
  const dropdownMenuNotify = document.getElementById("dropdownMenuNotify");

  userIcon.addEventListener("click", function (event) {
      event.preventDefault();
      const isOpen = dropdownMenu.classList.toggle("show");
      userIcon.setAttribute("aria-expanded", isOpen);
      // Evita que el evento de clic en el documento cierre el dropdown inmediatamente
      event.stopPropagation();
  });

  notifyIcon.addEventListener("click", function (event) {
      event.preventDefault();
      const isOpen = dropdownMenuNotify.classList.toggle("show");
      notifyIcon.setAttribute("aria-expanded", isOpen);
      // Evita que el evento de clic en el documento cierre el dropdown inmediatamente
      event.stopPropagation();
  });

  document.addEventListener("click", function (event) {
      // Cierra los dropdowns si se hace clic fuera de ellos
      if (!userIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
          dropdownMenu.classList.remove("show");
          userIcon.setAttribute("aria-expanded", "false");
      }

      if (!notifyIcon.contains(event.target) && !dropdownMenuNotify.contains(event.target)) {
          dropdownMenuNotify.classList.remove("show");
          notifyIcon.setAttribute("aria-expanded", "false");
      }
  });
});
