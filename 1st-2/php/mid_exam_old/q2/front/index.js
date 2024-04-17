import GetPage from "./startPage.js"
document.getElementById("app").innerHTML = GetPage()

const buyElem = document.querySelector("#buy")
const sellElem = document.querySelector("#sell")
const resultElem = document.querySelector("#result")
buyElem.addEventListener("input", ()=>handleUpdate())
sellElem.addEventListener("input", ()=>handleUpdate())

function handleUpdate() {
    const buy = buyElem.value
    const sell = sellElem.value
    let profitRate = 0 
    if (buy != 0 && sell != 0) {
        profitRate = (sell - buy - 0.001425 * buy - 0.004425 * sell) / buy
    }
    resultElem.innerHTML = `${profitRate.toFixed(4)*100}%`
}