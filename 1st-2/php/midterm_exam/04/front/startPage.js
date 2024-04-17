export default function GetPage() {
    return `
    <table id="input">
            ${generateInputTable()}
    </table>
    <button id="cal">計算</button>
    <div id="result"></div>
    `
}

function generateInputTable() {
    const names = ["小明", "小華", "小英", "小南", "小米"]
    let html = ""
    for (let name of names) {
        html += `<tr><td>${name}</td>`
        for (let i =0; i < 12; i++) {
            html += `<td><input type='text'value="${Math.round(Math.random()*50) + 50}"></td>`
        }
        html += "</tr>"
    }
    return html
}