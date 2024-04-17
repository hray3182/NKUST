
const table = document.querySelector("tbody")
function randomNumber() {
  return Math.round(Math.random() * 100)
}
let rowHtml = ""
for (let i = 0; i < 50; i++) {
  rowHtml += `
  <tr class="hover:bg-sky-600">
  <td class="">${i + 1}</td>
  <td class=" chi">${randomNumber()}</td>
  <td class=" eng">${randomNumber()}</td>
  <td class=" math">${randomNumber()}</td>
  <td class=" com">${randomNumber()}</td>
  <td class=" row-total"></td>
  <td class=" row-avg"></td>
  </tr>
  `
}

table.insertAdjacentHTML("beforeend", rowHtml)

document.addEventListener("DOMContentLoaded", () => {
  let chiTotal = 0
  let engTotal = 0
  let mathTotal = 0
  let comTotal = 0
  let allAvg = 0
  document.querySelectorAll("tr").forEach((row, index) => {
    if (index == 0 || index > 50) {
      return
    }
    const chi = parseInt(row.querySelector("td.chi").textContent)
    const eng = parseInt(row.querySelector(".eng").textContent)
    const math = parseInt(row.querySelector(".math").textContent)
    const com = parseInt(row.querySelector(".com").textContent)

    chiTotal += chi
    engTotal += eng
    mathTotal += math
    comTotal += com

    const rowTotal = row.querySelector(".row-total")
    const rowAvg = row.querySelector(".row-avg")

    const total = chi + eng + math + com
    const avg = total / 4
    allAvg += avg

    rowTotal.textContent = total
    rowAvg.textContent = avg.toFixed(2)

    if (avg > 60) {
      rowAvg.classList.add("text-green-200")
    } else {
      rowAvg.classList.add("text-red-200")
    }

  })
  const chiAvg = chiTotal / 50
  const engAvg = engTotal / 50
  const mathAvg = mathTotal / 50
  const comAvg = comTotal / 50
  allAvg = (allAvg / 50).toFixed(2)
  const passClass = "text-green-200"
  const failClass = "text-red-200"
  const totalTr = `<tr><td>科目總分</td><td>${chiTotal}</td><td>${engTotal}</td><td>${mathTotal}</td><td>${comTotal}</tr>`
  const avgTr = `<tr><td>平均</td><td>${chiAvg.toFixed(2)}</td><td>${engAvg.toFixed(2)}</td><td>${mathAvg.toFixed(2)}</td><td>${comAvg.toFixed(2)}</td><td>${allAvg}</td><td>${allAvg}</td></tr>`
  // table.insertAdjacentHTML("beforeend", totalTr)
  table.insertAdjacentHTML("beforeend", avgTr)
})