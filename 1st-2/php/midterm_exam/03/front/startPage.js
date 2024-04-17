export default function GetPage() {
    return `
    <span>小明的全支付帳戶: </span>
        <input type="text" id="money">
        <table>
            <thead>
                <tr>
                    <td>品項</td>
                    <td>單價</td>
                    <td>數量</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>大乾麵</td>
                    <td>28</td>
                    <td>5</td>
                </tr>
                <tr>
                    <td>義美低脂鮮乳</td>
                    <td>167</td>
                    <td>1</td>
                </tr>
                <tr>
                    <td>澎澎沐浴乳</td>
                    <td>184</td>
                    <td>1</td>
                </tr>
            </tbody>
        </table>
        <button id="cal">結算</button><br>
        <span id="total"></span><br>
        <span id="result"></span>
    `
}