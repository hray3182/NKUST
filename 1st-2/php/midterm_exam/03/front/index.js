import GetPage from "./startPage.js"

document.querySelector("#app").innerHTML = GetPage()
document.querySelector("#cal").addEventListener("click", handleClick)

function handleClick() {
    let total = 0
    Array.from(document.querySelectorAll("tr")).forEach(tr => {
        if (tr.children[1].textContent === "單價") {
            return
        }
        const currentTotal = parseInt(tr.children[1].textContent) * parseInt(tr.children[2].textContent)
        total += currentTotal
    })
    document.querySelector("#total").innerHTML = `共計: ${total} 元`
    let currentMoney = parseInt(document.querySelector("#money").value)
    if (isNaN(currentMoney)) {
        currentMoney = 0
    }
    const resultElem = document.querySelector("#result")
    if (currentMoney > total) {
        resultElem.innerHTML = `剩下: ${currentMoney - total} 元`
        resultElem.style = "color: blue"
    }
    else if (currentMoney < total) {
        resultElem.innerHTML = `不足: ${total - currentMoney} 元`
        resultElem.style = "color: red"
    }
    else {
        resultElem.innerHTML = `不用找錢`
    }

}