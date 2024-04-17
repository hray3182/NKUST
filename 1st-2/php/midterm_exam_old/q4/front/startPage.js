let tableData = ``

for (let i = 0; i < 10; i++) {
    const quantity1 = Math.floor(Math.random()*10)+1
    const quantity2 = Math.floor(Math.random()*10)+1
    const quantity3 = Math.floor(Math.random()*10)+1
    const quantitySum = quantity1 + quantity2 + quantity3
    tableData += `
    <tr class="detial">
        <td class="yellow">${i+1}</td>
        <td class="jan cost">${generageNum()}</td>
        <td class="jan price">${generageNum()}</td>
        <td class="jan quantity">${quantity1}</td>
        <td class="feb cost">${generageNum()}</td>
        <td class="feb price">${generageNum()}</td>
        <td class="feb quantity">${quantity2}</td>
        <td class="mar cost">${generageNum()}</td>
        <td class="mar price">${generageNum()}</td>
        <td class="mar quantity">${quantity3}</td>
        <td class="quantity-subtotal">${quantitySum}</td>
    </tr>
    `
}

function generageNum() {
    return Math.floor(Math.random()*20 + 70)
}

export default function GetPage() {
    return `
            <table>
            <thead>
                <tr>
                    <td rowspan="2">商品編號</td>
                    <td colspan="3">1月</td>
                    <td colspan="3">2月</td>
                    <td colspan="3">3月</td>
                    <td rowspan="2">總數量</td>
                </tr>
                <tr>
                    <td>成本</td>
                    <td>售價</td>
                    <td>數量</td>
                    <td>成本</td>
                    <td>售價</td>
                    <td>數量</td>
                    <td>成本</td>
                    <td>售價</td>
                    <td>數量</td>
                </tr>
            </thead>
            <tbody>
            ${tableData}
            
            <tr class="purple">
                <td>營業額</td>
                <td colspan="3" class="jan income"></td>
                <td colspan="3" class="feb income"></td>
                <td colspan="3" class="mar income"></td>
                <td class="total-income">總營業額</td>
            </tr>
            <tr class="red">
                <td>盈餘</td>
                <td colspan="3" class="jan profit"></td>
                <td colspan="3" class="feb profit"></td>
                <td colspan="3" class="mar profit"></td>
                <td class="total-profit">總盈餘</td>
            </tr>
            </tbody>
        </table>
        <button id="cal">計算</button>
    </div>
    `
}