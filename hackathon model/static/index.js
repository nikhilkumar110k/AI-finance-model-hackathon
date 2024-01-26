let search = document.querySelector(".searchBar");
let container = document.querySelector(".container");

search.addEventListener("submit", async (e) => {
  e.preventDefault();
  let { ticker } = e.target;
  let data = await fetch("http://localhost:5000/get_stock_data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ticker: ticker.value,
    }),
  })
    .then((d) => d.json())
    .then((d) => d);
  console.log(data);
  let newContainer = `<div class='card-container'>
  <div class='card'>
    <div class='front'>
      <div class='delete x'><i class='fa-solid fa-trash'></i></div>
      <p class='ticker'>${ticker.value}</p>
      <div class='prices'>
        <div class='info'>
          <p>Open</p>
          <p>${Math.floor(data.Openprice * 100) / 100}</p>
        </div>
        <div class='info'>
          <p>Current</p>
          <p class='${data.Openprice > data.currentPrice ? "red" : "green"}'>${
    Math.floor(data.currentPrice * 100) / 100
  }</p>
        </div>
      </div>
      <button class='analyze'>Analyze</button>
    </div>
    <div class='back'><div class='x close'>X</div><p>${
      data.output
    }</p><img src='data:image;base64,${data.plot}'></img></div>
  </div>
</div>`;
  container.innerHTML += newContainer;

  let flips = document.querySelectorAll(".analyze");
  let close = document.querySelectorAll(".close");
  let ds = document.querySelectorAll(".delete");

  let cardContainers = document.querySelectorAll(".card-container");

  flips.forEach((flip, index) => {
    flip.addEventListener("click", () => {
      cardContainers[index].classList.add("analyze");
    });
  });

  close.forEach((c, index) => {
    c.addEventListener("click", () => {
      cardContainers[index].classList.remove("analyze");
    });
  });

  ds.forEach((d, index) => {
    d.addEventListener("click", () => {
      cardContainers[index].remove();
    });
  });

  ticker.value = "";
});
