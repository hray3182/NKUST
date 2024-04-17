export default function GetPage() {
    return `
   <span>台幣</span><input type="text" id="amount"><button id="cal">兌換</button>
   <select name="currency" id="currency">
        <option value="USD">美元</option>
        <option value="JPY">日元</option>
        <option value="CNY">人民幣</option>
        <option value="SGD">新加坡幣</option>
   </select>
   <span id="result"></span>
    `
}