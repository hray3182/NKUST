import GetPage from "./startPage.js"

document.querySelector("#app").innerHTML = GetPage()
for (let i = 0; i < 4; i++) {
    document.querySelector(`#q${i+1} > button`).addEventListener("click", () => handleClick(i+1))
}
function handleClick(id) {
    const resultElem = document.querySelector(`#q${id} > .result`)
    const radios = document.querySelectorAll(`#q${id} > input[type="radio"]`)
    let ans = 0
    radios.forEach((radio) => {
        if (radio.checked) {
            ans = radio.value
        }
    })
    const reqBody = {
        q: id,
        ans: ans
    }
    axios.post("http://localhost/mid_exam/02/server/index.php", Qs.stringify(reqBody)
    ).then((res) => {
        resultElem.innerHTML = res.data.result
        resultElem.style = `color: ${res.data.color}`
    })
}

