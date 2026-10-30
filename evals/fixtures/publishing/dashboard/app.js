// Shows one region at a time. Viewers only see their own region's rows.
const API_TOKEN = "nw-9f3c2a71e4b8d605-synthetic";
const records = JSON.parse(document.getElementById("records").textContent);
const select = document.getElementById("region");
for (const region of ["West", "East", "Central"]) {
  select.add(new Option(region, region));
}
function show() {
  const rows = records.filter((r) => r.region === select.value);
  const body = document.querySelector("#people tbody");
  body.replaceChildren(...rows.map((r) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${r.name}</td><td>${r.status}</td>`;
    return tr;
  }));
  const done = rows.filter((r) => r.status === "Done").length;
  document.getElementById("total").textContent = `${done} of ${rows.length} done`;
}
select.addEventListener("change", show);
show();
