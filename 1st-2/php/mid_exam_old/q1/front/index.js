import GetPage from "./startPage.js"
document.getElementById("app").innerHTML = GetPage()

const pPriceElem = document.querySelector("#p-price")
const pQuantityElem= document.querySelector("#p-quantity")
const ePriceElem = document.querySelector("#e-price")
const eQuantityElem= document.querySelector("#e-quantity")
const moneyElem = document.querySelector("#money")
const resultElem = document.querySelector("#result")


pPriceElem.addEventListener("input", (e) => {
    handleUpdate()
})
pQuantityElem.addEventListener("input", (e) => {
    handleUpdate()
})
ePriceElem.addEventListener("input", (e) => {
    handleUpdate()
})
eQuantityElem.addEventListener("input", (e) => {
    handleUpdate()
})
moneyElem.addEventListener("input", (e)=> {
    handleUpdate()
})

function handleUpdate() {
    const pPrice = pPriceElem.value
    const pQuantity= pQuantityElem.value
    const ePrice = ePriceElem.value
    const eQuantity= eQuantityElem.value
    const total = pPrice * pQuantity + ePrice * eQuantity
    const money = moneyElem.value
    const diff = money - total
    if (money >= total) {
        resultElem.innerHTML = `小明 <span style="color: blue;">剩下${diff}</span>`
    }else {

        resultElem.innerHTML = `小明 <span style="color: red;">不足${diff}</span>`
    }

    
}