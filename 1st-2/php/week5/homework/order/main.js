let menu = [
    {
        "name": "奶茶",
        "price": 0,
        "quantity": 0
    },
    {
        "name": "炸雞",
        "price": 0,
        "quantity": 0
    },
    {
        "name": "薯條",
        "price": 0,
        "quantity": 0
    },
]



const tbody = document.querySelector("tbody")


function renderMenu() {
    let menuHtml = ""
    menu.forEach((item) => {
        menuHtml += `
        <tr class="item">
            <td class="item-name">${item.name}</td>
            <td><input class="item-price outline-none text-center bg-transparent border-2 rounded-lg mt-1"value=${item.price} data-name="${item.name}"></td>
            <td>
                <input class="item-quantity bg-transparent text-center outline-none border-2 rounded-lg"  value="${item.quantity}" min="0" data-name="${item.name}" class="quantity">
            </td>
        </tr>
        `
    })
    tbody.innerHTML = menuHtml
}

renderMenu()


document.addEventListener("DOMContentLoaded", () => {
    const member = document.querySelector("#member")
    const orderDetial = document.querySelector("#order-detial")
    const checkButton = document.querySelector("#checkout")
    let itemsHtml = document.querySelectorAll(".item")
    const addNewItem = document.querySelector("#add-new-item")

    function handleAddNewItemButtonClick(e) {
        e.preventDefault()
        const newItemName = document.querySelector("#new-item")
        menu.push({
            "name": newItemName.value,
            "price": 0,
            "quantity": 0
        })

        renderMenu()
        itemsHtml = document.querySelectorAll(".item")
        newItemName.value = ""
    }


    function handleCheckoutButtonClick(e) {
        e.preventDefault()
        let total = 0
        let orderDetialHtml = `<p>親愛的顧客，您點的是：</p>`
        itemsHtml.forEach((item) => {
            const name = item.querySelector(".item-name").textContent
            const price = item.querySelector(".item-price").value
            const quantity = item.querySelector(".item-quantity").value
            const index = menu.findIndex((item) => item.name === name)
            menu[index].price = price
            menu[index].quantity = quantity
            
            if (quantity > 0) {
                orderDetialHtml += `<p>${name} ${price}元 x ${quantity}</p>`
            }
        })
        
        
        menu.forEach((item) => {
            total += item.price * item.quantity
        })
        
        if (member.checked) {
            oldTotal = total
            total = (total * 0.8).toFixed(0)
            orderDetialHtml += `<p>會員折扣 8折：${oldTotal}元 -> ${total}元</p>`
            orderDetialHtml += `<p>總金額：${total}元</p>`
        }else {
            
            orderDetialHtml += `<p>總金額：${total}元</p>`
        }
        if (total == 0 ) {
            orderDetialHtml = `<p>您尚未點餐</p>`
        }
        orderDetial.classList.remove("hidden")

        orderDetial.innerHTML = orderDetialHtml
    }

    function handleQuantityAndPriceChange(e) {
        const name = e.target.dataset.name
        console.log(name)
        const price = e.target.closest(".item").querySelector(".item-price").value
        const quantity = e.target.closest(".item").querySelector(".item-quantity").value
        const index = menu.findIndex((item) => item.name === name)
        menu[index].price = price
        menu[index].quantity = quantity
        console.log(menu)
    }


    checkButton.addEventListener("click", (e) => handleCheckoutButtonClick(e))
    addNewItem.addEventListener("click", (e) => handleAddNewItemButtonClick(e))
    itemsHtml.forEach((item) => {
        item.querySelector(".item-quantity").addEventListener("change", (e) => handleQuantityAndPriceChange(e))
        item.querySelector(".item-price").addEventListener("change", (e) => handleQuantityAndPriceChange(e))
    })
})

