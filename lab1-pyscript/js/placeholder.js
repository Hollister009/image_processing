class Placeholder {
  static init(canvas) {
    const ctx = canvas.getContext("2d");
    const base_image = new Image();

    base_image.src = "assets/placeholder.jpg";
    base_image.onload = function () {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(
        base_image,
        0,
        0,
        base_image.width,
        base_image.height, // source rectangle
        0,
        0,
        canvas.width,
        canvas.height
      ); // destination rectangle
    };
  }
}
