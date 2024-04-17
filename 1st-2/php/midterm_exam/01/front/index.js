import GetPage from "./startPage.js"

document.querySelector("#app").innerHTML = GetPage()
const calButton = document.querySelector("#cal")
calButton.addEventListener("click", handleClick)
const resultElem = document.querySelector("#result")

function handleClick() {
    const amount = document.querySelector("#amount").value
    console.log(amount)
    const currency = document.getElementById("currency").value
    console.log(currency)
    const reqBody = {
        amount: amount,
        currency: currency
    }
    axios.post("http://localhost/mid_exam/01/server/index.php", Qs.stringify(reqBody)
    ).then((res) => {
        console.log(res['data'])
        resultElem.innerHTML = res.data
    })
}