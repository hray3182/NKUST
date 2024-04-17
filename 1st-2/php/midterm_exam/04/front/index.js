import GetPage from "./startPage.js"

document.querySelector("#app").innerHTML = GetPage()

document.querySelector("#cal").addEventListener("click", handleCal)

function handleCal() {
    let html = `
            <table>
            <thead>
                <tr>
                    <td></td>
                    <td>第一季</td>
                    <td>第二季</td>
                    <td>第三季</td>
                    <td>第四季</td>
                    <td>年平均</td>
                </tr>
            </thead>
            <tbody>
    `
    Array.from(document.querySelectorAll("#input tr")).forEach(tr => {
        let seasonOne =0
        let seasonTwo = 0
        let seasonThree = 0 
        let seasonFour = 0
        for (let i =1; i < 13; i++) {
            const value = Number(tr.children[i].children[0].value)
            if (i < 4) {
                seasonOne += (value /4)
            } else if (i < 7) {
                seasonTwo += (value /4)
            } else if (i < 10) {
                seasonThree += (value /4)
            } else {
                seasonFour += (value /4)
            }
        }
        let total = (seasonOne + seasonTwo + seasonThree + seasonFour)/4
        html += `
            <tr>
                <td>${tr.children[0].textContent}</td>
                <td style="color:${(seasonOne > total)? "black": "red"};">${seasonOne}</td>
                <td style="color:${(seasonTwo > total)? "black": "red"};">${seasonTwo}</td>
                <td style="color:${(seasonThree > total)? "black": "red"};">${seasonThree}</td>
                <td style="color:${(seasonFour > total)? "black": "red"};">${seasonFour}</td>
                <td>${total.toFixed(2)}</td>
            </tr>
        `
    })
    html += "</tbody></table>"
    document.querySelector("#result").innerHTML = html
}