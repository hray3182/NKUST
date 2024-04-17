export default function GetPage() {
    return `
    小明擁有
        <input type="text" id="money">
        <br>
        <table>
            <thead>
                <tr>
                    <td></td>
                    <td>單價</td>
                    <td>數量</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>鉛筆</td>
                    <td><input type="text"id="p-price"></td>
                    <td><input type="text" id="p-quantity"></td>
                </tr>
                <tr>
                    <td>橡皮擦</td>
                    <td><input type="text" id="e-price"></td>
                    <td><input type="text" id="e-quantity"></td>
                </tr>
            </tbody>
        </table>
        <div id="result"></div>

    `
}