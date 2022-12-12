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

  const app = new App('root');
  app.init();
});

class App {
  constructor(rootId) {
    this.root = document.getElementById(rootId);
  }

  init() {
    const event = new CustomEvent('ready');

    this.root.innerHTML = this.template;
    this.root.dispatchEvent(event);
  }

  get template() {
    return `
      <aside class="sidePanel">
        <input type="file" name="file" id="file" accept="image/*">
        <button id="openButton" class="btn">Open</button>
        <button id="saveButton" class="btn">Save</button>
      </aside>
      <div class="mainContent">
        <h2>Image Resizer: </h2>
        <div id="previewArea" class="preview">
          <img src="assets/placeholder.jpg" alt="">
        </div>
        <hr class="divider" />
        <fieldset id="dimenssions" class="fieldset">
          <div class="row">
            <label>
              Width:
              <input type="number" name="width" id="width">
            </label>
            <label>
              Height:
              <input type="number" name="height" id="height">
            </label>
            <label>
              Keep ratio:
              <input type="checkbox" name="ratio" id="ratio" checked>
            </label>
          </div>
        </fieldset>
      </div>
    `;
  }
}

