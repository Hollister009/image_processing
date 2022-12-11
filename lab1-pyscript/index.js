if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("sw.js")
    .then((registration) => {
      console.log("SW Registered!");
      console.log(registration);
    })
    .catch((error) => {
      console.log("SW Registration Failed!");
      console.error(error);
    });
}

document.addEventListener("DOMContentLoaded", (event) => {
  // we can move only if we are not in a browser's tab
  isBrowser = matchMedia("(display-mode: browser)").matches;
  if (!isBrowser) {
    window.moveTo(16, 16);
    window.resizeTo(800, 600);
  }
});
