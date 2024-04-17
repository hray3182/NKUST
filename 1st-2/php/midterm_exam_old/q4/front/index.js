import GetPage from "./startPage.js"
document.getElementById("app").innerHTML = GetPage()

document.querySelector("#cal").addEventListener("click", ()=>handleButtonClick())

function handleButtonClick() {
    let janIncome = 0
    let janProfit = 0
    let febIncome = 0
    let febProfit = 0 
    let marIncome = 0
    let marProfit = 0
    Array.from(document.querySelectorAll(".detial")).forEach(e => {
        const currJanCost = parseInt(e.querySelector(".jan.cost").textContent) * parseInt(e.querySelector(".jan.quantity").textContent)
        const currJanIncome = parseInt(e.querySelector(".jan.price").textContent) * parseInt(e.querySelector(".jan.quantity").textContent)
        janProfit += currJanIncome - currJanCost
        janIncome += currJanIncome
        const currFebCost = parseInt(e.querySelector(".feb.cost").textContent)* parseInt(e.querySelector(".feb.quantity").textContent)
        const currFebIncome = parseInt(e.querySelector(".feb.price").textContent)* parseInt(e.querySelector(".feb.quantity").textContent)
        febProfit += currFebIncome - currFebCost
        febIncome += currFebIncome
        const currMarCost = parseInt(e.querySelector(".mar.cost").textContent)* parseInt(e.querySelector(".mar.quantity").textContent)
        const currMarIncome = parseInt(e.querySelector(".mar.price").textContent)* parseInt(e.querySelector(".mar.quantity").textContent)
        marProfit += currMarIncome - currMarCost
        marIncome += currMarIncome
    })
    const totalIncome = janIncome + febIncome + marIncome
    const totalProfit = janProfit + febProfit + marProfit
    document.querySelector(".jan.income").innerHTML = janIncome
    document.querySelector(".jan.profit").innerHTML = janProfit
    document.querySelector(".feb.income").innerHTML = febIncome
    document.querySelector(".feb.profit").innerHTML = febProfit
    document.querySelector(".mar.income").innerHTML = marIncome
    document.querySelector(".mar.profit").innerHTML = marProfit
    document.querySelector(".total-income").innerHTML = totalIncome
    document.querySelector(".total-profit").innerHTML = totalProfit
}