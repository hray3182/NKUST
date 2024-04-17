export default function GetPage() {
    return `
        <div id="q1">
            <span class="result"></span>
            <span>1. 9+5=</span>
            <input type="radio" name="1" value="9">
            <label>9</label>
            <input type="radio" name="1" value="14">
            <label>14</label>
            <input type="radio" name="1" value="13">
            <label>13</label>
            <button class="sumbit">確定</button>
        </div>
        <div id="q2">
            <span class="result"></span>
            <span>2. 9+4=</span>
            <input type="radio" name="2" value="9">
            <label>9</label>
            <input type="radio" name="2" value="14">
            <label>14</label>
            <input type="radio" name="2" value="13">
            <label>13</label>
            <button class="sumbit">確定</button>
        </div>
        <div id="q3">
            <span class="result"></span>
            <span>3. 9+3=</span>
            <input type="radio" name="3" value="9">
            <label>9</label>
            <input type="radio" name="3" value="14">
            <label>14</label>
            <input type="radio" name="3" value="12">
            <label>12</label>
            <button class="sumbit">確定</button>
        </div>
        <div id="q4">
            <span class="result"></span>
            <span>4. 9+2=</span>
            <input type="radio" name="4" value="9">
            <label>9</label>
            <input type="radio" name="4" value="14">
            <label>14</label>
            <input type="radio" name="4" value="11">
            <label>11</label>
            <button class="sumbit">確定</button>
            </div>
    `
}