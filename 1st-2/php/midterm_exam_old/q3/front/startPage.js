const items = [
    {
        id: 1,
        name: "東芝 58 型",
        price: "12999"
    },
    {
        id: 2,
        name: "JVC 50 型",
        price: "10988"
    },
    {
        id: 3,
        name: "小米 65 型",
        price: "15990"
    },
    {
        id: 4,
        name: "禾聯 55型",
        price: "9999"
    },
    {
        id: 5,
        name: "DigiKing 43吋",
        price: "4999"
    },
    {
        id: 6,
        name: "海爾 50型",
        price: "8988"
    },
]

function GetPage() {

    return `
        <table id="items-for-sell">
            <tbody id="items">
                <tr>
                    <td id="item-1">
                        <p>${items[0].name}</p>
                        <p>$${items[0].price}</p>
                    </td>
                    <td id="item-2">
                        <p>${items[1].name}</p>
                        <p>$${items[1].price}</p>
                    </td>
                    <td id="item-3">
                        <p>${items[2].name}</p>
                        <p>$${items[2].price}</p>
                    </td>
                </tr>
                <tr>
                    <td id="item-4">
                        <p>${items[3].name}</p>
                        <p>$${items[3].price}</p>
                    </td>
                    <td id="item-5">
                        <p>${items[4].name}</p>
                        <p>$${items[4].price}</p>
                    </td>
                    <td id="item-6">
                        <p>${items[5].name}</p>
                        <p>$${items[5].price}</p>
                    </td>
                </tr>
            </tbody>
        </table>
        <div id="checkout">
        </div>
        <div id="result"></div>
    `
}

export { items, GetPage }