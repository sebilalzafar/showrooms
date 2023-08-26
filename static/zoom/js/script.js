const image = document.getElementById("image");
const magnifier = document.querySelector(".magnifier");

image.addEventListener("mousemove", (e) => {
    const { offsetX, offsetY } = e;
    const { offsetWidth, offsetHeight } = image;
    const { width, height } = magnifier.getBoundingClientRect();

    const x = (offsetX / offsetWidth) * 100;
    const y = (offsetY / offsetHeight) * 100;

    magnifier.style.backgroundImage = `url('${image.src}')`;
    magnifier.style.backgroundPosition = `-${x}% -${y}%`;
    magnifier.style.left = `${e.pageX - width / 2}px`;
    magnifier.style.top = `${e.pageY - height / 2}px`;
    magnifier.style.visibility = "visible";
});

image.addEventListener("mouseleave", () => {
    magnifier.style.visibility = "hidden";
});
