import { items, GetPage } from "./startPage.js"
document.getElementById("app").innerHTML = GetPage()

const itemsElem = Array.from(document.querySelectorAll("#items td"))
const checkoutElem = document.querySelector("#checkout")
let selectedItem = {}


document.addEventListener("DOMContentLoaded", () => {
    for (let i = 0; i < itemsElem.length; i++) {
        itemsElem[i].addEventListener("click", () => handleItemClick(i))
    }
})



function handleItemClick(id) {
    console.log(id)
    const checkoutHtml = `
        <table>
            <thead>
                <tr>
                    <td></td>
                    <td>單價</td>
                    <td>數量</td>
                </tr>
                <tr>
                    <td>${items[id].name}</td>
                    <td>${items[id].price}</td>
                    <td><input type="text" id="quantity"></td>
                </tr>
            </thead>
        </table>
        <input type="radio" name="payment" value="cash" checked>
        <span>現金</span>
        <input type="radio" name="payment" value="stored">
        <span>儲值金</span>
        <input type="radio" name="payment" value="point">
        <span>福利點數</span>
        <br>
        <span>現有儲值金</span>
        <input type="text" id="stored-fund">
        <span>現有福利點數</span>
        <input type="text" id="point-fund">
        <br>
        <button id="checkout-btn">計算</button>
`
    checkoutElem.innerHTML = checkoutHtml
    selectedItem = items[id]

    const checkoutButton = document.querySelector("#checkout-btn")
    checkoutButton.addEventListener("click", () => handleButtonClick())
    const storedFundElem = document.querySelector("#stored-fund")
    const pointFundElem = document.querySelector("#point-fund")
    const quantityElem = document.querySelector("#quantity")

    function handleButtonClick() {
        const quantity = quantityElem.value
        const cost = selectedItem.price * quantity
        const storedFund = storedFundElem.value
        let pointFund = parseInt(pointFundElem.value)
        const radios = document.getElementsByName("payment")
        const resultElem = document.querySelector("#result")
        let payment = ""
        let canBuy = true
        if (isNaN(pointFund)) {
            pointFund = 0
        }
        if (isNaN(storedFund)) {
            pointFund = 0
        }
        radios.forEach(r => {
            if (r.checked) {
                payment = r.value
            }
        })
        if (payment === "cash") {
            pointFund += 5
        }
        if (payment === "stored") {
            if (storedFund < cost) {
                canBuy = false
            }else {
                pointFund += 10
                total *= 0.9
            }
        }
        if (payment === "point") {
            if (pointFund < cost) {
                canBuy = false
            }
        }

        const resultHtml = `
        <p style="color:${canBuy? "green": "red"};">${canBuy? "可以購買": "金額不足"}</p>
        <p>現有福利點數${pointFund}</p>
        `
        resultElem.innerHTML = resultHtml
    }
}
